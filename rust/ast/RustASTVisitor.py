import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from rust.ast.Expression import QualifiedExpression, IdentifierExpression, BinaryExpression, FunctionCallExpression, \
    BorrowExpression, ArrayLiteral, CastExpression, StrLiteral, UnaryExpr, DereferenceExpr, ParenExpr, RangeExpression, SafeWrapper, \
    ByteLiteralExpression, TypePath, IntLiteral, ArrayAccess, FieldAccessExpr
from rust.ast.Func import FunctionParamList, Param
from rust.ast.Program import Program
from rust.ast.Statement import LetStmt, ForStmt, IfStmt, AssignStmt, ReturnStmt, WhileStmt, MatchStmt, MatchArm, \
    MatchPattern, CompoundAssignment, LoopStmt, BreakStmt, ContinueStmt, TypeWrapper
from rust.ast.Statement import Block as BlockStmt
from rust.ast.VarDef import VarDef
from rust.ast.Struct import StructField
from rust.ast.TopLevel import *
from rust.ast.Block import Block
from rust.ast.ASTNode import ASTNode
from rust.ast.Type import SafeNonNullWrapper, SignedIntType, StringType, BoolType, ArrayType, \
    PathType, \
    GenericType, ReferenceType, SliceType, CharType, UnknownType, UnsignedIntType, FloatingPointType, PointerType

class RustASTVisitor:

    def visit(self, node: ASTNode):
        # print("class is ", node.__class__)
        match node:
            case Program():
                return self.visitProgram(node)
            case FunctionDef():
                return self.visitFunctionDef(node)
            case FunctionParamList():
                return self.visitFunctionParamList(node)
            case Param():
                return self.visitParam(node)
            case StructDef():
                return self.visitStructDef(node)
            case StructField():
                return self.visitStructField(node)
            case LetStmt():
                return self.visitLetStmt(node)
            case ForStmt():
                return self.visitForStmt(node)
            case IfStmt():
                return self.visitIfStmt(node)
            case AssignStmt():
                return self.visitAssignStmt(node)
            case ReturnStmt():
                return self.visitReturnStmt(node)
            case WhileStmt():
                return self.visitWhileStmt(node)
            case MatchStmt():
                return self.visitMatchStmt(node)
            case MatchArm():
                return self.visitMatchArm(node)
            case MatchPattern():
                return self.visitMatchPattern(node)
            case CompoundAssignment():
                return self.visitCompoundAssignment(node)
            # case ExpressionStmt():
            #     return self.visitExpressionStmt(ctx)
            case LoopStmt():
                return self.visitLoopStmt(node)
            case BreakStmt():
                return self.visitBreakStmt(node)
            case ContinueStmt():
                return self.visitContinueStmt(node)
            # case CallStmt():
            #     return self.visitCallStmt(ctx)
            # case UnsafeBlock():
            #     return self.visitUnsafeBlock(ctx)
            case Block():
                return self.visitBlock(node)
            # case InitBlock():
            #     return self.visitInitBlock(ctx)
            # case MutableExpr():
            #     return self.visitMutableExpr(ctx)
            case QualifiedExpression():
                return self.visitQualifiedExpression(node)
            case IdentifierExpression():
                return self.visitIdentifierExpression(node)
            case BinaryExpression():
                return self.visitBinaryExpression(node)
            case FunctionCallExpression():
                return self.visitFunctionCallExpression(node)
            case ArrayAccess():
                return self.visitArrayAccess(node)
            # case UnsafeExpression():
            #     return self.visitUnsafeExpression(ctx)
            # case BasicTypeCastExpr():
            #     return self.visitBasicTypeCastExpr(ctx)
            # case TypeAccessExpr():
            #     return self.visitTypeAccessExpr(ctx)
            # case TypeWrapperExpr():
            #     return self.visitTypeWrapperExpr(ctx)
            # case BoxWrapperExpr():
            #     return self.visitBoxWrapperExpr(ctx)
            case BorrowExpression():
                return self.visitBorrowExpression(node)
            # case VariableRef():
            #     return self.visitVariableRef(ctx)
            # case ReferenceExpr():
            #     return self.visitReferenceExpr(ctx)
            case ArrayLiteral():
                return self.visitArrayLiteral(node)
            case IntLiteral():
                return self.visitIntLiteral(node)
            case StrLiteral():
                return self.visitStrLiteral(node)
            case CastExpression():
                return self.visitCastExpression(node)
            case UnaryExpr():
                return self.visitUnaryExpr(node)
            # case MethodCallExpr():
            #     return self.visitMethodCallExpr(ctx)
            case DereferenceExpr():
                return self.visitDereferenceExpr(node)
            # case IndexExpr():
            #     return self.visitIndexExpr(ctx)
            case ParenExpr():
                return self.visitParenExpr(node)
            case RangeExpression():
                return self.visitRangeExpression(node)
            case SafeWrapper():
                return self.visitSafeWrapper(node)
            case BlockStmt():
                return self.visitBlockStmt(node)
            case VarDef():
                return self.visitVarDef(node)
            case FieldAccessExpr():
                return self.visitFieldAccessExpr(node)
            case _:
                raise NotImplementedError(f"No visit method defined for {type(node)}")

    def visitProgram(self, ctx: Program):
        ctx.children = [exp.accept(self) for exp in ctx.getChildren()]
        return ctx

    def visitFunctionDef(self, ctx: FunctionDef):
        if isinstance(ctx.params, list):
            ctx.params = [p.accept(self) for p in ctx.params]
        else:
            ctx.params = ctx.params.accept(self)
        ctx.body = ctx.body.accept(self)
        if (ctx.return_type):
            ctx.return_type = ctx.return_type.accept(self)
        return ctx

    def visitFunctionParamList(self, ctx: FunctionParamList):
        ctx.params = [p.accept(self) for p in ctx.params]
        return ctx

    def visitParam(self, ctx: Param):
        return ctx

    def visitStructDef(self, ctx: StructDef):
        ret = True
        for child in ctx.getChildren():
            self.visit(child)

    def visitStructField(self, node: StructField):
        # mut = "mut " if node.mutable else ""
        self.visit(node.dtype)

    def visitLetStmt(self, node: LetStmt):
        node.var_defs = [i.accept(self) for i in node.var_defs]
        node.values = [i.accept(self) for i in node.values]
        return node

    def visitForStmt(self, node: ForStmt):
        node.iterable = node.iterable.accept(self)
        node.body = node.body.accept(self)
        return node

    def visitIfStmt(self, node: IfStmt):
        node.condition = node.condition.accept(self)
        node.then_branch = node.then_branch.accept(self)
        if node.else_branch is not None:
            node.else_branch = node.else_branch.accept(self)
        return node

    def visitAssignStmt(self, node: AssignStmt):
        node.target = node.target.accept(self)
        node.value = node.value.accept(self)
        return node

    def visitReturnStmt(self, node: ReturnStmt):
        node.value = node.value.accept(self)
        return node

    def visitWhileStmt(self, node: WhileStmt):
        node.condition = node.condition.accept(self)
        node.body = node.body.accept(self)
        return node

    def visitMatchStmt(self, node: MatchStmt):
        node.expr = node.expr.accept(self)
        node.arms = [i.accept(self) for i in node.arms]
        return node

    def visitMatchArm(self, node: MatchArm):
        node.patterns = [i.accept(self) for i in node.patterns]
        node.body = node.body.accept(self)
        return node

    def visitMatchPattern(self, node: MatchPattern):
        node.value = node.value.accept(self)
        return node

    def visitCompoundAssignment(self, node: CompoundAssignment):
        node.target = node.target.accept(self)
        node.value = node.value.accept(self)
        return node

    def visitLoopStmt(self, node: LoopStmt):
        node.body = node.body.accept(self)
        return node

    def visitBreakStmt(self, node: BreakStmt):
        node.stmts = [i.accept(self) for i in node.stmts]
        return node

    def visitContinueStmt(self, node: ContinueStmt):
        pass
        # node.value.accept(self)

    # def visitFunctionCallExpression(self, node: FunctionCallExpression):
    #     print("visitFunctionCallExpression0")
    #     retval = True
    #     if node.args():
    #         for arg in node.args():
    #             retval = arg.accept(self) and retval
    #     return retval
    def visitFunctionCallExpression(self, node):
        """Safely traverse function call arguments and preserve the AST node."""
        # print("visitFunctionCallExpression0")
        
        callee = node.callee() if callable(getattr(node, "callee", None)) else getattr(node, "callee", None)
        if callee is not None:
            self.visit(callee)

        args = node.args() if callable(getattr(node, "args", None)) else getattr(node, "args", None)
        if args:
            for arg in args:
                # Route through self.visit to catch primitives and avoid .accept() traps
                self.visit(arg)

        return node

    def visitBlock(self, node: Block):
            node.stmts = [stmt.accept(self) for stmt in node.stmts]
            return node
            
    # def visitInitBlock(self, node: InitBlock):
    #     node.returnExpr.accept(self)

    def visitQualifiedExpression(self, node: QualifiedExpression):
        return node.expression().accept(self)

    def visitIdentifierExpression(self, node: IdentifierExpression):
        return node

    # def visitBinaryExpression(self, node: BinaryExpression):
    #     print("visitBinaryExpression")
    #     retval = node.left().accept(self)
    #     retval = node.right().accept(self) and retval
    #     return retval
    def visitBinaryExpression(self, node: BinaryExpression):
        # print("visitBinaryExpression")
        
        left_child = node.left()
        if hasattr(left_child, "accept"):
            left_child.accept(self)
        elif left_child is not None:
            self.visit(left_child)

        right_child = node.right()
        if hasattr(right_child, "accept"):
            right_child.accept(self)
        elif right_child is not None:
            self.visit(right_child)

        return node

    def visitByteLiteralExpression(self, node: ByteLiteralExpression):
        return node

    def visitTypeWrapper(self, node: TypeWrapper):
        node.expr.accept(self)

    # def visitBoxWrapperExpr(self, node: BoxWrapperExpr):
    #     node.expr.accept(self)
    #     node.path.accept(self)

    # def visitBorrowExpression(self, ctx: BorrowExpression):
    #     ctx.expression().accept(self)
    def visitBorrowExpression(self, node):
        """Safely traverse borrow expressions without calling properties as functions."""
        # Check if expression is a method or a property
        expr = node.expression() if callable(getattr(node, "expression", None)) else getattr(node, "expression", None)
        
        if hasattr(expr, "accept"):
            expr.accept(self)
        elif expr is not None:
            self.visit(expr)
            
        return node

    def visitFieldAccessExpr(self, node: FieldAccessExpr):
        """Base traversal for field access expressions (e.g., receiver.field_name)."""        
        if hasattr(node.receiver, "accept"):
            node.receiver.accept(self)
        elif node.receiver is not None:
            self.visit(node.receiver)

        if hasattr(node.name, "accept"):
            node.name.accept(self)
        elif node.name is not None:
            self.visit(node.name)

        return node

    # def visitReferenceExpr(self, node: Ref):
    #     node.expr.accept(self)

    # def visitArrayLiteral(self, node: ArrayLiteral):
    #     for i in node.elements:
    #         i.accept(self)

    def visitIntLiteral(self, node: IntLiteral):
        # node.accept(self)
        return node
    
    def visitStrLiteral(self, node: StrLiteral):
        return node

    def visitCastExpression(self, ctx: CastExpression):
        ctx.expr.accept(self)
        ctx.type.accept(self)

    def visitUnaryExpr(self, node: UnaryExpr):
        node.expr.accept(self)

    def visitDereferenceExpr(self, node: DereferenceExpr):
        node.expr.accept(self)

    def visitParenExpr(self, node: ParenExpr):
        node.inner_expr.accept(self)

    # def visitRangeExpression(self, node: RangeExpression):
    #     node.initial.accept(self)
    #     node.last.accept(self)
    def visitRangeExpression(self, node: RangeExpression):
        if hasattr(node.initial, "accept"):
            node.initial.accept(self)
        elif node.initial is not None:
            self.visit(node.initial)

        if hasattr(node.last, "accept"):
            node.last.accept(self)
        elif node.last is not None:
            self.visit(node.last)

        return node

    def visitArrayLiteral(self, node: ArrayLiteral):
        if node.elements:
            for i in node.elements:
                if hasattr(i, "accept"):
                    i.accept(self)
                elif i is not None:
                    self.visit(i)

        return node

    def visitSafeWrapper(self, node: SafeWrapper):
        node.expr.accept(self)
        # node.last.accept(self)

    def visitBlockStmt(self, node: BlockStmt):
        for i in node.stmts:
            i.accept(self)

    def visitVarDef(self, node: VarDef):
        node.accept(self)

    def visitTypePath(self, node: TypePath):
        return node

    def visitSignedIntType(self, node: SignedIntType):
        return node

    def visitUnsignedIntType(self, node: UnsignedIntType):
        return node

    def visitFloatingPointType(self, node: FloatingPointType):
        return node

    def visitBoolType(self, node: BoolType):
        return node

    def visitCharType(self, node: CharType):
        return node

    def visitStringType(self, node: StringType):
        return node

    def visitSafeNonNullWrapper(self, node: SafeNonNullWrapper):
        return node.dtype.accept(self)

    def visitArrayType(self, node: ArrayType):
        return node.dtype.accept(self)

    def visitArrayAccess(self, node: ArrayAccess):
        print(node.name)
        return node.name.accept(self)

    def visitPathType(self, node: PathType):
        retval = node.type_path.accept(self)
        retval = node.dtype.accept(self) and retval
        return retval

    def visitGenericType(self, node: GenericType):
        retval = node.type_path.accept(self) if node.type_path else True
        for generic_dtype in node.generic_dtypes:
            retval = generic_dtype.accept(self) and retval

        return retval

    def visitReferenceType(self, node: ReferenceType):
        return node.dtype.accept(self)

    def visitSliceType(self, node: SliceType):
        return node.dtype.accept(self)

    def visitUnknownType(self, node: UnknownType):
        return node

    def visitPointerType(self, node: PointerType):
        return node.dtype.accept(self)

    def visitVarDef(self, node: VarDef):
        return node
    
