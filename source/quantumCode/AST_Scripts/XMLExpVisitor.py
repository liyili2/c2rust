# Generated from XMLExp.g4 by ANTLR 4.7.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .XMLExpParser import XMLExpParser
else:
    from XMLExpParser import XMLExpParser

# This class defines a complete generic visitor for a parse tree produced by XMLExpParser.

class XMLExpVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by XMLExpParser#program.
    def visitProgram(self, ctx:XMLExpParser.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XMLExpParser#exp.
    def visitExp(self, ctx:XMLExpParser.ExpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XMLExpParser#idexp.
    def visitIdexp(self, ctx:XMLExpParser.IdexpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XMLExpParser#vexp.
    def visitVexp(self, ctx:XMLExpParser.VexpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XMLExpParser#numexp.
    def visitNumexp(self, ctx:XMLExpParser.NumexpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XMLExpParser#skipexp.
    def visitSkipexp(self, ctx:XMLExpParser.SkipexpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XMLExpParser#xexp.
    def visitXexp(self, ctx:XMLExpParser.XexpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XMLExpParser#cuexp.
    def visitCuexp(self, ctx:XMLExpParser.CuexpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XMLExpParser#rzexp.
    def visitRzexp(self, ctx:XMLExpParser.RzexpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XMLExpParser#srexp.
    def visitSrexp(self, ctx:XMLExpParser.SrexpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XMLExpParser#lshiftexp.
    def visitLshiftexp(self, ctx:XMLExpParser.LshiftexpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XMLExpParser#rshiftexp.
    def visitRshiftexp(self, ctx:XMLExpParser.RshiftexpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XMLExpParser#revexp.
    def visitRevexp(self, ctx:XMLExpParser.RevexpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XMLExpParser#qftexp.
    def visitQftexp(self, ctx:XMLExpParser.QftexpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XMLExpParser#rqftexp.
    def visitRqftexp(self, ctx:XMLExpParser.RqftexpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XMLExpParser#op.
    def visitOp(self, ctx:XMLExpParser.OpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XMLExpParser#boolexp.
    def visitBoolexp(self, ctx:XMLExpParser.BoolexpContext):
        return self.visitChildren(ctx)



del XMLExpParser