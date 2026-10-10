"""
RandomCandidateReplacementGenerator

Rust-native successor to the old RandomCandidateReplacementProgramGenerator.
Same architecture: a full AST-reconstructing generator that threads scope/
type state through traversal, and at the one selected MarkedASTNode,
dispatches to a small, specialized helper per expression type instead of
one monolithic if/elif. Each helper enumerates legal candidates and picks
one at random (enumeration and selection are kept separate, per the old
system's philosophy).

Why this can't just be a CandidateGenerator (rust.modification.CandidateGenerator):
that interface is generate(node) with no context. Real scope-awareness
(§18: "variables visible at the mutation location") requires state that
only grows as the generator descends - params, then each `let` in
sequence. That can only live on the traversing generator itself, so this
class extends ScopeTrackingGenerator (a RustASTGenerator that owns the scope
state), the same way ASTEditor extends RustASTGenerator.
ASTEditor + CandidateGenerator are untouched; this is a second, richer
option, not a replacement.

Candidate representation: no new wrapper class was introduced. Matching
ASTEditor's already-established behavior, the selected MarkedASTNode is
replaced with the raw candidate expression directly (unwrapped) - that IS
this repository's equivalent of QXCandidateTop; inventing a second concept
would violate §21.

Pipeline:
    MarkedASTNode (selected)
        -> visitMarkedASTNode
        -> _DISPATCH[type(inner)]           (table, not if/elif)
        -> node-specific helper
        -> enumerate candidates -> rng.choice
        -> raw candidate node (unwrapped)

Every other MarkedASTNode falls through to RustASTGenerator's own default
visitMarkedASTNode (rebuilt + re-marked), same as ASTEditor.

Function calls have NO handler on purpose: a call selected as the modification
point is rebuilt unchanged (its arguments are separate points of their own).
"""

import random

from rust.visitors.ScopeTrackingGenerator import ScopeTrackingGenerator
from rust.nodes.MarkedASTNode import MarkedASTNode
from rust.nodes.Expression import (
    IdentifierExpression, BinaryExpression,
    BorrowExpression, ArrayLiteral, CastExpression, UnaryExpr,
    DereferenceExpr, ParenExpr, RangeExpression, QualifiedExpression,
)
from rust.modification.ProgramInventory import ProgramInventory


class RandomCandidateReplacementGenerator(ScopeTrackingGenerator):

    # --- operator groups: only swap an operator for another in the same
    # group, since we have no per-type "legal operator" metadata to check
    # against (§7: "do not assume all operators are interchangeable") ---
    _ARITHMETIC_OPS = ["+", "-", "*", "/", "%"]
    _COMPARISON_OPS = ["<", ">", "<=", ">=", "==", "!="]
    _LOGICAL_OPS = ["&&", "||"]
    _OP_GROUPS = [_ARITHMETIC_OPS, _COMPARISON_OPS, _LOGICAL_OPS]

    def __init__(self, selected: MarkedASTNode, rng: random.Random = None,
                 inventory: ProgramInventory = None):
        super().__init__()
        self._selected_id = selected.get_id()
        self._rng = rng or random.Random()
        self._inventory = inventory   # program-wide operators/numbers; None = static op groups
        self._replacement = None

    def replacement(self):
        """The node that took the selected node's place (None until the visitor has run)."""
        return self._replacement

    # --- dispatch ---

    def visitMarkedASTNode(self, node: MarkedASTNode):
        if node.get_id() != self._selected_id:
            return super().visitMarkedASTNode(node)

        inner = node.node
        handler = self._DISPATCH.get(type(inner))
        if handler is None:
            # Safe fallback (§17.B): no specialized strategy for this type -
            # rebuild it unchanged rather than risk corrupting an AST shape
            # we don't have a verified mutation for.
            self._replacement = inner.accept(self)
        else:
            self._replacement = handler(self, inner)

        return self._replacement

    # --- shared helpers ---

    def _operator_group(self, op):
        for group in self._OP_GROUPS:
            if op in group:
                return group
        return [op]

    def _operator_pool(self, op):
        """Operators `op` may be swapped for: same group, and (when an inventory is
        given) only operators the program itself already uses."""
        group = self._operator_group(op)
        if self._inventory is not None:
            group = self._inventory.operators_in_group(group)
        return [o for o in group if o != op]

    @staticmethod
    def _unwrap(expr):
        """Children of a marked node are MarkedASTNode wrappers; isinstance() needs the inner node."""
        return expr.node if isinstance(expr, MarkedASTNode) else expr

    def _replace_expression_with_identifier(self, current):
        """Swap `current` for a DIFFERENT in-scope identifier (excluding its own name
        when it already is a bare identifier). No-op if nothing else is visible."""
        inner = self._unwrap(current)
        excluded = inner.name() if isinstance(inner, IdentifierExpression) else None
        names = self._scope.names_excluding(excluded)
        if not names:
            return current
        chosen = self._rng.choice(names)
        return IdentifierExpression(chosen, self._scope.type_of(chosen))

    # --- node-specific candidate helpers ---
    # Each one enumerates legal candidates, then picks one at random.
    # Every helper falls back to returning the node unchanged when it finds
    # no legal alternative - a safe no-op, never a guess.

    def _candidates_for_identifier(self, node: IdentifierExpression):
        names = self._scope.names_matching_type(node.type(), excluded_name=node.name())
        if not names:
            return node
        chosen = self._rng.choice(names)
        return IdentifierExpression(chosen, self._scope.type_of(chosen))

    def _candidates_for_binary(self, node: BinaryExpression):
        strategies = []

        other_ops = self._operator_pool(node.op())
        if other_ops:
            strategies.append(BinaryExpression(node.left(), self._rng.choice(other_ops), node.right()))

        left_name = getattr(node.left(), "name", lambda: None)()
        left_candidates = self._scope.names_excluding(left_name)
        if left_candidates:
            strategies.append(BinaryExpression(IdentifierExpression(self._rng.choice(left_candidates)), node.op(), node.right()))

        right_name = getattr(node.right(), "name", lambda: None)()
        right_candidates = self._scope.names_excluding(right_name)
        if right_candidates:
            strategies.append(BinaryExpression(node.left(), node.op(), IdentifierExpression(self._rng.choice(right_candidates))))

        return self._rng.choice(strategies) if strategies else node

    def _candidates_for_borrow(self, node: BorrowExpression):
        return BorrowExpression(self._replace_expression_with_identifier(node.expression()), node.is_mutable())

    def _candidates_for_array_literal(self, node: ArrayLiteral):
        # Swap two elements already in the SAME array - always type-safe
        # since Rust arrays are homogeneous, unlike inventing a new value.
        elements = node.value()
        if len(elements) < 2:
            return node
        i, j = self._rng.sample(range(len(elements)), 2)
        new_elements = list(elements)
        new_elements[i], new_elements[j] = new_elements[j], new_elements[i]
        return ArrayLiteral(new_elements)

    def _candidates_for_cast(self, node: CastExpression):
        # Target-type mutation is NOT implemented: type_expressions'
        # legal shapes aren't verifiable from this repo alone (§12, §26).
        names = self._scope.names()
        if not names:
            return node
        return CastExpression(IdentifierExpression(self._rng.choice(names)), node.type())

    def _candidates_for_unary(self, node: UnaryExpr):
        # No second legal operator in either observed group (! or -) to
        # swap to, so only the operand is mutated (§13, §26).
        names = self._scope.names()
        if not names:
            return node
        return UnaryExpr(node.op(), IdentifierExpression(self._rng.choice(names)))

    def _candidates_for_dereference(self, node: DereferenceExpr):
        names = self._scope.names()
        if not names:
            return node
        return DereferenceExpr(IdentifierExpression(self._rng.choice(names)))

    def _candidates_for_paren(self, node: ParenExpr):
        return ParenExpr(self._replace_expression_with_identifier(node.expression()))

    def _candidates_for_range(self, node: RangeExpression):
        names = self._scope.names()
        if not names:
            return node
        if self._rng.random() < 0.5:
            return RangeExpression(IdentifierExpression(self._rng.choice(names)), node.last())
        return RangeExpression(node.initial(), IdentifierExpression(self._rng.choice(names)))

    def _candidates_for_qualified(self, node: QualifiedExpression):
        # Single-child wrapper: same treatment as Borrow/Paren.
        return QualifiedExpression(self._replace_expression_with_identifier(node.expression()))


RandomCandidateReplacementGenerator._DISPATCH = {
    IdentifierExpression: RandomCandidateReplacementGenerator._candidates_for_identifier,
    BinaryExpression: RandomCandidateReplacementGenerator._candidates_for_binary,
    BorrowExpression: RandomCandidateReplacementGenerator._candidates_for_borrow,
    ArrayLiteral: RandomCandidateReplacementGenerator._candidates_for_array_literal,
    CastExpression: RandomCandidateReplacementGenerator._candidates_for_cast,
    UnaryExpr: RandomCandidateReplacementGenerator._candidates_for_unary,
    DereferenceExpr: RandomCandidateReplacementGenerator._candidates_for_dereference,
    ParenExpr: RandomCandidateReplacementGenerator._candidates_for_paren,
    RangeExpression: RandomCandidateReplacementGenerator._candidates_for_range,
    QualifiedExpression: RandomCandidateReplacementGenerator._candidates_for_qualified,
}