"""
ASTEditor

A RustASTGenerator: given an AST and ONE already-selected modification
point (a MarkedASTNode), produces a brand-new AST identical to the input
except that the selected point is replaced with a generated candidate.
The original AST passed in is never mutated.

This replaces the earlier "shuffle every marked node inside every eligible
function" design with QGen's select-one-point / generate-a-candidate
model. Selection (ModificationPointSelector) and candidate generation
(CandidateGenerator) both happen elsewhere and are just handed to this
class - ASTEditor's only job is the one override below: walk the tree as
RustASTGenerator normally would, and when the node currently being
rebuilt is the one selected point, substitute in whatever the candidate
generator produces instead of regenerating it normally. Every other
MarkedASTNode - eligible or not, just not the one selected this run -
falls through to RustASTGenerator's own default visitMarkedASTNode, which
rebuilds it and re-wraps it in a fresh MarkedASTNode. That matters: it
keeps every other modification point marked and available, so a later
selection run over the same base AST can pick a different point without
needing to re-run the marking pass.

Usage:
    checker = ConstraintChecker()
    selected = ModificationPointSelector(checker).select(ast)
    if selected is not None:
        new_ast = ast.accept(ASTEditor(selected, candidate_generator))
"""

from rust.visitors.Base import RustASTGenerator
from rust.nodes.MarkedASTNode import MarkedASTNode
from rust.modification.CandidateGenerator import CandidateGenerator


class ASTEditor(RustASTGenerator):

    def __init__(self, selected: MarkedASTNode, candidate_generator: CandidateGenerator):
        self._selected_id = selected.get_id()
        self._candidate_generator = candidate_generator

    def visitMarkedASTNode(self, node: MarkedASTNode):
        if node.get_id() == self._selected_id:
            return self._candidate_generator.generate(node.node)

        return super().visitMarkedASTNode(node)
