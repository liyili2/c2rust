"""
ModificationPointSelector

Single responsibility: given a full AST and a ConstraintChecker describing
which modification points are eligible, pick exactly ONE eligible
MarkedASTNode at random.

This is the "selection" half of the select-then-generate pipeline described
by QGen's RandomCandidateReplacementProgramGenerator: constraints describe
eligibility of a modification point's WRAPPED CONTENT (e.g. "is a
BinaryExpression"), not the MarkedASTNode wrapper itself, so the checker is
applied to `marked.node`, not `marked`.

This class does no editing and no candidate generation - just: of all the
eligible points in this AST, which one are we touching this run?
"""

import random

from rust.nodes.MarkedASTNode import MarkedASTNode
from rust.visitors.NodeCollector import NodeCollector
from rust.modification.Constraint import ConstraintChecker


class ModificationPointSelector:

    def __init__(self, checker: ConstraintChecker = None, rng: random.Random = None):
        self._checker = checker or ConstraintChecker()
        self._rng = rng or random.Random()

    def select(self, ast) -> MarkedASTNode:
        """Returns one randomly-chosen eligible MarkedASTNode, or None if there are none."""
        eligible = NodeCollector(
            MarkedASTNode,
            lambda marked: self._checker.satisfies_any(marked.node),
        ).collect(ast)

        if not eligible:
            return None

        return self._rng.choice(eligible)
