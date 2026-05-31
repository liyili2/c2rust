import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
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

class MarkingVisitor:
    def __init__(self, program):
        self.program = program

    def visit(self, node: ASTNode) -> ASTNode:
        """Recursively visits children, then dispatches to specific visit methods."""
        # First, recurse into children (bottom-up traversal)
        self._visit_children(node)
        
        # Dispatch based on the specific expression type
        match node:
            case QualifiedExpression():
                return self.visitQualifiedExpression(node)
            case IdentifierExpression():
                return self.visitIdentifierExpression(node)
            case BinaryExpression():
                return self.visitBinaryExpression(node)
            case FunctionCallExpression():
                return self.visitFunctionCallExpression(node)
            case BorrowExpression():
                return self.visitBorrowExpression(node)
            case ArrayLiteral():
                return self.visitArrayLiteral(node)
            case CastExpression():
                return self.visitCastExpression(node)
            case UnaryExpr():
                return self.visitUnaryExpr(node)
            case DereferenceExpr():
                return self.visitDereferenceExpr(node)
            case ParenExpr():
                return self.visitParenExpr(node)
            case RangeExpression():
                return self.visitRangeExpression(node)
            # Catch-all for any other expression subclasses not explicitly matched
            case Expression():
                return self.visitExpression(node)
            case _:
                # Non-expression nodes are returned exactly as-is
                return node

    def _mark_and_wrap(self, node: Expression) -> ASTNode:
        """Helper to avoid duplicating the wrapping logic in every visit method."""
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

    def _visit_children(self, node: ASTNode):
        for attr_name in list(node.__dict__.keys()):
            if attr_name == 'parent':
                continue

            attr = getattr(node, attr_name)

            if isinstance(attr, CloneableASTNode):
                # Using 'self.visit' instead of 'self.mark'
                setattr(node, attr_name, self.visit(attr))

            elif isinstance(attr, (list, tuple)):
                new_list = []
                for item in attr:
                    if isinstance(item, CloneableASTNode):
                        new_list.append(self.visit(item))
                    else:
                        new_list.append(item)
                setattr(node, attr_name, new_list)

            elif isinstance(attr, dict):
                new_dict = {}
                for k, v in attr.items():
                    if isinstance(v, CloneableASTNode):
                        new_dict[k] = self.visit(v)
                    else:
                        new_dict[k] = v
                setattr(node, attr_name, new_dict)

    def run(self):
        """Start marking from the program's items."""
        new_items = []
        for item in self.program.items:
            new_items.append(self.visit(item))
        self.program.items = new_items
        return self.program
