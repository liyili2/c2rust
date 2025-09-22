# Generated from Rust.g4 by ANTLR 4.13.1
from antlr4 import *
if "." in __name__:
    from .RustParser import RustParser
else:
    from RustParser import RustParser

# This class defines a complete generic visitor for a parse tree produced by RustParser.

class RustVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by RustParser#program.
    def visitProgram(self, ctx:RustParser.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RustParser#topLevelItem.
    def visitTopLevelItem(self, ctx:RustParser.TopLevelItemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RustParser#useDecl.
    def visitUseDecl(self, ctx:RustParser.UseDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RustParser#topLevelDef.
    def visitTopLevelDef(self, ctx:RustParser.TopLevelDefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RustParser#topLevelVarDef.
    def visitTopLevelVarDef(self, ctx:RustParser.TopLevelVarDefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RustParser#defKind.
    def visitDefKind(self, ctx:RustParser.DefKindContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RustParser#varDefField.
    def visitVarDefField(self, ctx:RustParser.VarDefFieldContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RustParser#typeAlias.
    def visitTypeAlias(self, ctx:RustParser.TypeAliasContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RustParser#interfaceDef.
    def visitInterfaceDef(self, ctx:RustParser.InterfaceDefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RustParser#externBlock.
    def visitExternBlock(self, ctx:RustParser.ExternBlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RustParser#externItem.
    def visitExternItem(self, ctx:RustParser.ExternItemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RustParser#externParams.
    def visitExternParams(self, ctx:RustParser.ExternParamsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RustParser#externParam.
    def visitExternParam(self, ctx:RustParser.ExternParamContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RustParser#visibility.
    def visitVisibility(self, ctx:RustParser.VisibilityContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RustParser#unsafeModifier.
    def visitUnsafeModifier(self, ctx:RustParser.UnsafeModifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RustParser#externAbi.
    def visitExternAbi(self, ctx:RustParser.ExternAbiContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RustParser#attributes.
    def visitAttributes(self, ctx:RustParser.AttributesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RustParser#innerAttribute.
    def visitInnerAttribute(self, ctx:RustParser.InnerAttributeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RustParser#attribute.
    def visitAttribute(self, ctx:RustParser.AttributeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RustParser#attrArgs.
    def visitAttrArgs(self, ctx:RustParser.AttrArgsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RustParser#attrArg.
    def visitAttrArg(self, ctx:RustParser.AttrArgContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RustParser#attrValue.
    def visitAttrValue(self, ctx:RustParser.AttrValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RustParser#structDef.
    def visitStructDef(self, ctx:RustParser.StructDefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RustParser#structField.
    def visitStructField(self, ctx:RustParser.StructFieldContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RustParser#structLiteral.
    def visitStructLiteral(self, ctx:RustParser.StructLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RustParser#structLiteralField.
    def visitStructLiteralField(self, ctx:RustParser.StructLiteralFieldContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RustParser#functionDef.
    def visitFunctionDef(self, ctx:RustParser.FunctionDefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RustParser#paramList.
    def visitParamList(self, ctx:RustParser.ParamListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RustParser#param.
    def visitParam(self, ctx:RustParser.ParamContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RustParser#typeExpr.
    def visitTypeExpr(self, ctx:RustParser.TypeExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RustParser#pointerType.
    def visitPointerType(self, ctx:RustParser.PointerTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RustParser#basicType.
    def visitBasicType(self, ctx:RustParser.BasicTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RustParser#safeNonNullWrapper.
    def visitSafeNonNullWrapper(self, ctx:RustParser.SafeNonNullWrapperContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RustParser#typePath.
    def visitTypePath(self, ctx:RustParser.TypePathContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RustParser#arrayType.
    def visitArrayType(self, ctx:RustParser.ArrayTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RustParser#block.
    def visitBlock(self, ctx:RustParser.BlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RustParser#unsafeBlcok.
    def visitUnsafeBlcok(self, ctx:RustParser.UnsafeBlcokContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RustParser#statement.
    def visitStatement(self, ctx:RustParser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RustParser#conditionalAssignmentStmt.
    def visitConditionalAssignmentStmt(self, ctx:RustParser.ConditionalAssignmentStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RustParser#callStmt.
    def visitCallStmt(self, ctx:RustParser.CallStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RustParser#letStmt.
    def visitLetStmt(self, ctx:RustParser.LetStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RustParser#varDef.
    def visitVarDef(self, ctx:RustParser.VarDefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RustParser#compoundOp.
    def visitCompoundOp(self, ctx:RustParser.CompoundOpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RustParser#compoundAssignment.
    def visitCompoundAssignment(self, ctx:RustParser.CompoundAssignmentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RustParser#matchStmt.
    def visitMatchStmt(self, ctx:RustParser.MatchStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RustParser#matchArm.
    def visitMatchArm(self, ctx:RustParser.MatchArmContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RustParser#matchPattern.
    def visitMatchPattern(self, ctx:RustParser.MatchPatternContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RustParser#whileStmt.
    def visitWhileStmt(self, ctx:RustParser.WhileStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RustParser#initializer.
    def visitInitializer(self, ctx:RustParser.InitializerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RustParser#staticVarDecl.
    def visitStaticVarDecl(self, ctx:RustParser.StaticVarDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RustParser#initBlock.
    def visitInitBlock(self, ctx:RustParser.InitBlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RustParser#assignStmt.
    def visitAssignStmt(self, ctx:RustParser.AssignStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RustParser#forStmt.
    def visitForStmt(self, ctx:RustParser.ForStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RustParser#ifStmt.
    def visitIfStmt(self, ctx:RustParser.IfStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RustParser#exprStmt.
    def visitExprStmt(self, ctx:RustParser.ExprStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RustParser#returnStmt.
    def visitReturnStmt(self, ctx:RustParser.ReturnStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RustParser#loopStmt.
    def visitLoopStmt(self, ctx:RustParser.LoopStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RustParser#safeWrapper.
    def visitSafeWrapper(self, ctx:RustParser.SafeWrapperContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RustParser#expression.
    def visitExpression(self, ctx:RustParser.ExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RustParser#basicTypeCastExpr.
    def visitBasicTypeCastExpr(self, ctx:RustParser.BasicTypeCastExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RustParser#unsafeExpression.
    def visitUnsafeExpression(self, ctx:RustParser.UnsafeExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RustParser#qualifiedExpression.
    def visitQualifiedExpression(self, ctx:RustParser.QualifiedExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RustParser#structDefInit.
    def visitStructDefInit(self, ctx:RustParser.StructDefInitContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RustParser#arrayDeclaration.
    def visitArrayDeclaration(self, ctx:RustParser.ArrayDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RustParser#typePathExpression.
    def visitTypePathExpression(self, ctx:RustParser.TypePathExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RustParser#patternPrefix.
    def visitPatternPrefix(self, ctx:RustParser.PatternPrefixContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RustParser#pattern.
    def visitPattern(self, ctx:RustParser.PatternContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RustParser#castExpressionPostFix.
    def visitCastExpressionPostFix(self, ctx:RustParser.CastExpressionPostFixContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RustParser#compoundOps.
    def visitCompoundOps(self, ctx:RustParser.CompoundOpsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RustParser#rangeSymbol.
    def visitRangeSymbol(self, ctx:RustParser.RangeSymbolContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RustParser#binaryOps.
    def visitBinaryOps(self, ctx:RustParser.BinaryOpsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RustParser#binaryExpression.
    def visitBinaryExpression(self, ctx:RustParser.BinaryExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RustParser#structFieldDec.
    def visitStructFieldDec(self, ctx:RustParser.StructFieldDecContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RustParser#unaryOpes.
    def visitUnaryOpes(self, ctx:RustParser.UnaryOpesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RustParser#parenExpression.
    def visitParenExpression(self, ctx:RustParser.ParenExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RustParser#dereferenceExpression.
    def visitDereferenceExpression(self, ctx:RustParser.DereferenceExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RustParser#expressionBlock.
    def visitExpressionBlock(self, ctx:RustParser.ExpressionBlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RustParser#borrowExpression.
    def visitBorrowExpression(self, ctx:RustParser.BorrowExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RustParser#primaryExpression.
    def visitPrimaryExpression(self, ctx:RustParser.PrimaryExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RustParser#fieldAccessPostFix.
    def visitFieldAccessPostFix(self, ctx:RustParser.FieldAccessPostFixContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RustParser#callExpressionPostFix.
    def visitCallExpressionPostFix(self, ctx:RustParser.CallExpressionPostFixContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RustParser#functionCallArgs.
    def visitFunctionCallArgs(self, ctx:RustParser.FunctionCallArgsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RustParser#literal.
    def visitLiteral(self, ctx:RustParser.LiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RustParser#byteLiteral.
    def visitByteLiteral(self, ctx:RustParser.ByteLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RustParser#booleanLiteral.
    def visitBooleanLiteral(self, ctx:RustParser.BooleanLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RustParser#arrayLiteral.
    def visitArrayLiteral(self, ctx:RustParser.ArrayLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RustParser#stringLiteral.
    def visitStringLiteral(self, ctx:RustParser.StringLiteralContext):
        return self.visitChildren(ctx)



del RustParser