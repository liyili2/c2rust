from rust.ast.Expression import QualifiedExpression, IdentifierExpression, BinaryExpression, FunctionCallExpression, \
    BorrowExpression, ArrayLiteral, CastExpression, UnaryExpr, DereferenceExpr, ParenExpr, RangeExpression, SafeWrapper, \
    ByteLiteralExpression
from rust.ast.Func import FunctionParamList, Param
from rust.ast.Program import Program
from rust.ast.Statement import LetStmt, ForStmt, IfStmt, AssignStmt, ReturnStmt, WhileStmt, MatchStmt, MatchArm, \
    MatchPattern, CompoundAssignment, LoopStmt, BreakStmt, ContinueStmt, TypeWrapper
from rust.ast.Struct import StructField
from rust.ast.TopLevel import *
from rust.ast.Block import *
from rust.ast.ASTNode import ASTNode


class RustASTVisitor:

    def visit(self, node: ASTNode):
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
            case _:
                raise NotImplementedError(f"No visit method defined for {type(node)}")

    def visitProgram(self, ctx: Program):
        ret = False
        for exp in ctx.getChildren():
            ret = ret and exp.accept(self)

        return ret

    def visitFunctionDef(self, ctx: FunctionDef):
        ret = ctx.params.accept(self)
        ret = ret and ctx.body.accept(self)
        ret = ret and ctx.return_type.accept(self)

        return ret

    def visitFunctionParamList(self, ctx: FunctionParamList):
        ret = True
        for param in ctx.params:
            ret = ret and param.accept(self)

        return ret

    def visitParam(self, ctx: Param):
        return True

    def visitStructDef(self, ctx: StructDef):
        ret = True
        for child in ctx.getChildren():
            self.visit(child)

    def visitStructField(self, node: StructField):
        # mut = "mut " if node.mutable else ""
        self.visit(node.dtype)

    def visitLetStmt(self, node: LetStmt):
        for i in node.var_defs:
            i.accept(self)
        for i in node.values:
            i.accept(self)

    def visitForStmt(self, node: ForStmt):
        node.iterable.accept(self)
        node.body.accept(self)

    def visitIfStmt(self, node: IfStmt):
        node.condition.accept(self)
        node.then_branch.accept(self)
        if node.else_branch is not None:
            node.else_branch.accept(self)

    def visitAssignStmt(self, node: AssignStmt):
        node.target.accept(self)
        node.value.accept(self)

    def visitReturnStmt(self, node: ReturnStmt):
        node.value.accept(self)

    def visitWhileStmt(self, node: WhileStmt):
        node.condition.accept(self)
        node.body.accept(self)

    def visitMatchStmt(self, node: MatchStmt):
        node.expr.accept(self)
        for i in node.arms:
            i.accept(self)

    def visitMatchArm(self, node: MatchArm):
        for i in node.patterns:
            i.accept(self)
        node.body.accept(self)

    def visitMatchPattern(self, node: MatchPattern):
        node.value.accept(self)

    def visitCompoundAssignment(self, node: CompoundAssignment):
        node.target.accept(self)
        node.value.accept(self)

    def visitLoopStmt(self, node: LoopStmt):
        node.body.accept(self)
        # node.value.accept(self)

    def visitBreakStmt(self, node: BreakStmt):
        pass
        # node.value.accept(self)

    def visitContinueStmt(self, node: ContinueStmt):
        pass
        # node.value.accept(self)

    def visitFunctionCallExpression(self, node: FunctionCallExpression):
        retval = True
        for arg in node.args():
            retval = retval and arg.accept(self)

        return retval

    def visitBlock(self, node: Block):
        for i in node.stmts:
            i.accept(self)

    # def visitInitBlock(self, node: InitBlock):
    #     node.returnExpr.accept(self)

    def visitQualifiedExpression(self, ctx: QualifiedExpression):
        return ctx.expression().accept(self)

    def visitIdentifierExpression(self, ctx: IdentifierExpression):
        return True

    def visitBinaryExpression(self, node: BinaryExpression):
        return node.left().accept(self) and node.right().accept(self)

    def visitByteLiteralExpression(self, node: ByteLiteralExpression):
        return True

    def visitTypeWrapper(self, node: TypeWrapper):
        node.expr.accept(self)

    # def visitBoxWrapperExpr(self, node: BoxWrapperExpr):
    #     node.expr.accept(self)
    #     node.path.accept(self)

    def visitBorrowExpression(self, ctx: BorrowExpression):
        ctx.expression().accept(self)

    # def visitReferenceExpr(self, node: Ref):
    #     node.expr.accept(self)

    def visitArrayLiteral(self, node: ArrayLiteral):
        for i in node.elements:
            i.accept(self)

    def visitCastExpression(self, ctx: CastExpression):
        ctx.expr.accept(self)
        ctx.type.accept(self)

    def visitUnaryExpr(self, node: UnaryExpr):
        node.expr.accept(self)

    def visitDereferenceExpr(self, node: DereferenceExpr):
        node.expr.accept(self)

    def visitParenExpr(self, node: ParenExpr):
        node.inner_expr.accept(self)

    def visitRangeExpression(self, node: RangeExpression):
        node.initial.accept(self)
        node.last.accept(self)

    def visitSafeWrapper(self, node: SafeWrapper):
        node.expr.accept(self)
        # node.last.accept(self)
