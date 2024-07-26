# Generated from XMLExp.g4 by ANTLR 4.13.1
from antlr4 import *
if "." in __name__:
    from .XMLExpParser import XMLExpParser
else:
    from XMLExpParser import XMLExpParser

# This class defines a complete generic visitor for a parse tree produced by XMLExpParser.

class XMLExpVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by XMLExpParser#program.
    def visitProgram(self, ctx:XMLExpParser.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XMLExpParser#blockstmt.
    def visitBlockstmt(self, ctx:XMLExpParser.BlockstmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XMLExpParser#letstmt.
    def visitLetstmt(self, ctx:XMLExpParser.LetstmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XMLExpParser#printstmt.
    def visitPrintstmt(self, ctx:XMLExpParser.PrintstmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XMLExpParser#ifstmt.
    def visitIfstmt(self, ctx:XMLExpParser.IfstmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XMLExpParser#breakstmt.
    def visitBreakstmt(self, ctx:XMLExpParser.BreakstmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XMLExpParser#returnstmt.
    def visitReturnstmt(self, ctx:XMLExpParser.ReturnstmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XMLExpParser#loopstmt.
    def visitLoopstmt(self, ctx:XMLExpParser.LoopstmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XMLExpParser#forstmt.
    def visitForstmt(self, ctx:XMLExpParser.ForstmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XMLExpParser#exp.
    def visitExp(self, ctx:XMLExpParser.ExpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XMLExpParser#idexp.
    def visitIdexp(self, ctx:XMLExpParser.IdexpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XMLExpParser#stringval.
    def visitStringval(self, ctx:XMLExpParser.StringvalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XMLExpParser#vexp.
    def visitVexp(self, ctx:XMLExpParser.VexpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XMLExpParser#numexp.
    def visitNumexp(self, ctx:XMLExpParser.NumexpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XMLExpParser#binexp.
    def visitBinexp(self, ctx:XMLExpParser.BinexpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XMLExpParser#op.
    def visitOp(self, ctx:XMLExpParser.OpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XMLExpParser#boolexp.
    def visitBoolexp(self, ctx:XMLExpParser.BoolexpContext):
        return self.visitChildren(ctx)



del XMLExpParser