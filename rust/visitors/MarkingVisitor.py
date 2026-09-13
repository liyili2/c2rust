import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from rust.visitors.RustASTVisitor import RustASTVisitor
from rust.nodes.Expression import QualifiedExpression, IdentifierExpression, BinaryExpression, FunctionCallExpression, \
    BorrowExpression, ArrayLiteral, CastExpression, UnaryExpr, DereferenceExpr, ParenExpr, RangeExpression

from rust.nodes.ASTNode import ASTNode
from rust.nodes.Expression import Expression
from rust.nodes.MarkedASTNode import MarkedASTNode

class MarkingVisitor(RustASTVisitor):
    def __init__(self):
        pass

    # def visit(self, node):
    #     if node is None:
    #         return None

    #     # Fix: Intercept raw python primitive types to prevent base match-case crashes
    #     if isinstance(node, (int, str, bool, float)):
    #         return node

    #     return super().visit(node)

    def _mark_and_wrap(self, node: Expression) -> ASTNode:
        """Helper to avoid duplicating the wrapping logic in every visit method."""
        marked = MarkedASTNode(node)
        return marked

    def visitQualifiedExpression(self, node: QualifiedExpression):
        return self._mark_and_wrap(node)

    def visitIdentifierExpression(self, node: IdentifierExpression):
        return MarkedASTNode(node)

    def visitBinaryExpression(self, node: BinaryExpression):
        return self._mark_and_wrap(node)

    def visitFunctionCallExpression(self, node: FunctionCallExpression):
        return self._mark_and_wrap(node)

    def visitBorrowExpression(self, node: BorrowExpression):
        return self._mark_and_wrap(node)

    def visitArrayLiteral(self, node: ArrayLiteral):
        return self._mark_and_wrap(node)

    def visitCastExpression(self, node: CastExpression):
        return self._mark_and_wrap(node)

    def visitUnaryExpr(self, node: UnaryExpr):
        return self._mark_and_wrap(node)

    def visitDereferenceExpr(self, node: DereferenceExpr):
        return self._mark_and_wrap(node)

    def visitParenExpr(self, node: ParenExpr):
        return self._mark_and_wrap(node)

    def visitRangeExpression(self, node: RangeExpression):
        return self._mark_and_wrap(node)

    def visitExpression(self, node: Expression):
        return self._mark_and_wrap(node)
