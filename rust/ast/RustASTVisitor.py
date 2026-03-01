from rust.ast.ASTNode import *
from rust.ast.Func import FunctionParamList, Param
from rust.ast.TopLevel import *
from rust.ast.Block import *
from rust.ast.utils import *


class RustASTVisitor:

    def visit(self, ctx):
        match ctx:
            case Program():
                return self.visitProgram(ctx)
            case FunctionDef():
                return self.visitFunctionDef(ctx)
            case FunctionParamList():
                return self.visitFunctionParamList(ctx)
            case Param():
                return self.visitParam(ctx)
            case StructDef():
                return self.visitStructDef(ctx)
            case StructField():
                return self.visitStructField(ctx)
            case LetStmt():
                return self.visitLetStmt(ctx)
            case ForStmt():
                return self.visitForStmt(ctx)
            case IfStmt():
                return self.visitIfStmt(ctx)
            case AssignStmt():
                return self.visitAssignStmt(ctx)
            case ReturnStmt():
                return self.visitReturnStmt(ctx)
            case WhileStmt():
                return self.visitWhileStmt(ctx)
            case MatchStmt():
                return self.visitMatchStmt(ctx)
            case MatchArm():
                return self.visitMatchArm(ctx)
            case MatchPattern():
                return self.visitMatchPattern(ctx)
            case CompoundAssignment():
                return self.visitCompoundAssignment(ctx)
            # case ExpressionStmt():
            #     return self.visitExpressionStmt(ctx)
            case LoopStmt():
                return self.visitLoopStmt(ctx)
            case BreakStmt():
                return self.visitBreakStmt(ctx)
            case ContinueStmt():
                return self.visitContinueStmt(ctx)
            # case CallStmt():
            #     return self.visitCallStmt(ctx)
            # case UnsafeBlock():
            #     return self.visitUnsafeBlock(ctx)
            case Block():
                return self.visitBlock(ctx)
            # case InitBlock():
            #     return self.visitInitBlock(ctx)
            # case MutableExpr():
            #     return self.visitMutableExpr(ctx)
            case QualifiedExpression():
                return self.visitQualifiedExpression(ctx)
            case IdentifierExpression():
                return self.visitIdentifierExpr(ctx)
            case BinaryExpression():
                return self.visitBinaryExpr(ctx)
            case FunctionCallExpression():
                return self.visitFunctionCallExpression(ctx)
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
            case BorrowExpr():
                return self.visitBorrowExpr(ctx)
            # case VariableRef():
            #     return self.visitVariableRef(ctx)
            # case ReferenceExpr():
            #     return self.visitReferenceExpr(ctx)
            case ArrayLiteral():
                return self.visitArrayLiteral(ctx)
            case CastExpression():
                return self.visitCastExpression(ctx)
            case UnaryExpr():
                return self.visitUnaryExpr(ctx)
            # case MethodCallExpr():
            #     return self.visitMethodCallExpr(ctx)
            case DereferenceExpr():
                return self.visitDereferenceExpr(ctx)
            # case IndexExpr():
            #     return self.visitIndexExpr(ctx)
            case ParenExpr():
                return self.visitParenExpr(ctx)
            case RangeExpression():
                return self.visitRangeExpression(ctx)
            case SafeWrapper():
                return self.visitSafeWrapper(ctx)
            case _:
                raise NotImplementedError(f"No visit method defined for {type(ctx)}")

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
            self.visit(i)

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
        for i in node.args:
            i.accept(self)

    def visitBlock(self, node: Block):
        for i in node.stmts:
            i.accept(self)

    # def visitInitBlock(self, node: InitBlock):
    #     node.returnExpr.accept(self)

    def visitQualifiedExpression(self, node: QualifiedExpression):
        node.inner_expr.accept(self)

    def visitIdentifierExpr(self, node: IdentifierExpression):
        pass

    def visitBinaryExpr(self, node: BinaryExpression):
        node.left.accept(self)
        node.right.accept(self)

    def visitByteLiteralExpression(self, ctx: ByteLiteralExpression):
        pass

    def visitTypeWrapper(self, node: TypeWrapper):
        node.expr.accept(self)

    # def visitBoxWrapperExpr(self, node: BoxWrapperExpr):
    #     node.expr.accept(self)
    #     node.path.accept(self)

    def visitBorrowExpr(self, node: BorrowExpr):
        node.expr.accept(self)

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
