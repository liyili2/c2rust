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


    # Visit a parse tree produced by RustParser#typeAlias.
    def visitTypeAlias(self, ctx:RustParser.TypeAliasContext):
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


    # Visit a parse tree produced by RustParser#structDef.
    def visitStructDef(self, ctx:RustParser.StructDefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RustParser#structField.
    def visitStructField(self, ctx:RustParser.StructFieldContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RustParser#functionDef.
    def visitFunctionDef(self, ctx:RustParser.FunctionDefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RustParser#unsafeModifier.
    def visitUnsafeModifier(self, ctx:RustParser.UnsafeModifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RustParser#externAbi.
    def visitExternAbi(self, ctx:RustParser.ExternAbiContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RustParser#paramList.
    def visitParamList(self, ctx:RustParser.ParamListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RustParser#param.
    def visitParam(self, ctx:RustParser.ParamContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RustParser#constDef.
    def visitConstDef(self, ctx:RustParser.ConstDefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RustParser#unionDef.
    def visitUnionDef(self, ctx:RustParser.UnionDefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RustParser#unionField.
    def visitUnionField(self, ctx:RustParser.UnionFieldContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RustParser#unsafeDef.
    def visitUnsafeDef(self, ctx:RustParser.UnsafeDefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RustParser#referenceType.
    def visitReferenceType(self, ctx:RustParser.ReferenceTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RustParser#type.
    def visitType(self, ctx:RustParser.TypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RustParser#typePath.
    def visitTypePath(self, ctx:RustParser.TypePathContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RustParser#pointerType.
    def visitPointerType(self, ctx:RustParser.PointerTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RustParser#basicType.
    def visitBasicType(self, ctx:RustParser.BasicTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RustParser#block.
    def visitBlock(self, ctx:RustParser.BlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RustParser#statement.
    def visitStatement(self, ctx:RustParser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RustParser#whileStmt.
    def visitWhileStmt(self, ctx:RustParser.WhileStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RustParser#staticVarDecl.
    def visitStaticVarDecl(self, ctx:RustParser.StaticVarDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RustParser#initializer.
    def visitInitializer(self, ctx:RustParser.InitializerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RustParser#letStmt.
    def visitLetStmt(self, ctx:RustParser.LetStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RustParser#varDef.
    def visitVarDef(self, ctx:RustParser.VarDefContext):
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


    # Visit a parse tree produced by RustParser#expression.
    def visitExpression(self, ctx:RustParser.ExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RustParser#expressionBlock.
    def visitExpressionBlock(self, ctx:RustParser.ExpressionBlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RustParser#borrowExpression.
    def visitBorrowExpression(self, ctx:RustParser.BorrowExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RustParser#postfixExpression.
    def visitPostfixExpression(self, ctx:RustParser.PostfixExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RustParser#primaryExpression.
    def visitPrimaryExpression(self, ctx:RustParser.PrimaryExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RustParser#qualifiedFunctionCall.
    def visitQualifiedFunctionCall(self, ctx:RustParser.QualifiedFunctionCallContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RustParser#genericArgs.
    def visitGenericArgs(self, ctx:RustParser.GenericArgsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RustParser#structLiteralField.
    def visitStructLiteralField(self, ctx:RustParser.StructLiteralFieldContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RustParser#matchArm.
    def visitMatchArm(self, ctx:RustParser.MatchArmContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RustParser#matchPattern.
    def visitMatchPattern(self, ctx:RustParser.MatchPatternContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RustParser#argumentList.
    def visitArgumentList(self, ctx:RustParser.ArgumentListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RustParser#macroCall.
    def visitMacroCall(self, ctx:RustParser.MacroCallContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RustParser#macroArgs.
    def visitMacroArgs(self, ctx:RustParser.MacroArgsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RustParser#macroInner.
    def visitMacroInner(self, ctx:RustParser.MacroInnerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RustParser#literal.
    def visitLiteral(self, ctx:RustParser.LiteralContext):
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