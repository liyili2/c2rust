# Generated from TypeLang.g4 by ANTLR 4.7.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .TypeLangParser import TypeLangParser
else:
    from TypeLangParser import TypeLangParser

# This class defines a complete listener for a parse tree produced by TypeLangParser.
class TypeLangListener(ParseTreeListener):

    # Enter a parse tree produced by TypeLangParser#program.
    def enterProgram(self, ctx:TypeLangParser.ProgramContext):
        pass

    # Exit a parse tree produced by TypeLangParser#program.
    def exitProgram(self, ctx:TypeLangParser.ProgramContext):
        pass


    # Enter a parse tree produced by TypeLangParser#exp.
    def enterExp(self, ctx:TypeLangParser.ExpContext):
        pass

    # Exit a parse tree produced by TypeLangParser#exp.
    def exitExp(self, ctx:TypeLangParser.ExpContext):
        pass


    # Enter a parse tree produced by TypeLangParser#numexp.
    def enterNumexp(self, ctx:TypeLangParser.NumexpContext):
        pass

    # Exit a parse tree produced by TypeLangParser#numexp.
    def exitNumexp(self, ctx:TypeLangParser.NumexpContext):
        pass


    # Enter a parse tree produced by TypeLangParser#addexp.
    def enterAddexp(self, ctx:TypeLangParser.AddexpContext):
        pass

    # Exit a parse tree produced by TypeLangParser#addexp.
    def exitAddexp(self, ctx:TypeLangParser.AddexpContext):
        pass


    # Enter a parse tree produced by TypeLangParser#subexp.
    def enterSubexp(self, ctx:TypeLangParser.SubexpContext):
        pass

    # Exit a parse tree produced by TypeLangParser#subexp.
    def exitSubexp(self, ctx:TypeLangParser.SubexpContext):
        pass


    # Enter a parse tree produced by TypeLangParser#multexp.
    def enterMultexp(self, ctx:TypeLangParser.MultexpContext):
        pass

    # Exit a parse tree produced by TypeLangParser#multexp.
    def exitMultexp(self, ctx:TypeLangParser.MultexpContext):
        pass


    # Enter a parse tree produced by TypeLangParser#divexp.
    def enterDivexp(self, ctx:TypeLangParser.DivexpContext):
        pass

    # Exit a parse tree produced by TypeLangParser#divexp.
    def exitDivexp(self, ctx:TypeLangParser.DivexpContext):
        pass


    # Enter a parse tree produced by TypeLangParser#varexp.
    def enterVarexp(self, ctx:TypeLangParser.VarexpContext):
        pass

    # Exit a parse tree produced by TypeLangParser#varexp.
    def exitVarexp(self, ctx:TypeLangParser.VarexpContext):
        pass


    # Enter a parse tree produced by TypeLangParser#letexp.
    def enterLetexp(self, ctx:TypeLangParser.LetexpContext):
        pass

    # Exit a parse tree produced by TypeLangParser#letexp.
    def exitLetexp(self, ctx:TypeLangParser.LetexpContext):
        pass


    # Enter a parse tree produced by TypeLangParser#definedecl.
    def enterDefinedecl(self, ctx:TypeLangParser.DefinedeclContext):
        pass

    # Exit a parse tree produced by TypeLangParser#definedecl.
    def exitDefinedecl(self, ctx:TypeLangParser.DefinedeclContext):
        pass


    # Enter a parse tree produced by TypeLangParser#carexp.
    def enterCarexp(self, ctx:TypeLangParser.CarexpContext):
        pass

    # Exit a parse tree produced by TypeLangParser#carexp.
    def exitCarexp(self, ctx:TypeLangParser.CarexpContext):
        pass


    # Enter a parse tree produced by TypeLangParser#cdrexp.
    def enterCdrexp(self, ctx:TypeLangParser.CdrexpContext):
        pass

    # Exit a parse tree produced by TypeLangParser#cdrexp.
    def exitCdrexp(self, ctx:TypeLangParser.CdrexpContext):
        pass


    # Enter a parse tree produced by TypeLangParser#consexp.
    def enterConsexp(self, ctx:TypeLangParser.ConsexpContext):
        pass

    # Exit a parse tree produced by TypeLangParser#consexp.
    def exitConsexp(self, ctx:TypeLangParser.ConsexpContext):
        pass


    # Enter a parse tree produced by TypeLangParser#listexp.
    def enterListexp(self, ctx:TypeLangParser.ListexpContext):
        pass

    # Exit a parse tree produced by TypeLangParser#listexp.
    def exitListexp(self, ctx:TypeLangParser.ListexpContext):
        pass


    # Enter a parse tree produced by TypeLangParser#nullexp.
    def enterNullexp(self, ctx:TypeLangParser.NullexpContext):
        pass

    # Exit a parse tree produced by TypeLangParser#nullexp.
    def exitNullexp(self, ctx:TypeLangParser.NullexpContext):
        pass


    # Enter a parse tree produced by TypeLangParser#strexp.
    def enterStrexp(self, ctx:TypeLangParser.StrexpContext):
        pass

    # Exit a parse tree produced by TypeLangParser#strexp.
    def exitStrexp(self, ctx:TypeLangParser.StrexpContext):
        pass


    # Enter a parse tree produced by TypeLangParser#boolexp.
    def enterBoolexp(self, ctx:TypeLangParser.BoolexpContext):
        pass

    # Exit a parse tree produced by TypeLangParser#boolexp.
    def exitBoolexp(self, ctx:TypeLangParser.BoolexpContext):
        pass


    # Enter a parse tree produced by TypeLangParser#lambdaexp.
    def enterLambdaexp(self, ctx:TypeLangParser.LambdaexpContext):
        pass

    # Exit a parse tree produced by TypeLangParser#lambdaexp.
    def exitLambdaexp(self, ctx:TypeLangParser.LambdaexpContext):
        pass


    # Enter a parse tree produced by TypeLangParser#callexp.
    def enterCallexp(self, ctx:TypeLangParser.CallexpContext):
        pass

    # Exit a parse tree produced by TypeLangParser#callexp.
    def exitCallexp(self, ctx:TypeLangParser.CallexpContext):
        pass


    # Enter a parse tree produced by TypeLangParser#ifexp.
    def enterIfexp(self, ctx:TypeLangParser.IfexpContext):
        pass

    # Exit a parse tree produced by TypeLangParser#ifexp.
    def exitIfexp(self, ctx:TypeLangParser.IfexpContext):
        pass


    # Enter a parse tree produced by TypeLangParser#switchexp.
    def enterSwitchexp(self, ctx:TypeLangParser.SwitchexpContext):
        pass

    # Exit a parse tree produced by TypeLangParser#switchexp.
    def exitSwitchexp(self, ctx:TypeLangParser.SwitchexpContext):
        pass


    # Enter a parse tree produced by TypeLangParser#lessexp.
    def enterLessexp(self, ctx:TypeLangParser.LessexpContext):
        pass

    # Exit a parse tree produced by TypeLangParser#lessexp.
    def exitLessexp(self, ctx:TypeLangParser.LessexpContext):
        pass


    # Enter a parse tree produced by TypeLangParser#equalexp.
    def enterEqualexp(self, ctx:TypeLangParser.EqualexpContext):
        pass

    # Exit a parse tree produced by TypeLangParser#equalexp.
    def exitEqualexp(self, ctx:TypeLangParser.EqualexpContext):
        pass


    # Enter a parse tree produced by TypeLangParser#greaterexp.
    def enterGreaterexp(self, ctx:TypeLangParser.GreaterexpContext):
        pass

    # Exit a parse tree produced by TypeLangParser#greaterexp.
    def exitGreaterexp(self, ctx:TypeLangParser.GreaterexpContext):
        pass


    # Enter a parse tree produced by TypeLangParser#refexp.
    def enterRefexp(self, ctx:TypeLangParser.RefexpContext):
        pass

    # Exit a parse tree produced by TypeLangParser#refexp.
    def exitRefexp(self, ctx:TypeLangParser.RefexpContext):
        pass


    # Enter a parse tree produced by TypeLangParser#derefexp.
    def enterDerefexp(self, ctx:TypeLangParser.DerefexpContext):
        pass

    # Exit a parse tree produced by TypeLangParser#derefexp.
    def exitDerefexp(self, ctx:TypeLangParser.DerefexpContext):
        pass


    # Enter a parse tree produced by TypeLangParser#assignexp.
    def enterAssignexp(self, ctx:TypeLangParser.AssignexpContext):
        pass

    # Exit a parse tree produced by TypeLangParser#assignexp.
    def exitAssignexp(self, ctx:TypeLangParser.AssignexpContext):
        pass


    # Enter a parse tree produced by TypeLangParser#freeexp.
    def enterFreeexp(self, ctx:TypeLangParser.FreeexpContext):
        pass

    # Exit a parse tree produced by TypeLangParser#freeexp.
    def exitFreeexp(self, ctx:TypeLangParser.FreeexpContext):
        pass


    # Enter a parse tree produced by TypeLangParser#type.
    def enterType(self, ctx:TypeLangParser.TypeContext):
        pass

    # Exit a parse tree produced by TypeLangParser#type.
    def exitType(self, ctx:TypeLangParser.TypeContext):
        pass


    # Enter a parse tree produced by TypeLangParser#booleantype.
    def enterBooleantype(self, ctx:TypeLangParser.BooleantypeContext):
        pass

    # Exit a parse tree produced by TypeLangParser#booleantype.
    def exitBooleantype(self, ctx:TypeLangParser.BooleantypeContext):
        pass


    # Enter a parse tree produced by TypeLangParser#unittype.
    def enterUnittype(self, ctx:TypeLangParser.UnittypeContext):
        pass

    # Exit a parse tree produced by TypeLangParser#unittype.
    def exitUnittype(self, ctx:TypeLangParser.UnittypeContext):
        pass


    # Enter a parse tree produced by TypeLangParser#numtype.
    def enterNumtype(self, ctx:TypeLangParser.NumtypeContext):
        pass

    # Exit a parse tree produced by TypeLangParser#numtype.
    def exitNumtype(self, ctx:TypeLangParser.NumtypeContext):
        pass


    # Enter a parse tree produced by TypeLangParser#listtype.
    def enterListtype(self, ctx:TypeLangParser.ListtypeContext):
        pass

    # Exit a parse tree produced by TypeLangParser#listtype.
    def exitListtype(self, ctx:TypeLangParser.ListtypeContext):
        pass


    # Enter a parse tree produced by TypeLangParser#pairtype.
    def enterPairtype(self, ctx:TypeLangParser.PairtypeContext):
        pass

    # Exit a parse tree produced by TypeLangParser#pairtype.
    def exitPairtype(self, ctx:TypeLangParser.PairtypeContext):
        pass


    # Enter a parse tree produced by TypeLangParser#reft.
    def enterReft(self, ctx:TypeLangParser.ReftContext):
        pass

    # Exit a parse tree produced by TypeLangParser#reft.
    def exitReft(self, ctx:TypeLangParser.ReftContext):
        pass


    # Enter a parse tree produced by TypeLangParser#stringt.
    def enterStringt(self, ctx:TypeLangParser.StringtContext):
        pass

    # Exit a parse tree produced by TypeLangParser#stringt.
    def exitStringt(self, ctx:TypeLangParser.StringtContext):
        pass


    # Enter a parse tree produced by TypeLangParser#funct.
    def enterFunct(self, ctx:TypeLangParser.FunctContext):
        pass

    # Exit a parse tree produced by TypeLangParser#funct.
    def exitFunct(self, ctx:TypeLangParser.FunctContext):
        pass


