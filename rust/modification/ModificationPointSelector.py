"""
ModificationPointSelector

Single responsibility: given a full AST, pick exactly ONE eligible
MarkedASTNode at random.

Eligibility now has two independent levels:

  scope_checker  - which ENCLOSING FUNCTIONS may contain a modification point
                   (e.g. Constraint(FunctionDefinition, "is_unsafe", True)).
                   Applied to FunctionDefinition nodes. None = whole AST.

  checker        - which expression TYPES/contents inside those functions are
                   allowed (applied to `marked.node`, not the wrapper).
                   None = ANY marked expression is allowed.

Why two levels: MarkedASTNode only wraps expressions, never functions, so a
function-level Constraint applied to `marked.node` can never match. The
function has to be found first, and its marked nodes collected from inside it.

This class does no editing and no candidate generation.
"""

import random

from rust.nodes.MarkedASTNode import MarkedASTNode
from rust.nodes.TopLevel import FunctionDefinition
from rust.visitors.NodeCollector import NodeCollector
from rust.modification.Constraint import ConstraintChecker


class ModificationPointSelector:

    def __init__(
        self,
        checker: ConstraintChecker = None,
        rng: random.Random = None,
        scope_checker: ConstraintChecker = None,
    ):
        self._checker = checker              # None => any expression type
        self._scope_checker = scope_checker  # None => whole AST
        self._rng = rng or random.Random()

    def _scopes(self, ast) -> list:
        if self._scope_checker is None:
            return [ast]
        return NodeCollector(
            FunctionDefinition,
            lambda fn: self._scope_checker.satisfies_any(fn),
        ).collect(ast)

    def _is_eligible_point(self, marked) -> bool:
        return self._checker is None or self._checker.satisfies_any(marked.node)

    def eligible_points(self, ast) -> list:
        """All eligible MarkedASTNodes (deduplicated). Useful for debugging."""
        points, seen = [], set()
        for scope in self._scopes(ast):
            for marked in NodeCollector(MarkedASTNode, self._is_eligible_point).collect(scope):
                if id(marked) not in seen:
                    seen.add(id(marked))
                    points.append(marked)
        return points

    def select(self, ast) -> MarkedASTNode:
        """Returns one randomly-chosen eligible MarkedASTNode, or None if there are none."""
        eligible = self.eligible_points(ast)
        if not eligible:
            return None
        return self._rng.choice(eligible)
