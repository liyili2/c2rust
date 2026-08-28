"""
UnsafeFunctionShuffleEditor

Coordinates the "shuffle modification points inside eligible functions" edit
by composing single-purpose collaborators:

  - a ConstraintChecker (rust.constraints.Constraints) : the eligibility
    condition(s), expressed as declarative Constraint(node_type, attribute,
    expected_value) data rather than code. Defaults to the static
    DEFAULT_CONSTRAINTS list (currently just "is_unsafe == True"). Adding a
    condition means adding a Constraint(...) entry - never touches this file.
  - NodeCollector(FunctionDefinition, checker.satisfies_any) : applies the
    checker during traversal to find eligible functions
  - NodeCollector(MarkedASTNode)                            : finds the
    modification points inside an eligible function's body
  - MarkedNodeShuffler                                      : performs the
    actual edit
"""

from rust.nodes.TopLevel import FunctionDefinition
from rust.nodes.MarkedASTNode import MarkedASTNode
from rust.visitors.NodeCollector import NodeCollector
from rust.modification.MarkedNodeShuffler import MarkedNodeShuffler
from rust.modification.Constraint import ConstraintChecker


class UnsafeFunctionShuffleEditor:

    def __init__(self,
                 checker: ConstraintChecker = None,
                 shuffler: MarkedNodeShuffler = None):
        checker = checker or ConstraintChecker()
        self._eligible_finder = NodeCollector(FunctionDefinition, checker.satisfies_any)
        self._marked_collector = NodeCollector(MarkedASTNode)
        self._shuffler = shuffler or MarkedNodeShuffler()

    def edit(self, ast) -> None:
        """Shuffles the modification points inside every eligible function reachable from `ast`."""
        for func in self._eligible_finder.collect(ast):
            marked_nodes = self._marked_collector.collect(func.body())
            self._shuffler.shuffle(marked_nodes)
