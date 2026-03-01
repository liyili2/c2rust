# Generated from Exp.g4 by ANTLR 4.7.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .ExpParser import ExpParser
else:
    from ExpParser import ExpParser

# This class defines a complete generic visitor for a parse tree produced by ExpParser.

class ExpVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by ExpParser#program.
    def visitProgram(self, ctx:ExpParser.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExpParser#exp.
    def visitExp(self, ctx:ExpParser.ExpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExpParser#vexp.
    def visitVexp(self, ctx:ExpParser.VexpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExpParser#bexp.
    def visitBexp(self, ctx:ExpParser.BexpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExpParser#posiexp.
    def visitPosiexp(self, ctx:ExpParser.PosiexpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExpParser#skipexp.
    def visitSkipexp(self, ctx:ExpParser.SkipexpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExpParser#xgexp.
    def visitXgexp(self, ctx:ExpParser.XgexpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExpParser#cuexp.
    def visitCuexp(self, ctx:ExpParser.CuexpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExpParser#rzexp.
    def visitRzexp(self, ctx:ExpParser.RzexpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExpParser#srexp.
    def visitSrexp(self, ctx:ExpParser.SrexpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExpParser#lshiftexp.
    def visitLshiftexp(self, ctx:ExpParser.LshiftexpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExpParser#rshiftexp.
    def visitRshiftexp(self, ctx:ExpParser.RshiftexpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExpParser#revexp.
    def visitRevexp(self, ctx:ExpParser.RevexpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExpParser#qftexp.
    def visitQftexp(self, ctx:ExpParser.QftexpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExpParser#rqftexp.
    def visitRqftexp(self, ctx:ExpParser.RqftexpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExpParser#numexp.
    def visitNumexp(self, ctx:ExpParser.NumexpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExpParser#addexp.
    def visitAddexp(self, ctx:ExpParser.AddexpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExpParser#subexp.
    def visitSubexp(self, ctx:ExpParser.SubexpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExpParser#multexp.
    def visitMultexp(self, ctx:ExpParser.MultexpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExpParser#divexp.
    def visitDivexp(self, ctx:ExpParser.DivexpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExpParser#modexp.
    def visitModexp(self, ctx:ExpParser.ModexpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExpParser#expexp.
    def visitExpexp(self, ctx:ExpParser.ExpexpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExpParser#letexp.
    def visitLetexp(self, ctx:ExpParser.LetexpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExpParser#matchexp.
    def visitMatchexp(self, ctx:ExpParser.MatchexpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExpParser#boolexp.
    def visitBoolexp(self, ctx:ExpParser.BoolexpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExpParser#callexp.
    def visitCallexp(self, ctx:ExpParser.CallexpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExpParser#ifexp.
    def visitIfexp(self, ctx:ExpParser.IfexpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExpParser#lessexp.
    def visitLessexp(self, ctx:ExpParser.LessexpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExpParser#equalexp.
    def visitEqualexp(self, ctx:ExpParser.EqualexpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExpParser#greaterexp.
    def visitGreaterexp(self, ctx:ExpParser.GreaterexpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExpParser#andexp.
    def visitAndexp(self, ctx:ExpParser.AndexpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExpParser#orexp.
    def visitOrexp(self, ctx:ExpParser.OrexpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExpParser#typea.
    def visitTypea(self, ctx:ExpParser.TypeaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExpParser#booleantype.
    def visitBooleantype(self, ctx:ExpParser.BooleantypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExpParser#numtype.
    def visitNumtype(self, ctx:ExpParser.NumtypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExpParser#pairtype.
    def visitPairtype(self, ctx:ExpParser.PairtypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExpParser#funct.
    def visitFunct(self, ctx:ExpParser.FunctContext):
        return self.visitChildren(ctx)



del ExpParser