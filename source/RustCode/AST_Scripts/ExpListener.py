# Generated from Exp.g4 by ANTLR 4.7.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .ExpParser import ExpParser
else:
    from ExpParser import ExpParser

# This class defines a complete listener for a parse tree produced by ExpParser.
class ExpListener(ParseTreeListener):

    # Enter a parse tree produced by ExpParser#program.
    def enterProgram(self, ctx:ExpParser.ProgramContext):
        pass

    # Exit a parse tree produced by ExpParser#program.
    def exitProgram(self, ctx:ExpParser.ProgramContext):
        pass


    # Enter a parse tree produced by ExpParser#exp.
    def enterExp(self, ctx:ExpParser.ExpContext):
        pass

    # Exit a parse tree produced by ExpParser#exp.
    def exitExp(self, ctx:ExpParser.ExpContext):
        pass


    # Enter a parse tree produced by ExpParser#vexp.
    def enterVexp(self, ctx:ExpParser.VexpContext):
        pass

    # Exit a parse tree produced by ExpParser#vexp.
    def exitVexp(self, ctx:ExpParser.VexpContext):
        pass


    # Enter a parse tree produced by ExpParser#bexp.
    def enterBexp(self, ctx:ExpParser.BexpContext):
        pass

    # Exit a parse tree produced by ExpParser#bexp.
    def exitBexp(self, ctx:ExpParser.BexpContext):
        pass


    # Enter a parse tree produced by ExpParser#posiexp.
    def enterPosiexp(self, ctx:ExpParser.PosiexpContext):
        pass

    # Exit a parse tree produced by ExpParser#posiexp.
    def exitPosiexp(self, ctx:ExpParser.PosiexpContext):
        pass


    # Enter a parse tree produced by ExpParser#skipexp.
    def enterSkipexp(self, ctx:ExpParser.SkipexpContext):
        pass

    # Exit a parse tree produced by ExpParser#skipexp.
    def exitSkipexp(self, ctx:ExpParser.SkipexpContext):
        pass


    # Enter a parse tree produced by ExpParser#xgexp.
    def enterXgexp(self, ctx:ExpParser.XgexpContext):
        pass

    # Exit a parse tree produced by ExpParser#xgexp.
    def exitXgexp(self, ctx:ExpParser.XgexpContext):
        pass


    # Enter a parse tree produced by ExpParser#cuexp.
    def enterCuexp(self, ctx:ExpParser.CuexpContext):
        pass

    # Exit a parse tree produced by ExpParser#cuexp.
    def exitCuexp(self, ctx:ExpParser.CuexpContext):
        pass


    # Enter a parse tree produced by ExpParser#rzexp.
    def enterRzexp(self, ctx:ExpParser.RzexpContext):
        pass

    # Exit a parse tree produced by ExpParser#rzexp.
    def exitRzexp(self, ctx:ExpParser.RzexpContext):
        pass


    # Enter a parse tree produced by ExpParser#srexp.
    def enterSrexp(self, ctx:ExpParser.SrexpContext):
        pass

    # Exit a parse tree produced by ExpParser#srexp.
    def exitSrexp(self, ctx:ExpParser.SrexpContext):
        pass


    # Enter a parse tree produced by ExpParser#lshiftexp.
    def enterLshiftexp(self, ctx:ExpParser.LshiftexpContext):
        pass

    # Exit a parse tree produced by ExpParser#lshiftexp.
    def exitLshiftexp(self, ctx:ExpParser.LshiftexpContext):
        pass


    # Enter a parse tree produced by ExpParser#rshiftexp.
    def enterRshiftexp(self, ctx:ExpParser.RshiftexpContext):
        pass

    # Exit a parse tree produced by ExpParser#rshiftexp.
    def exitRshiftexp(self, ctx:ExpParser.RshiftexpContext):
        pass


    # Enter a parse tree produced by ExpParser#revexp.
    def enterRevexp(self, ctx:ExpParser.RevexpContext):
        pass

    # Exit a parse tree produced by ExpParser#revexp.
    def exitRevexp(self, ctx:ExpParser.RevexpContext):
        pass


    # Enter a parse tree produced by ExpParser#qftexp.
    def enterQftexp(self, ctx:ExpParser.QftexpContext):
        pass

    # Exit a parse tree produced by ExpParser#qftexp.
    def exitQftexp(self, ctx:ExpParser.QftexpContext):
        pass


    # Enter a parse tree produced by ExpParser#rqftexp.
    def enterRqftexp(self, ctx:ExpParser.RqftexpContext):
        pass

    # Exit a parse tree produced by ExpParser#rqftexp.
    def exitRqftexp(self, ctx:ExpParser.RqftexpContext):
        pass


    # Enter a parse tree produced by ExpParser#numexp.
    def enterNumexp(self, ctx:ExpParser.NumexpContext):
        pass

    # Exit a parse tree produced by ExpParser#numexp.
    def exitNumexp(self, ctx:ExpParser.NumexpContext):
        pass


    # Enter a parse tree produced by ExpParser#addexp.
    def enterAddexp(self, ctx:ExpParser.AddexpContext):
        pass

    # Exit a parse tree produced by ExpParser#addexp.
    def exitAddexp(self, ctx:ExpParser.AddexpContext):
        pass


    # Enter a parse tree produced by ExpParser#subexp.
    def enterSubexp(self, ctx:ExpParser.SubexpContext):
        pass

    # Exit a parse tree produced by ExpParser#subexp.
    def exitSubexp(self, ctx:ExpParser.SubexpContext):
        pass


    # Enter a parse tree produced by ExpParser#multexp.
    def enterMultexp(self, ctx:ExpParser.MultexpContext):
        pass

    # Exit a parse tree produced by ExpParser#multexp.
    def exitMultexp(self, ctx:ExpParser.MultexpContext):
        pass


    # Enter a parse tree produced by ExpParser#divexp.
    def enterDivexp(self, ctx:ExpParser.DivexpContext):
        pass

    # Exit a parse tree produced by ExpParser#divexp.
    def exitDivexp(self, ctx:ExpParser.DivexpContext):
        pass


    # Enter a parse tree produced by ExpParser#modexp.
    def enterModexp(self, ctx:ExpParser.ModexpContext):
        pass

    # Exit a parse tree produced by ExpParser#modexp.
    def exitModexp(self, ctx:ExpParser.ModexpContext):
        pass


    # Enter a parse tree produced by ExpParser#expexp.
    def enterExpexp(self, ctx:ExpParser.ExpexpContext):
        pass

    # Exit a parse tree produced by ExpParser#expexp.
    def exitExpexp(self, ctx:ExpParser.ExpexpContext):
        pass


    # Enter a parse tree produced by ExpParser#letexp.
    def enterLetexp(self, ctx:ExpParser.LetexpContext):
        pass

    # Exit a parse tree produced by ExpParser#letexp.
    def exitLetexp(self, ctx:ExpParser.LetexpContext):
        pass


    # Enter a parse tree produced by ExpParser#matchexp.
    def enterMatchexp(self, ctx:ExpParser.MatchexpContext):
        pass

    # Exit a parse tree produced by ExpParser#matchexp.
    def exitMatchexp(self, ctx:ExpParser.MatchexpContext):
        pass


    # Enter a parse tree produced by ExpParser#boolexp.
    def enterBoolexp(self, ctx:ExpParser.BoolexpContext):
        pass

    # Exit a parse tree produced by ExpParser#boolexp.
    def exitBoolexp(self, ctx:ExpParser.BoolexpContext):
        pass


    # Enter a parse tree produced by ExpParser#callexp.
    def enterCallexp(self, ctx:ExpParser.CallexpContext):
        pass

    # Exit a parse tree produced by ExpParser#callexp.
    def exitCallexp(self, ctx:ExpParser.CallexpContext):
        pass


    # Enter a parse tree produced by ExpParser#ifexp.
    def enterIfexp(self, ctx:ExpParser.IfexpContext):
        pass

    # Exit a parse tree produced by ExpParser#ifexp.
    def exitIfexp(self, ctx:ExpParser.IfexpContext):
        pass


    # Enter a parse tree produced by ExpParser#lessexp.
    def enterLessexp(self, ctx:ExpParser.LessexpContext):
        pass

    # Exit a parse tree produced by ExpParser#lessexp.
    def exitLessexp(self, ctx:ExpParser.LessexpContext):
        pass


    # Enter a parse tree produced by ExpParser#equalexp.
    def enterEqualexp(self, ctx:ExpParser.EqualexpContext):
        pass

    # Exit a parse tree produced by ExpParser#equalexp.
    def exitEqualexp(self, ctx:ExpParser.EqualexpContext):
        pass


    # Enter a parse tree produced by ExpParser#greaterexp.
    def enterGreaterexp(self, ctx:ExpParser.GreaterexpContext):
        pass

    # Exit a parse tree produced by ExpParser#greaterexp.
    def exitGreaterexp(self, ctx:ExpParser.GreaterexpContext):
        pass


    # Enter a parse tree produced by ExpParser#andexp.
    def enterAndexp(self, ctx:ExpParser.AndexpContext):
        pass

    # Exit a parse tree produced by ExpParser#andexp.
    def exitAndexp(self, ctx:ExpParser.AndexpContext):
        pass


    # Enter a parse tree produced by ExpParser#orexp.
    def enterOrexp(self, ctx:ExpParser.OrexpContext):
        pass

    # Exit a parse tree produced by ExpParser#orexp.
    def exitOrexp(self, ctx:ExpParser.OrexpContext):
        pass


    # Enter a parse tree produced by ExpParser#typea.
    def enterTypea(self, ctx:ExpParser.TypeaContext):
        pass

    # Exit a parse tree produced by ExpParser#typea.
    def exitTypea(self, ctx:ExpParser.TypeaContext):
        pass


    # Enter a parse tree produced by ExpParser#booleantype.
    def enterBooleantype(self, ctx:ExpParser.BooleantypeContext):
        pass

    # Exit a parse tree produced by ExpParser#booleantype.
    def exitBooleantype(self, ctx:ExpParser.BooleantypeContext):
        pass


    # Enter a parse tree produced by ExpParser#numtype.
    def enterNumtype(self, ctx:ExpParser.NumtypeContext):
        pass

    # Exit a parse tree produced by ExpParser#numtype.
    def exitNumtype(self, ctx:ExpParser.NumtypeContext):
        pass


    # Enter a parse tree produced by ExpParser#pairtype.
    def enterPairtype(self, ctx:ExpParser.PairtypeContext):
        pass

    # Exit a parse tree produced by ExpParser#pairtype.
    def exitPairtype(self, ctx:ExpParser.PairtypeContext):
        pass


    # Enter a parse tree produced by ExpParser#funct.
    def enterFunct(self, ctx:ExpParser.FunctContext):
        pass

    # Exit a parse tree produced by ExpParser#funct.
    def exitFunct(self, ctx:ExpParser.FunctContext):
        pass


