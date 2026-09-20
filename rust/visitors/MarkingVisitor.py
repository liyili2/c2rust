"""
MarkingVisitor

Single behavior: wrap every expression that can be a modification point in a
MarkedASTNode. It does NOT check constraints or select anything - that is
Constraint / ConstraintChecker / ModificationPointSelector's job.

Each override is `MarkedASTNode(super().visitX(node))`: RustASTGenerator's default
visitX first rebuilds the node from its (recursively visited) children and keeps
its id, then the rebuilt node is wrapped. That is what makes NESTED expressions
modification points too, while every traversal detail stays in the base class.

Removed from the previous version (both were dead code):
  - visitExpression: no such method exists in AbstractASTVisitor, so nothing calls it.
  - visitArrayLiteral: ArrayLiteral inherits Literal.accept, which dispatches to
    visitLiteral, so this was never reached. (avl.rs has no array literals; if you
    need them later, override visitLiteral and mark only ArrayLiteral instances.)
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from rust.visitors.Base import RustASTGenerator
from rust.nodes.MarkedASTNode import MarkedASTNode
from rust.nodes.Expression import (
    QualifiedExpression, IdentifierExpression, BinaryExpression,
    FunctionCallExpression, BorrowExpression, CastExpression, UnaryExpr,
    DereferenceExpr, ParenExpr, RangeExpression,
)


class MarkingVisitor(RustASTGenerator):

    def _mark(self, rebuilt):
        """Wraps an already-rebuilt node; the single place where marking happens."""
        return MarkedASTNode(rebuilt)

    def visitQualifiedExpression(self, node: QualifiedExpression):
        return self._mark(super().visitQualifiedExpression(node))

    def visitIdentifierExpression(self, node: IdentifierExpression):
        return self._mark(super().visitIdentifierExpression(node))

    def visitBinaryExpression(self, node: BinaryExpression):
        return self._mark(super().visitBinaryExpression(node))

    def visitFunctionCallExpression(self, node: FunctionCallExpression):
        return self._mark(super().visitFunctionCallExpression(node))

    def visitBorrowExpression(self, node: BorrowExpression):
        return self._mark(super().visitBorrowExpression(node))

    def visitCastExpression(self, node: CastExpression):
        return self._mark(super().visitCastExpression(node))

    def visitUnaryExpr(self, node: UnaryExpr):
        return self._mark(super().visitUnaryExpr(node))

    def visitDereferenceExpr(self, node: DereferenceExpr):
        return self._mark(super().visitDereferenceExpr(node))

    def visitParenExpr(self, node: ParenExpr):
        return self._mark(super().visitParenExpr(node))

    def visitRangeExpression(self, node: RangeExpression):
        return self._mark(super().visitRangeExpression(node))