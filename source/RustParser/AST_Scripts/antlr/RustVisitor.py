# Generated from Rust.g4 by ANTLR 4.13.2
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

    # Visit a parse tree produced by RustParser#structDef.
    def visitStructDef(self, ctx:RustParser.StructDefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RustParser#structField.
    def visitStructField(self, ctx:RustParser.StructFieldContext):
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


    # Visit a parse tree produced by RustParser#referenceType.
    def visitReferenceType(self, ctx:RustParser.ReferenceTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RustParser#type.
    def visitType(self, ctx:RustParser.TypeContext):
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


    # Visit a parse tree produced by RustParser#letStmt.
    def visitLetStmt(self, ctx:RustParser.LetStmtContext):
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


    # Visit a parse tree produced by RustParser#expression.
    def visitExpression(self, ctx:RustParser.ExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RustParser#primaryExpression.
    def visitPrimaryExpression(self, ctx:RustParser.PrimaryExpressionContext):
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


    # Visit a parse tree produced by RustParser#attribute.
    def visitAttribute(self, ctx:RustParser.AttributeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RustParser#attrInner.
    def visitAttrInner(self, ctx:RustParser.AttrInnerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RustParser#literal.
    def visitLiteral(self, ctx:RustParser.LiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RustParser#arrayLiteral.
    def visitArrayLiteral(self, ctx:RustParser.ArrayLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RustParser#stringLiteral.
    def visitStringLiteral(self, ctx:RustParser.StringLiteralContext):
        return self.visitChildren(ctx)



del RustParser