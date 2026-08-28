"""
ASTEditor

A RustASTGenerator: given an AST, produces a brand-new AST equivalent to
the input, except that every function matching the eligibility constraints
has its modification points (MarkedASTNode positions) shuffled in the
generated copy. The original AST passed in is never mutated.

Single responsibility of the one override below: for the FunctionDefinition
currently being rebuilt, decide whether it's eligible, and if so, shuffle
it. Everything else is handled by inherited default behavior:

  - RustASTGenerator's own default traversal rebuilds the rest of the AST
    unchanged - this class does not reimplement walking the tree.
  - ConstraintChecker (rust.constraints.Constraints) answers "is this
    function eligible?" against the node already in hand - no traversal
    needed for that, so NodeCollector is not used here; using it just to
    re-find functions the generator is already visiting would be a
    redundant second traversal.
  - NodeCollector(MarkedASTNode) IS used, but for a different job: once a
    function is confirmed eligible, gathering the flat list of marked
    positions inside its freshly-rebuilt body, since shuffling is a
    whole-list operation a single-node visit method can't do alone.
  - MarkedNodeShuffler performs the actual edit on that freshly-rebuilt
    (and therefore already-independent-of-the-original) body.

Usage:
    editor = ASTEditor()
    new_ast = ast.accept(editor)   # `ast` itself is left untouched
"""

from rust.visitors.Base import RustASTGenerator
from rust.visitors.NodeCollector import NodeCollector
from rust.nodes.MarkedASTNode import MarkedASTNode
from rust.nodes.TopLevel import FunctionDefinition
from rust.modification.Constraint import ConstraintChecker
from rust.modification.MarkedNodeShuffler import MarkedNodeShuffler

class ASTEditor(RustASTGenerator):

    def __init__(self,
                 checker: ConstraintChecker = None,
                 shuffler: MarkedNodeShuffler = None):
        self._checker = checker or ConstraintChecker()
        self._marked_collector = NodeCollector(MarkedASTNode)
        self._shuffler = shuffler or MarkedNodeShuffler()

    def visitFunctionDefinition(self, node: FunctionDefinition):
        rebuilt = super().visitFunctionDefinition(node)

        if self._checker.satisfies_any(node):
            marked_nodes = self._marked_collector.collect(rebuilt.body())
            self._shuffler.shuffle(marked_nodes)

        return rebuilt