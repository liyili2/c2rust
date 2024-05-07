# Generated from TypeLang.g4 by ANTLR 4.7.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .TypeLangParser import TypeLangParser
else:
    from TypeLangParser import TypeLangParser

# This class defines a complete generic visitor for a parse tree produced by TypeLangParser.

class TypeLangVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by TypeLangParser#program.
    def visitProgram(self, ctx:TypeLangParser.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeLangParser#exp.
    def visitExp(self, ctx:TypeLangParser.ExpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeLangParser#numexp.
    def visitNumexp(self, ctx:TypeLangParser.NumexpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeLangParser#addexp.
    def visitAddexp(self, ctx:TypeLangParser.AddexpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeLangParser#subexp.
    def visitSubexp(self, ctx:TypeLangParser.SubexpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeLangParser#multexp.
    def visitMultexp(self, ctx:TypeLangParser.MultexpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeLangParser#divexp.
    def visitDivexp(self, ctx:TypeLangParser.DivexpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeLangParser#varexp.
    def visitVarexp(self, ctx:TypeLangParser.VarexpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeLangParser#letexp.
    def visitLetexp(self, ctx:TypeLangParser.LetexpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeLangParser#definedecl.
    def visitDefinedecl(self, ctx:TypeLangParser.DefinedeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeLangParser#carexp.
    def visitCarexp(self, ctx:TypeLangParser.CarexpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeLangParser#cdrexp.
    def visitCdrexp(self, ctx:TypeLangParser.CdrexpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeLangParser#consexp.
    def visitConsexp(self, ctx:TypeLangParser.ConsexpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeLangParser#listexp.
    def visitListexp(self, ctx:TypeLangParser.ListexpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeLangParser#nullexp.
    def visitNullexp(self, ctx:TypeLangParser.NullexpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeLangParser#strexp.
    def visitStrexp(self, ctx:TypeLangParser.StrexpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeLangParser#boolexp.
    def visitBoolexp(self, ctx:TypeLangParser.BoolexpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeLangParser#lambdaexp.
    def visitLambdaexp(self, ctx:TypeLangParser.LambdaexpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeLangParser#callexp.
    def visitCallexp(self, ctx:TypeLangParser.CallexpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeLangParser#ifexp.
    def visitIfexp(self, ctx:TypeLangParser.IfexpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeLangParser#switchexp.
    def visitSwitchexp(self, ctx:TypeLangParser.SwitchexpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeLangParser#lessexp.
    def visitLessexp(self, ctx:TypeLangParser.LessexpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeLangParser#equalexp.
    def visitEqualexp(self, ctx:TypeLangParser.EqualexpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeLangParser#greaterexp.
    def visitGreaterexp(self, ctx:TypeLangParser.GreaterexpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeLangParser#refexp.
    def visitRefexp(self, ctx:TypeLangParser.RefexpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeLangParser#derefexp.
    def visitDerefexp(self, ctx:TypeLangParser.DerefexpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeLangParser#assignexp.
    def visitAssignexp(self, ctx:TypeLangParser.AssignexpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeLangParser#freeexp.
    def visitFreeexp(self, ctx:TypeLangParser.FreeexpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeLangParser#type.
    def visitType(self, ctx:TypeLangParser.TypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeLangParser#booleantype.
    def visitBooleantype(self, ctx:TypeLangParser.BooleantypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeLangParser#unittype.
    def visitUnittype(self, ctx:TypeLangParser.UnittypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeLangParser#numtype.
    def visitNumtype(self, ctx:TypeLangParser.NumtypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeLangParser#listtype.
    def visitListtype(self, ctx:TypeLangParser.ListtypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeLangParser#pairtype.
    def visitPairtype(self, ctx:TypeLangParser.PairtypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeLangParser#reft.
    def visitReft(self, ctx:TypeLangParser.ReftContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeLangParser#stringt.
    def visitStringt(self, ctx:TypeLangParser.StringtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeLangParser#funct.
    def visitFunct(self, ctx:TypeLangParser.FunctContext):
        return self.visitChildren(ctx)



del TypeLangParser