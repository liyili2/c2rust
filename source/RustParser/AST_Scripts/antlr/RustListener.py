# Generated from Rust.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .RustParser import RustParser
else:
    from RustParser import RustParser

# This class defines a complete listener for a parse tree produced by RustParser.
class RustListener(ParseTreeListener):

    # Enter a parse tree produced by RustParser#program.
    def enterProgram(self, ctx:RustParser.ProgramContext):
        pass

    # Exit a parse tree produced by RustParser#program.
    def exitProgram(self, ctx:RustParser.ProgramContext):
        pass


    # Enter a parse tree produced by RustParser#topLevelItem.
    def enterTopLevelItem(self, ctx:RustParser.TopLevelItemContext):
        pass

    # Exit a parse tree produced by RustParser#topLevelItem.
    def exitTopLevelItem(self, ctx:RustParser.TopLevelItemContext):
        pass


    # Enter a parse tree produced by RustParser#structDef.
    def enterStructDef(self, ctx:RustParser.StructDefContext):
        pass

    # Exit a parse tree produced by RustParser#structDef.
    def exitStructDef(self, ctx:RustParser.StructDefContext):
        pass


    # Enter a parse tree produced by RustParser#structField.
    def enterStructField(self, ctx:RustParser.StructFieldContext):
        pass

    # Exit a parse tree produced by RustParser#structField.
    def exitStructField(self, ctx:RustParser.StructFieldContext):
        pass


    # Enter a parse tree produced by RustParser#functionDef.
    def enterFunctionDef(self, ctx:RustParser.FunctionDefContext):
        pass

    # Exit a parse tree produced by RustParser#functionDef.
    def exitFunctionDef(self, ctx:RustParser.FunctionDefContext):
        pass


    # Enter a parse tree produced by RustParser#paramList.
    def enterParamList(self, ctx:RustParser.ParamListContext):
        pass

    # Exit a parse tree produced by RustParser#paramList.
    def exitParamList(self, ctx:RustParser.ParamListContext):
        pass


    # Enter a parse tree produced by RustParser#param.
    def enterParam(self, ctx:RustParser.ParamContext):
        pass

    # Exit a parse tree produced by RustParser#param.
    def exitParam(self, ctx:RustParser.ParamContext):
        pass


    # Enter a parse tree produced by RustParser#referenceType.
    def enterReferenceType(self, ctx:RustParser.ReferenceTypeContext):
        pass

    # Exit a parse tree produced by RustParser#referenceType.
    def exitReferenceType(self, ctx:RustParser.ReferenceTypeContext):
        pass


    # Enter a parse tree produced by RustParser#type.
    def enterType(self, ctx:RustParser.TypeContext):
        pass

    # Exit a parse tree produced by RustParser#type.
    def exitType(self, ctx:RustParser.TypeContext):
        pass


    # Enter a parse tree produced by RustParser#basicType.
    def enterBasicType(self, ctx:RustParser.BasicTypeContext):
        pass

    # Exit a parse tree produced by RustParser#basicType.
    def exitBasicType(self, ctx:RustParser.BasicTypeContext):
        pass


    # Enter a parse tree produced by RustParser#block.
    def enterBlock(self, ctx:RustParser.BlockContext):
        pass

    # Exit a parse tree produced by RustParser#block.
    def exitBlock(self, ctx:RustParser.BlockContext):
        pass


    # Enter a parse tree produced by RustParser#statement.
    def enterStatement(self, ctx:RustParser.StatementContext):
        pass

    # Exit a parse tree produced by RustParser#statement.
    def exitStatement(self, ctx:RustParser.StatementContext):
        pass


    # Enter a parse tree produced by RustParser#letStmt.
    def enterLetStmt(self, ctx:RustParser.LetStmtContext):
        pass

    # Exit a parse tree produced by RustParser#letStmt.
    def exitLetStmt(self, ctx:RustParser.LetStmtContext):
        pass


    # Enter a parse tree produced by RustParser#assignStmt.
    def enterAssignStmt(self, ctx:RustParser.AssignStmtContext):
        pass

    # Exit a parse tree produced by RustParser#assignStmt.
    def exitAssignStmt(self, ctx:RustParser.AssignStmtContext):
        pass


    # Enter a parse tree produced by RustParser#forStmt.
    def enterForStmt(self, ctx:RustParser.ForStmtContext):
        pass

    # Exit a parse tree produced by RustParser#forStmt.
    def exitForStmt(self, ctx:RustParser.ForStmtContext):
        pass


    # Enter a parse tree produced by RustParser#ifStmt.
    def enterIfStmt(self, ctx:RustParser.IfStmtContext):
        pass

    # Exit a parse tree produced by RustParser#ifStmt.
    def exitIfStmt(self, ctx:RustParser.IfStmtContext):
        pass


    # Enter a parse tree produced by RustParser#exprStmt.
    def enterExprStmt(self, ctx:RustParser.ExprStmtContext):
        pass

    # Exit a parse tree produced by RustParser#exprStmt.
    def exitExprStmt(self, ctx:RustParser.ExprStmtContext):
        pass


    # Enter a parse tree produced by RustParser#returnStmt.
    def enterReturnStmt(self, ctx:RustParser.ReturnStmtContext):
        pass

    # Exit a parse tree produced by RustParser#returnStmt.
    def exitReturnStmt(self, ctx:RustParser.ReturnStmtContext):
        pass


    # Enter a parse tree produced by RustParser#expression.
    def enterExpression(self, ctx:RustParser.ExpressionContext):
        pass

    # Exit a parse tree produced by RustParser#expression.
    def exitExpression(self, ctx:RustParser.ExpressionContext):
        pass


    # Enter a parse tree produced by RustParser#primaryExpression.
    def enterPrimaryExpression(self, ctx:RustParser.PrimaryExpressionContext):
        pass

    # Exit a parse tree produced by RustParser#primaryExpression.
    def exitPrimaryExpression(self, ctx:RustParser.PrimaryExpressionContext):
        pass


    # Enter a parse tree produced by RustParser#argumentList.
    def enterArgumentList(self, ctx:RustParser.ArgumentListContext):
        pass

    # Exit a parse tree produced by RustParser#argumentList.
    def exitArgumentList(self, ctx:RustParser.ArgumentListContext):
        pass


    # Enter a parse tree produced by RustParser#macroCall.
    def enterMacroCall(self, ctx:RustParser.MacroCallContext):
        pass

    # Exit a parse tree produced by RustParser#macroCall.
    def exitMacroCall(self, ctx:RustParser.MacroCallContext):
        pass


    # Enter a parse tree produced by RustParser#macroArgs.
    def enterMacroArgs(self, ctx:RustParser.MacroArgsContext):
        pass

    # Exit a parse tree produced by RustParser#macroArgs.
    def exitMacroArgs(self, ctx:RustParser.MacroArgsContext):
        pass


    # Enter a parse tree produced by RustParser#macroInner.
    def enterMacroInner(self, ctx:RustParser.MacroInnerContext):
        pass

    # Exit a parse tree produced by RustParser#macroInner.
    def exitMacroInner(self, ctx:RustParser.MacroInnerContext):
        pass


    # Enter a parse tree produced by RustParser#attribute.
    def enterAttribute(self, ctx:RustParser.AttributeContext):
        pass

    # Exit a parse tree produced by RustParser#attribute.
    def exitAttribute(self, ctx:RustParser.AttributeContext):
        pass


    # Enter a parse tree produced by RustParser#attrInner.
    def enterAttrInner(self, ctx:RustParser.AttrInnerContext):
        pass

    # Exit a parse tree produced by RustParser#attrInner.
    def exitAttrInner(self, ctx:RustParser.AttrInnerContext):
        pass


    # Enter a parse tree produced by RustParser#literal.
    def enterLiteral(self, ctx:RustParser.LiteralContext):
        pass

    # Exit a parse tree produced by RustParser#literal.
    def exitLiteral(self, ctx:RustParser.LiteralContext):
        pass


    # Enter a parse tree produced by RustParser#arrayLiteral.
    def enterArrayLiteral(self, ctx:RustParser.ArrayLiteralContext):
        pass

    # Exit a parse tree produced by RustParser#arrayLiteral.
    def exitArrayLiteral(self, ctx:RustParser.ArrayLiteralContext):
        pass


    # Enter a parse tree produced by RustParser#stringLiteral.
    def enterStringLiteral(self, ctx:RustParser.StringLiteralContext):
        pass

    # Exit a parse tree produced by RustParser#stringLiteral.
    def exitStringLiteral(self, ctx:RustParser.StringLiteralContext):
        pass



del RustParser