# Generated from XMLExp.g4 by ANTLR 4.7.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .XMLExpParser import XMLExpParser
else:
    from XMLExpParser import XMLExpParser

# This class defines a complete listener for a parse tree produced by XMLExpParser.
class XMLExpListener(ParseTreeListener):

    # Enter a parse tree produced by XMLExpParser#program.
    def enterProgram(self, ctx:XMLExpParser.ProgramContext):
        pass

    # Exit a parse tree produced by XMLExpParser#program.
    def exitProgram(self, ctx:XMLExpParser.ProgramContext):
        pass


    # Enter a parse tree produced by XMLExpParser#blockstmt.
    def enterBlockstmt(self, ctx:XMLExpParser.BlockstmtContext):
        pass

    # Exit a parse tree produced by XMLExpParser#blockstmt.
    def exitBlockstmt(self, ctx:XMLExpParser.BlockstmtContext):
        pass


    # Enter a parse tree produced by XMLExpParser#letstmt.
    def enterLetstmt(self, ctx:XMLExpParser.LetstmtContext):
        pass

    # Exit a parse tree produced by XMLExpParser#letstmt.
    def exitLetstmt(self, ctx:XMLExpParser.LetstmtContext):
        pass


    # Enter a parse tree produced by XMLExpParser#printstmt.
    def enterPrintstmt(self, ctx:XMLExpParser.PrintstmtContext):
        pass

    # Exit a parse tree produced by XMLExpParser#printstmt.
    def exitPrintstmt(self, ctx:XMLExpParser.PrintstmtContext):
        pass


    # Enter a parse tree produced by XMLExpParser#ifstmt.
    def enterIfstmt(self, ctx:XMLExpParser.IfstmtContext):
        pass

    # Exit a parse tree produced by XMLExpParser#ifstmt.
    def exitIfstmt(self, ctx:XMLExpParser.IfstmtContext):
        pass


    # Enter a parse tree produced by XMLExpParser#breakstmt.
    def enterBreakstmt(self, ctx:XMLExpParser.BreakstmtContext):
        pass

    # Exit a parse tree produced by XMLExpParser#breakstmt.
    def exitBreakstmt(self, ctx:XMLExpParser.BreakstmtContext):
        pass


    # Enter a parse tree produced by XMLExpParser#returnstmt.
    def enterReturnstmt(self, ctx:XMLExpParser.ReturnstmtContext):
        pass

    # Exit a parse tree produced by XMLExpParser#returnstmt.
    def exitReturnstmt(self, ctx:XMLExpParser.ReturnstmtContext):
        pass


    # Enter a parse tree produced by XMLExpParser#loopstmt.
    def enterLoopstmt(self, ctx:XMLExpParser.LoopstmtContext):
        pass

    # Exit a parse tree produced by XMLExpParser#loopstmt.
    def exitLoopstmt(self, ctx:XMLExpParser.LoopstmtContext):
        pass


    # Enter a parse tree produced by XMLExpParser#forstmt.
    def enterForstmt(self, ctx:XMLExpParser.ForstmtContext):
        pass

    # Exit a parse tree produced by XMLExpParser#forstmt.
    def exitForstmt(self, ctx:XMLExpParser.ForstmtContext):
        pass


    # Enter a parse tree produced by XMLExpParser#exp.
    def enterExp(self, ctx:XMLExpParser.ExpContext):
        pass

    # Exit a parse tree produced by XMLExpParser#exp.
    def exitExp(self, ctx:XMLExpParser.ExpContext):
        pass


    # Enter a parse tree produced by XMLExpParser#idexp.
    def enterIdexp(self, ctx:XMLExpParser.IdexpContext):
        pass

    # Exit a parse tree produced by XMLExpParser#idexp.
    def exitIdexp(self, ctx:XMLExpParser.IdexpContext):
        pass


    # Enter a parse tree produced by XMLExpParser#stringval.
    def enterStringval(self, ctx:XMLExpParser.StringvalContext):
        pass

    # Exit a parse tree produced by XMLExpParser#stringval.
    def exitStringval(self, ctx:XMLExpParser.StringvalContext):
        pass


    # Enter a parse tree produced by XMLExpParser#vexp.
    def enterVexp(self, ctx:XMLExpParser.VexpContext):
        pass

    # Exit a parse tree produced by XMLExpParser#vexp.
    def exitVexp(self, ctx:XMLExpParser.VexpContext):
        pass


    # Enter a parse tree produced by XMLExpParser#numexp.
    def enterNumexp(self, ctx:XMLExpParser.NumexpContext):
        pass

    # Exit a parse tree produced by XMLExpParser#numexp.
    def exitNumexp(self, ctx:XMLExpParser.NumexpContext):
        pass


    # Enter a parse tree produced by XMLExpParser#binexp.
    def enterBinexp(self, ctx:XMLExpParser.BinexpContext):
        pass

    # Exit a parse tree produced by XMLExpParser#binexp.
    def exitBinexp(self, ctx:XMLExpParser.BinexpContext):
        pass


    # Enter a parse tree produced by XMLExpParser#op.
    def enterOp(self, ctx:XMLExpParser.OpContext):
        pass

    # Exit a parse tree produced by XMLExpParser#op.
    def exitOp(self, ctx:XMLExpParser.OpContext):
        pass


    # Enter a parse tree produced by XMLExpParser#boolexp.
    def enterBoolexp(self, ctx:XMLExpParser.BoolexpContext):
        pass

    # Exit a parse tree produced by XMLExpParser#boolexp.
    def exitBoolexp(self, ctx:XMLExpParser.BoolexpContext):
        pass


