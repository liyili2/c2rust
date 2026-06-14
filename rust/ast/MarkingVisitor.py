import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from rust.ast.RustASTVisitor  import RustASTVisitor
from rust.ast.Expression import QualifiedExpression, IdentifierExpression, BinaryExpression, FunctionCallExpression, \
    BorrowExpression, ArrayLiteral, CastExpression, UnaryExpr, DereferenceExpr, ParenExpr, RangeExpression, SafeWrapper, \
    ByteLiteralExpression, TypePath
from rust.ast.Func import FunctionParamList, Param
from rust.ast.Program import Program
from rust.ast.Statement import LetStmt, ForStmt, IfStmt, AssignStmt, ReturnStmt, WhileStmt, MatchStmt, MatchArm, \
    MatchPattern, CompoundAssignment, LoopStmt, BreakStmt, ContinueStmt, TypeWrapper
from rust.ast.VarDef import VarDef
from rust.ast.Struct import StructField
from rust.ast.TopLevel import *
from rust.ast.Block import Block
from rust.ast.ASTNode import ASTNode
from rust.ast.Type import SafeNonNullWrapper, SignedIntType, StringType, BoolType, ArrayType, \
    PathType, \
    GenericType, ReferenceType, SliceType, CharType, UnknownType, UnsignedIntType, FloatingPointType, PointerType

from rust.ast.ASTNode import ASTNode, CloneableASTNode
from rust.ast.Expression import Expression
from rust.ast.MarkedASTNode import MarkedASTNode

class MarkingVisitor(RustASTVisitor):
    def __init__(self, program):
        self.program = program

    def _mark_and_wrap(self, node: Expression) -> ASTNode:
        """Helper to avoid duplicating the wrapping logic in every visit method."""
        # print("marking\n")
        marked = MarkedASTNode(node)
        self.program.add_marked(marked)
        return marked

    def visitQualifiedExpression(self, node: QualifiedExpression):
        return self._mark_and_wrap(node)

    def visitIdentifierExpression(self, node: IdentifierExpression):
        return self._mark_and_wrap(node)

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
