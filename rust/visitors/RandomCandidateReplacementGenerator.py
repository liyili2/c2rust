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
class extends RustASTGenerator directly, exactly like ASTEditor does.
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
"""

import random

from rust.visitors.Base import RustASTGenerator
from rust.nodes.MarkedASTNode import MarkedASTNode
from rust.nodes.TopLevel import FunctionDefinition
from rust.nodes.Statement import Block, LetStmt
from rust.nodes.Expression import (
    IdentifierExpression, BinaryExpression, FunctionCallExpression,
    BorrowExpression, ArrayLiteral, CastExpression, UnaryExpr,
    DereferenceExpr, ParenExpr, RangeExpression, QualifiedExpression,
)
from rust.modification.ScopeEnvironment import ScopeEnvironment


class RandomCandidateReplacementGenerator(RustASTGenerator):

    # --- operator groups: only swap an operator for another in the same
    # group, since we have no per-type "legal operator" metadata to check
    # against (§7: "do not assume all operators are interchangeable") ---
    _ARITHMETIC_OPS = ["+", "-", "*", "/", "%"]
    _COMPARISON_OPS = ["<", ">", "<=", ">=", "==", "!="]
    _LOGICAL_OPS = ["&&", "||"]
    _OP_GROUPS = [_ARITHMETIC_OPS, _COMPARISON_OPS, _LOGICAL_OPS]

    def __init__(self, selected: MarkedASTNode, rng: random.Random = None):
        self._selected_id = selected.get_id()
        self._rng = rng or random.Random()
        self._scope = ScopeEnvironment()

    # --- scope threading ---

    def _scope_with_params(self, params) -> ScopeEnvironment:
        scope = ScopeEnvironment()
        if isinstance(params, list):
            for param in params:
                scope = scope.with_binding(param.name(), param.type())
        return scope

    def visitFunctionDefinition(self, node: FunctionDefinition):
        outer_scope = self._scope
        self._scope = self._scope_with_params(node.params())
        try:
            return super().visitFunctionDefinition(node)
        finally:
            self._scope = outer_scope

    def visitBlock(self, node: Block):
        outer_scope = self._scope
        try:
            return super().visitBlock(node)
        finally:
            self._scope = outer_scope

    def visitLetStmt(self, node: LetStmt):
        rebuilt = super().visitLetStmt(node)
        for var_def in node.var_defs():
            self._scope = self._scope.with_binding(var_def.name(), var_def.type())
        return rebuilt

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
            return inner.accept(self)

        return handler(self, inner)

    # --- shared helper ---

    def _operator_group(self, op):
        for group in self._OP_GROUPS:
            if op in group:
                return group
        return [op]

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

        group = self._operator_group(node.op())
        other_ops = [op for op in group if op != node.op()]
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

    def _candidates_for_function_call(self, node: FunctionCallExpression):
        # Mutating the callee itself is NOT implemented: this repo has no
        # function-signature/arity registry to validate against (§8, §26).
        # Argument replacement is implemented since args()+scope are both
        # reliably available.
        if not node.args():
            return node
        names = self._scope.names()
        if not names:
            return node

        index = self._rng.randrange(len(node.args()))
        new_args = list(node.args())
        new_args[index] = IdentifierExpression(self._rng.choice(names))
        return FunctionCallExpression(node.caller(), new_args, node.callee())

    def _candidates_for_borrow(self, node: BorrowExpression):
        # The only reliably safe, structural mutation available: &T <-> &mut T.
        return BorrowExpression(node.expression(), not node.is_mutable())

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
        names = self._scope.names()
        if not names:
            return node
        return ParenExpr(IdentifierExpression(self._rng.choice(names)))

    def _candidates_for_range(self, node: RangeExpression):
        names = self._scope.names()
        if not names:
            return node
        if self._rng.random() < 0.5:
            return RangeExpression(IdentifierExpression(self._rng.choice(names)), node.last())
        return RangeExpression(node.initial(), IdentifierExpression(self._rng.choice(names)))

    def _candidates_for_qualified(self, node: QualifiedExpression):
        # QualifiedExpression has no fields/usage beyond wrapping one
        # expression anywhere in the repo (§9) - treated as a generic
        # single-child wrapper, same treatment as ParenExpr/Dereference.
        names = self._scope.names()
        if not names:
            return node
        return QualifiedExpression(IdentifierExpression(self._rng.choice(names)))


RandomCandidateReplacementGenerator._DISPATCH = {
    IdentifierExpression: RandomCandidateReplacementGenerator._candidates_for_identifier,
    BinaryExpression: RandomCandidateReplacementGenerator._candidates_for_binary,
    FunctionCallExpression: RandomCandidateReplacementGenerator._candidates_for_function_call,
    BorrowExpression: RandomCandidateReplacementGenerator._candidates_for_borrow,
    ArrayLiteral: RandomCandidateReplacementGenerator._candidates_for_array_literal,
    CastExpression: RandomCandidateReplacementGenerator._candidates_for_cast,
    UnaryExpr: RandomCandidateReplacementGenerator._candidates_for_unary,
    DereferenceExpr: RandomCandidateReplacementGenerator._candidates_for_dereference,
    ParenExpr: RandomCandidateReplacementGenerator._candidates_for_paren,
    RangeExpression: RandomCandidateReplacementGenerator._candidates_for_range,
    QualifiedExpression: RandomCandidateReplacementGenerator._candidates_for_qualified,
}
