# Generated from Rust.g4 by ANTLR 4.13.1
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


    # Enter a parse tree produced by RustParser#topLevelDef.
    def enterTopLevelDef(self, ctx:RustParser.TopLevelDefContext):
        pass

    # Exit a parse tree produced by RustParser#topLevelDef.
    def exitTopLevelDef(self, ctx:RustParser.TopLevelDefContext):
        pass


    # Enter a parse tree produced by RustParser#typeAlias.
    def enterTypeAlias(self, ctx:RustParser.TypeAliasContext):
        pass

    # Exit a parse tree produced by RustParser#typeAlias.
    def exitTypeAlias(self, ctx:RustParser.TypeAliasContext):
        pass


    # Enter a parse tree produced by RustParser#interfaceDef.
    def enterInterfaceDef(self, ctx:RustParser.InterfaceDefContext):
        pass

    # Exit a parse tree produced by RustParser#interfaceDef.
    def exitInterfaceDef(self, ctx:RustParser.InterfaceDefContext):
        pass


    # Enter a parse tree produced by RustParser#externBlock.
    def enterExternBlock(self, ctx:RustParser.ExternBlockContext):
        pass

    # Exit a parse tree produced by RustParser#externBlock.
    def exitExternBlock(self, ctx:RustParser.ExternBlockContext):
        pass


    # Enter a parse tree produced by RustParser#externItem.
    def enterExternItem(self, ctx:RustParser.ExternItemContext):
        pass

    # Exit a parse tree produced by RustParser#externItem.
    def exitExternItem(self, ctx:RustParser.ExternItemContext):
        pass


    # Enter a parse tree produced by RustParser#externParams.
    def enterExternParams(self, ctx:RustParser.ExternParamsContext):
        pass

    # Exit a parse tree produced by RustParser#externParams.
    def exitExternParams(self, ctx:RustParser.ExternParamsContext):
        pass


    # Enter a parse tree produced by RustParser#externParam.
    def enterExternParam(self, ctx:RustParser.ExternParamContext):
        pass

    # Exit a parse tree produced by RustParser#externParam.
    def exitExternParam(self, ctx:RustParser.ExternParamContext):
        pass


    # Enter a parse tree produced by RustParser#visibility.
    def enterVisibility(self, ctx:RustParser.VisibilityContext):
        pass

    # Exit a parse tree produced by RustParser#visibility.
    def exitVisibility(self, ctx:RustParser.VisibilityContext):
        pass


    # Enter a parse tree produced by RustParser#unsafeModifier.
    def enterUnsafeModifier(self, ctx:RustParser.UnsafeModifierContext):
        pass

    # Exit a parse tree produced by RustParser#unsafeModifier.
    def exitUnsafeModifier(self, ctx:RustParser.UnsafeModifierContext):
        pass


    # Enter a parse tree produced by RustParser#externAbi.
    def enterExternAbi(self, ctx:RustParser.ExternAbiContext):
        pass

    # Exit a parse tree produced by RustParser#externAbi.
    def exitExternAbi(self, ctx:RustParser.ExternAbiContext):
        pass


    # Enter a parse tree produced by RustParser#attributes.
    def enterAttributes(self, ctx:RustParser.AttributesContext):
        pass

    # Exit a parse tree produced by RustParser#attributes.
    def exitAttributes(self, ctx:RustParser.AttributesContext):
        pass


    # Enter a parse tree produced by RustParser#innerAttribute.
    def enterInnerAttribute(self, ctx:RustParser.InnerAttributeContext):
        pass

    # Exit a parse tree produced by RustParser#innerAttribute.
    def exitInnerAttribute(self, ctx:RustParser.InnerAttributeContext):
        pass


    # Enter a parse tree produced by RustParser#attribute.
    def enterAttribute(self, ctx:RustParser.AttributeContext):
        pass

    # Exit a parse tree produced by RustParser#attribute.
    def exitAttribute(self, ctx:RustParser.AttributeContext):
        pass


    # Enter a parse tree produced by RustParser#attrArgs.
    def enterAttrArgs(self, ctx:RustParser.AttrArgsContext):
        pass

    # Exit a parse tree produced by RustParser#attrArgs.
    def exitAttrArgs(self, ctx:RustParser.AttrArgsContext):
        pass


    # Enter a parse tree produced by RustParser#attrArg.
    def enterAttrArg(self, ctx:RustParser.AttrArgContext):
        pass

    # Exit a parse tree produced by RustParser#attrArg.
    def exitAttrArg(self, ctx:RustParser.AttrArgContext):
        pass


    # Enter a parse tree produced by RustParser#attrValue.
    def enterAttrValue(self, ctx:RustParser.AttrValueContext):
        pass

    # Exit a parse tree produced by RustParser#attrValue.
    def exitAttrValue(self, ctx:RustParser.AttrValueContext):
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


    # Enter a parse tree produced by RustParser#structLiteral.
    def enterStructLiteral(self, ctx:RustParser.StructLiteralContext):
        pass

    # Exit a parse tree produced by RustParser#structLiteral.
    def exitStructLiteral(self, ctx:RustParser.StructLiteralContext):
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


    # Enter a parse tree produced by RustParser#constDef.
    def enterConstDef(self, ctx:RustParser.ConstDefContext):
        pass

    # Exit a parse tree produced by RustParser#constDef.
    def exitConstDef(self, ctx:RustParser.ConstDefContext):
        pass


    # Enter a parse tree produced by RustParser#unionDef.
    def enterUnionDef(self, ctx:RustParser.UnionDefContext):
        pass

    # Exit a parse tree produced by RustParser#unionDef.
    def exitUnionDef(self, ctx:RustParser.UnionDefContext):
        pass


    # Enter a parse tree produced by RustParser#unionField.
    def enterUnionField(self, ctx:RustParser.UnionFieldContext):
        pass

    # Exit a parse tree produced by RustParser#unionField.
    def exitUnionField(self, ctx:RustParser.UnionFieldContext):
        pass


    # Enter a parse tree produced by RustParser#unsafeDef.
    def enterUnsafeDef(self, ctx:RustParser.UnsafeDefContext):
        pass

    # Exit a parse tree produced by RustParser#unsafeDef.
    def exitUnsafeDef(self, ctx:RustParser.UnsafeDefContext):
        pass


    # Enter a parse tree produced by RustParser#type.
    def enterType(self, ctx:RustParser.TypeContext):
        pass

    # Exit a parse tree produced by RustParser#type.
    def exitType(self, ctx:RustParser.TypeContext):
        pass


    # Enter a parse tree produced by RustParser#pointerType.
    def enterPointerType(self, ctx:RustParser.PointerTypeContext):
        pass

    # Exit a parse tree produced by RustParser#pointerType.
    def exitPointerType(self, ctx:RustParser.PointerTypeContext):
        pass


    # Enter a parse tree produced by RustParser#basicType.
    def enterBasicType(self, ctx:RustParser.BasicTypeContext):
        pass

    # Exit a parse tree produced by RustParser#basicType.
    def exitBasicType(self, ctx:RustParser.BasicTypeContext):
        pass


    # Enter a parse tree produced by RustParser#typePath.
    def enterTypePath(self, ctx:RustParser.TypePathContext):
        pass

    # Exit a parse tree produced by RustParser#typePath.
    def exitTypePath(self, ctx:RustParser.TypePathContext):
        pass


    # Enter a parse tree produced by RustParser#block.
    def enterBlock(self, ctx:RustParser.BlockContext):
        pass

    # Exit a parse tree produced by RustParser#block.
    def exitBlock(self, ctx:RustParser.BlockContext):
        pass


    # Enter a parse tree produced by RustParser#unsafeBlock.
    def enterUnsafeBlock(self, ctx:RustParser.UnsafeBlockContext):
        pass

    # Exit a parse tree produced by RustParser#unsafeBlock.
    def exitUnsafeBlock(self, ctx:RustParser.UnsafeBlockContext):
        pass


    # Enter a parse tree produced by RustParser#statement.
    def enterStatement(self, ctx:RustParser.StatementContext):
        pass

    # Exit a parse tree produced by RustParser#statement.
    def exitStatement(self, ctx:RustParser.StatementContext):
        pass


    # Enter a parse tree produced by RustParser#callStmt.
    def enterCallStmt(self, ctx:RustParser.CallStmtContext):
        pass

    # Exit a parse tree produced by RustParser#callStmt.
    def exitCallStmt(self, ctx:RustParser.CallStmtContext):
        pass


    # Enter a parse tree produced by RustParser#letStmt.
    def enterLetStmt(self, ctx:RustParser.LetStmtContext):
        pass

    # Exit a parse tree produced by RustParser#letStmt.
    def exitLetStmt(self, ctx:RustParser.LetStmtContext):
        pass


    # Enter a parse tree produced by RustParser#varDef.
    def enterVarDef(self, ctx:RustParser.VarDefContext):
        pass

    # Exit a parse tree produced by RustParser#varDef.
    def exitVarDef(self, ctx:RustParser.VarDefContext):
        pass


    # Enter a parse tree produced by RustParser#compoundOp.
    def enterCompoundOp(self, ctx:RustParser.CompoundOpContext):
        pass

    # Exit a parse tree produced by RustParser#compoundOp.
    def exitCompoundOp(self, ctx:RustParser.CompoundOpContext):
        pass


    # Enter a parse tree produced by RustParser#compoundAssignment.
    def enterCompoundAssignment(self, ctx:RustParser.CompoundAssignmentContext):
        pass

    # Exit a parse tree produced by RustParser#compoundAssignment.
    def exitCompoundAssignment(self, ctx:RustParser.CompoundAssignmentContext):
        pass


    # Enter a parse tree produced by RustParser#matchStmt.
    def enterMatchStmt(self, ctx:RustParser.MatchStmtContext):
        pass

    # Exit a parse tree produced by RustParser#matchStmt.
    def exitMatchStmt(self, ctx:RustParser.MatchStmtContext):
        pass


    # Enter a parse tree produced by RustParser#whileStmt.
    def enterWhileStmt(self, ctx:RustParser.WhileStmtContext):
        pass

    # Exit a parse tree produced by RustParser#whileStmt.
    def exitWhileStmt(self, ctx:RustParser.WhileStmtContext):
        pass


    # Enter a parse tree produced by RustParser#initializer.
    def enterInitializer(self, ctx:RustParser.InitializerContext):
        pass

    # Exit a parse tree produced by RustParser#initializer.
    def exitInitializer(self, ctx:RustParser.InitializerContext):
        pass


    # Enter a parse tree produced by RustParser#staticVarDecl.
    def enterStaticVarDecl(self, ctx:RustParser.StaticVarDeclContext):
        pass

    # Exit a parse tree produced by RustParser#staticVarDecl.
    def exitStaticVarDecl(self, ctx:RustParser.StaticVarDeclContext):
        pass


    # Enter a parse tree produced by RustParser#initBlock.
    def enterInitBlock(self, ctx:RustParser.InitBlockContext):
        pass

    # Exit a parse tree produced by RustParser#initBlock.
    def exitInitBlock(self, ctx:RustParser.InitBlockContext):
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


    # Enter a parse tree produced by RustParser#loopStmt.
    def enterLoopStmt(self, ctx:RustParser.LoopStmtContext):
        pass

    # Exit a parse tree produced by RustParser#loopStmt.
    def exitLoopStmt(self, ctx:RustParser.LoopStmtContext):
        pass


    # Enter a parse tree produced by RustParser#expression.
    def enterExpression(self, ctx:RustParser.ExpressionContext):
        pass

    # Exit a parse tree produced by RustParser#expression.
    def exitExpression(self, ctx:RustParser.ExpressionContext):
        pass


    # Enter a parse tree produced by RustParser#typePathExpression.
    def enterTypePathExpression(self, ctx:RustParser.TypePathExpressionContext):
        pass

    # Exit a parse tree produced by RustParser#typePathExpression.
    def exitTypePathExpression(self, ctx:RustParser.TypePathExpressionContext):
        pass


    # Enter a parse tree produced by RustParser#patternPrefix.
    def enterPatternPrefix(self, ctx:RustParser.PatternPrefixContext):
        pass

    # Exit a parse tree produced by RustParser#patternPrefix.
    def exitPatternPrefix(self, ctx:RustParser.PatternPrefixContext):
        pass


    # Enter a parse tree produced by RustParser#pattern.
    def enterPattern(self, ctx:RustParser.PatternContext):
        pass

    # Exit a parse tree produced by RustParser#pattern.
    def exitPattern(self, ctx:RustParser.PatternContext):
        pass


    # Enter a parse tree produced by RustParser#castExpressionPostFix.
    def enterCastExpressionPostFix(self, ctx:RustParser.CastExpressionPostFixContext):
        pass

    # Exit a parse tree produced by RustParser#castExpressionPostFix.
    def exitCastExpressionPostFix(self, ctx:RustParser.CastExpressionPostFixContext):
        pass


    # Enter a parse tree produced by RustParser#compoundOps.
    def enterCompoundOps(self, ctx:RustParser.CompoundOpsContext):
        pass

    # Exit a parse tree produced by RustParser#compoundOps.
    def exitCompoundOps(self, ctx:RustParser.CompoundOpsContext):
        pass


    # Enter a parse tree produced by RustParser#patternSymbol.
    def enterPatternSymbol(self, ctx:RustParser.PatternSymbolContext):
        pass

    # Exit a parse tree produced by RustParser#patternSymbol.
    def exitPatternSymbol(self, ctx:RustParser.PatternSymbolContext):
        pass


    # Enter a parse tree produced by RustParser#conditionalOps.
    def enterConditionalOps(self, ctx:RustParser.ConditionalOpsContext):
        pass

    # Exit a parse tree produced by RustParser#conditionalOps.
    def exitConditionalOps(self, ctx:RustParser.ConditionalOpsContext):
        pass


    # Enter a parse tree produced by RustParser#booleanOps.
    def enterBooleanOps(self, ctx:RustParser.BooleanOpsContext):
        pass

    # Exit a parse tree produced by RustParser#booleanOps.
    def exitBooleanOps(self, ctx:RustParser.BooleanOpsContext):
        pass


    # Enter a parse tree produced by RustParser#binaryOps.
    def enterBinaryOps(self, ctx:RustParser.BinaryOpsContext):
        pass

    # Exit a parse tree produced by RustParser#binaryOps.
    def exitBinaryOps(self, ctx:RustParser.BinaryOpsContext):
        pass


    # Enter a parse tree produced by RustParser#structFieldDec.
    def enterStructFieldDec(self, ctx:RustParser.StructFieldDecContext):
        pass

    # Exit a parse tree produced by RustParser#structFieldDec.
    def exitStructFieldDec(self, ctx:RustParser.StructFieldDecContext):
        pass


    # Enter a parse tree produced by RustParser#mutableExpression.
    def enterMutableExpression(self, ctx:RustParser.MutableExpressionContext):
        pass

    # Exit a parse tree produced by RustParser#mutableExpression.
    def exitMutableExpression(self, ctx:RustParser.MutableExpressionContext):
        pass


    # Enter a parse tree produced by RustParser#unaryOpes.
    def enterUnaryOpes(self, ctx:RustParser.UnaryOpesContext):
        pass

    # Exit a parse tree produced by RustParser#unaryOpes.
    def exitUnaryOpes(self, ctx:RustParser.UnaryOpesContext):
        pass


    # Enter a parse tree produced by RustParser#parenExpression.
    def enterParenExpression(self, ctx:RustParser.ParenExpressionContext):
        pass

    # Exit a parse tree produced by RustParser#parenExpression.
    def exitParenExpression(self, ctx:RustParser.ParenExpressionContext):
        pass


    # Enter a parse tree produced by RustParser#referenceExpression.
    def enterReferenceExpression(self, ctx:RustParser.ReferenceExpressionContext):
        pass

    # Exit a parse tree produced by RustParser#referenceExpression.
    def exitReferenceExpression(self, ctx:RustParser.ReferenceExpressionContext):
        pass


    # Enter a parse tree produced by RustParser#dereferenceExpression.
    def enterDereferenceExpression(self, ctx:RustParser.DereferenceExpressionContext):
        pass

    # Exit a parse tree produced by RustParser#dereferenceExpression.
    def exitDereferenceExpression(self, ctx:RustParser.DereferenceExpressionContext):
        pass


    # Enter a parse tree produced by RustParser#expressionBlock.
    def enterExpressionBlock(self, ctx:RustParser.ExpressionBlockContext):
        pass

    # Exit a parse tree produced by RustParser#expressionBlock.
    def exitExpressionBlock(self, ctx:RustParser.ExpressionBlockContext):
        pass


    # Enter a parse tree produced by RustParser#borrowExpression.
    def enterBorrowExpression(self, ctx:RustParser.BorrowExpressionContext):
        pass

    # Exit a parse tree produced by RustParser#borrowExpression.
    def exitBorrowExpression(self, ctx:RustParser.BorrowExpressionContext):
        pass


    # Enter a parse tree produced by RustParser#primaryExpression.
    def enterPrimaryExpression(self, ctx:RustParser.PrimaryExpressionContext):
        pass

    # Exit a parse tree produced by RustParser#primaryExpression.
    def exitPrimaryExpression(self, ctx:RustParser.PrimaryExpressionContext):
        pass


    # Enter a parse tree produced by RustParser#fieldAccessPostFix.
    def enterFieldAccessPostFix(self, ctx:RustParser.FieldAccessPostFixContext):
        pass

    # Exit a parse tree produced by RustParser#fieldAccessPostFix.
    def exitFieldAccessPostFix(self, ctx:RustParser.FieldAccessPostFixContext):
        pass


    # Enter a parse tree produced by RustParser#callExpressionPostFix.
    def enterCallExpressionPostFix(self, ctx:RustParser.CallExpressionPostFixContext):
        pass

    # Exit a parse tree produced by RustParser#callExpressionPostFix.
    def exitCallExpressionPostFix(self, ctx:RustParser.CallExpressionPostFixContext):
        pass


    # Enter a parse tree produced by RustParser#functionCallArgs.
    def enterFunctionCallArgs(self, ctx:RustParser.FunctionCallArgsContext):
        pass

    # Exit a parse tree produced by RustParser#functionCallArgs.
    def exitFunctionCallArgs(self, ctx:RustParser.FunctionCallArgsContext):
        pass


    # Enter a parse tree produced by RustParser#postfixExpression.
    def enterPostfixExpression(self, ctx:RustParser.PostfixExpressionContext):
        pass

    # Exit a parse tree produced by RustParser#postfixExpression.
    def exitPostfixExpression(self, ctx:RustParser.PostfixExpressionContext):
        pass


    # Enter a parse tree produced by RustParser#qualifiedFunctionCall.
    def enterQualifiedFunctionCall(self, ctx:RustParser.QualifiedFunctionCallContext):
        pass

    # Exit a parse tree produced by RustParser#qualifiedFunctionCall.
    def exitQualifiedFunctionCall(self, ctx:RustParser.QualifiedFunctionCallContext):
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


    # Enter a parse tree produced by RustParser#genericArgs.
    def enterGenericArgs(self, ctx:RustParser.GenericArgsContext):
        pass

    # Exit a parse tree produced by RustParser#genericArgs.
    def exitGenericArgs(self, ctx:RustParser.GenericArgsContext):
        pass


    # Enter a parse tree produced by RustParser#structLiteralField.
    def enterStructLiteralField(self, ctx:RustParser.StructLiteralFieldContext):
        pass

    # Exit a parse tree produced by RustParser#structLiteralField.
    def exitStructLiteralField(self, ctx:RustParser.StructLiteralFieldContext):
        pass


    # Enter a parse tree produced by RustParser#matchArm.
    def enterMatchArm(self, ctx:RustParser.MatchArmContext):
        pass

    # Exit a parse tree produced by RustParser#matchArm.
    def exitMatchArm(self, ctx:RustParser.MatchArmContext):
        pass


    # Enter a parse tree produced by RustParser#matchPattern.
    def enterMatchPattern(self, ctx:RustParser.MatchPatternContext):
        pass

    # Exit a parse tree produced by RustParser#matchPattern.
    def exitMatchPattern(self, ctx:RustParser.MatchPatternContext):
        pass


    # Enter a parse tree produced by RustParser#argumentList.
    def enterArgumentList(self, ctx:RustParser.ArgumentListContext):
        pass

    # Exit a parse tree produced by RustParser#argumentList.
    def exitArgumentList(self, ctx:RustParser.ArgumentListContext):
        pass


    # Enter a parse tree produced by RustParser#literal.
    def enterLiteral(self, ctx:RustParser.LiteralContext):
        pass

    # Exit a parse tree produced by RustParser#literal.
    def exitLiteral(self, ctx:RustParser.LiteralContext):
        pass


    # Enter a parse tree produced by RustParser#booleanLiteral.
    def enterBooleanLiteral(self, ctx:RustParser.BooleanLiteralContext):
        pass

    # Exit a parse tree produced by RustParser#booleanLiteral.
    def exitBooleanLiteral(self, ctx:RustParser.BooleanLiteralContext):
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