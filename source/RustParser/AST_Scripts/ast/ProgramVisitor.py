
from RustParser.AST_Scripts.ast.ASTNode import ASTNode
from RustParser.AST_Scripts.ast.Expression import ArrayDeclaration, ArrayLiteral, BasicTypeCastExpr, BinaryExpr, BoolLiteral, BorrowExpr, BoxWrapperExpr, CastExpr, CharLiteral, CharLiteralExpr, DereferenceExpr, FieldAccessExpr, FunctionCallExpr, IdentifierExpr, IndexExpr, IntLiteral, MethodCallExpr, MutableExpr, ParenExpr, Pattern, PatternExpr, QualifiedExpression, RangeExpression, RepeatArrayLiteral, SafeWrapper, StrLiteral, StructDefInit, StructLiteralExpr, StructLiteralField, TypeAccessExpr, TypePathExpression, TypePathFullExpr, TypeWrapperExpr, UnaryExpr, UnsafeExpression
from RustParser.AST_Scripts.ast.Statement import AssignStmt, BreakStmt, CallStmt, CompoundAssignment, ConditionalAssignmentStmt, ContinueStmt, ExpressionStmt, ForStmt, IfStmt, LetStmt, LoopStmt, MatchArm, MatchPattern, MatchStmt, ReturnStmt, StructLiteral, TypeWrapper, UnsafeBlock, WhileStmt
#from RustParser.AST_Scripts.antlr.RustVisitor import RustVisitor
from RustParser.AST_Scripts.ast.TopLevel import StaticVarDecl, ExternBlock, ExternFunctionDecl, ExternStaticVarDecl, ExternTypeDecl, FunctionDef, InterfaceDef, StructDef, Attribute, StructField, TopLevel, TopLevelVarDef, TypeAliasDecl, UseDecl, VarDefField
from RustParser.AST_Scripts.ast.Program import Program
from RustParser.AST_Scripts.ast.Expression import LiteralExpr
from RustParser.AST_Scripts.ast.Type import SafeNonNullWrapper, ArrayType, BoolType, IntType, PathType, PointerType, StringType, Type
#from RustParser.AST_Scripts.antlr import RustLexer, RustParser
from RustParser.AST_Scripts.ast.VarDef import VarDef
#from RustParser.AST_Scripts.antlr import RustParser
from RustParser.AST_Scripts.ast.Block import Block, InitBlock
from RustParser.AST_Scripts.ast.Func import FunctionParamList, Param

class ProgramVisitor:

    def visit(self, ctx):
        match ctx:
            case Program():
                return self.visitProgram(ctx)
            case FunctionDef():
                return self.visitFunctionDef(ctx)
            case StructDef():
                return self.visitStructDef(ctx)
            case StructField():
                return self.visitStructDef(ctx)
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
            case ExpressionStmt():
                return self.visitExpressionStmt(ctx)
            case LoopStmt():
                return self.visitLoopStmt(ctx)
            case BreakStmt():
                return self.visitBreakStmt(ctx)
            case ContinueStmt():
                return self.visitContinueStmt(ctx)
            case CallStmt():
                return self.visitCallStmt(ctx)
            case UnsafeBlock():
                return self.visitUnsafeBlock(ctx)
            case Block():
                return self.visitBlock(ctx)
            case InitBlock():
                return self.visitInitBlock(ctx)
            case MutableExpr():
                return self.visitMutableExpr(ctx)
            case QualifiedExpression():
                return self.visitQualifiedExpression(ctx)
            case IdentifierExpr():
                return self.visitIdentifierExpr(ctx)
            case BinaryExpr():
                return self.visitBinaryExpr(ctx)
            case LiteralExpr():
                return self.visitLiteralExpr(ctx)
            case FunctionCallExpr():
                return self.visitFunctionCallExpr(ctx)
            case UnsafeExpression():
                return self.visitUnsafeExpression(ctx)
            case BasicTypeCastExpr():
                return self.visitBasicTypeCastExpr(ctx)
            case TypeAccessExpr():
                return self.visitTypeAccessExpr(ctx)
            case TypeWrapperExpr():
                return self.visitTypeWrapperExpr(ctx)
            case BoxWrapperExpr():
                return self.visitBoxWrapperExpr(ctx)
            case BorrowExpr():
                return self.visitBorrowExpr(ctx)
            case VariableRef():
                return self.visitVariableRef(ctx)
            case ReferenceExpr():
                return self.visitReferenceExpr(ctx)
            case ArrayLiteral():
                return self.visitArrayLiteral(ctx)
            case CastExpr():
                return self.visitCastExpr(ctx)
            case UnaryExpr():
                return self.visitUnaryExpr(ctx)
            case MethodCallExpr():
                return self.visitMethodCallExpr(ctx)
            case DereferenceExpr():
                return self.visitDereferenceExpr(ctx)
            case IndexExpr():
                return self.visitIndexExpr(ctx)
            case ParenExpr():
                return self.visitParenExpr(ctx)
            case RangeExpression():
                return self.visitRangeExpression(ctx)
            case SafeWrapper():
                return self.visitSafeWrapper(ctx)
            case _:
                raise NotImplementedError(f"No visit method defined for {type(ctx)}")

    def visitProgram(self, node:Program):
        for i in node.getChildren():
            self.visit(i)

    def visitFunctionDef(self, node:FunctionDef):
        self.visit(node.params)
        self.visit(node.body)
        self.visit(node.return_type)

    def visitStructDef(self, node:StructDef):
        #mut = "mut " if node.mutable else ""
        for i in node.getChildren():
            self.visit(i)

    def visitStructField(self, node:StructField):
        #mut = "mut " if node.mutable else ""
        self.visit(node.type)

    def visitLetStmt(self, node:LetStmt):
        for i in node.var_defs:
            i.accept(self)
        for i in node.values:
            i.accept(self)

    def visitForStmt(self, node:ForStmt):
        node.iterable.accept(self)
        node.body.accept(self)

    def visitIfStmt(self, node:IfStmt):
        node.condition.accept(self)
        node.then_branch.accept(self)
        if node.else_branch is not None:
            node.else_branch.accept(self)

    def visitAssignStmt(self, node:AssignStmt):
        node.target.accept(self)
        node.value.accept(self)

    def visitReturnStmt(self, node:ReturnStmt):
        node.value.accept(self)


    def visitWhileStmt(self, node:WhileStmt):
        node.condition.accept(self)
        node.body.accept(self)

    def visitMatchStmt(self, node:MatchStmt):
        node.expr.accept(self)
        for i in node.arms:
            i.accept(self)

    def visitMatchArm(self, node:MatchArm):
        for i in node.patterns:
            i.accept(self)
        node.body.accept(self)

    def visitMatchPattern(self, node:MatchPattern):
        node.value.accept(self)

    def visitCompoundAssignment(self, node:CompoundAssignment):
        node.target.accept(self)
        node.value.accept(self)

    def visitExpressionStmt(self, node:ExpressionStmt):
        node.expr.accept(self)
        #node.value.accept(self)

    def visitLoopStmt(self, node:LoopStmt):
        node.body.accept(self)
        #node.value.accept(self)

    def visitBreakStmt(self, node:BreakStmt):
        pass
        #node.value.accept(self)

    def visitContinueStmt(self, node:ContinueStmt):
        pass
        #node.value.accept(self)

    def visitCallStmt(self, node: CallStmt):
        for i in node.args:
            i.accept(self)

    def visitUnsafeBlock(self, node: UnsafeBlock):
        for i in node.stmts:
            i.accept(self)

    def visitBlock(self, node: Block):
        for i in node.stmts:
            i.accept(self)

    def visitInitBlock(self, node: InitBlock):
        node.returnExpr.accept(self)

    def visitMutableExpr(self, node: MutableExpr):
        node.expr.accept(self)

    def visitQualifiedExpression(self, node: QualifiedExpression):
        node.inner_expr.accept(self)

    def visitIdentifierExpr(self, node: IdentifierExpr):
        pass

    def visitBinaryExpr(self, node: BinaryExpr):
        node.left.accept(self)
        node.right.accept(self)

    def visitLiteralExpr(self, node: LiteralExpr):
        node.value.accept(self)

    def visitFunctionCallExpr(self, node: FunctionCallExpr):
        for i in node.args:
            i.accept(self)

    def visitUnsafeExpression(self, node: UnsafeExpression):
        node.expr.accept(self)

    def visitBasicTypeCastExpr(self, node: BasicTypeCastExpr):
        node.basicType.accept(self)
        node.typePath.accept(self)

    def visitTypeAccessExpr(self, node: TypeAccessExpr):
        node.expr.accept(self)
        node.type.accept(self)

    def visitTypeWrapperExpr(self, node: TypeWrapperExpr):
        node.expr.accept(self)

    def visitBoxWrapperExpr(self, node: BoxWrapperExpr):
        node.expr.accept(self)
        node.path.accept(self)


    def visitBorrowExpr(self, node: BorrowExpr):
        node.expr.accept(self)

    def visitVariableRef(self, node: VariableRef):
        pass

    def visitReferenceExpr(self, node: ReferenceExpr):
        node.expr.accept(self)

    def visitArrayLiteral(self, node: ArrayLiteral):
        for i in node.elements:
            i.accept(self)

    def visitCastExpr(self, node: CastExpr):
        node.expr.accept(self)
        node.type.accept(self)

    def visitUnaryExpr(self, node: UnaryExpr):
        node.expr.accept(self)


    def visitMethodCallExpr(self, node: MethodCallExpr):
        node.receiver.accept(self)
        for i in node.args:
            i.accept(self)

    def visitDereferenceExpr(self, node: DereferenceExpr):
        node.expr.accept(self)

    def visitIndexExpr(self, node: IndexExpr):
        node.target.accept(self)
        node.index.accept(self)


    def visitParenExpr(self, node: ParenExpr):
        node.inner_expr.accept(self)


    def visitRangeExpression(self, node: RangeExpression):
        node.initial.accept(self)
        node.last.accept(self)

    def visitSafeWrapper(self, node: SafeWrapper):
        node.expr.accept(self)
        #node.last.accept(self)


