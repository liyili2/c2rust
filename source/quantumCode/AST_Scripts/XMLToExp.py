from collections import ChainMap
from types import NoneType
from XMLExpVisitor import XMLExpVisitor
from XMLExpParser import XMLExpParser
import sys
sys.path.append('../')
from typechecker import TypeName
from typechecker import Nor
from typechecker import QFT


def M_add(k, x, s: ChainMap):
    if len(s.maps) == 0:
        return ChainMap({k: x})
    else:
        p = s.maps[0]
        k_prime, y = next(iter(p.items()))
        if k < k_prime:
            return ChainMap({k: x}, s)
        elif k == k_prime:
            s.__delitem__(k_prime)
            return ChainMap({k: x}, s)
        else:
            s.__delitem__(k_prime)
            return ChainMap({k_prime: y}, M_add(k, x, s))


def M_find(k, M: ChainMap):
    if len(M.maps) == 0:
        return None
    else:
        p = M.maps[0]
        k_prime, x = next(iter(p.items()))
        if k < k_prime:
            return None
        elif k == k_prime:
            return x
        else:
            M.__delitem__(k_prime)
            return M_find(k, M)

class XMLToExp(XMLExpVisitor):

    def __init__(self):
        self.tenv = ChainMap()

    # Visit a parse tree produced by XMLExpParser#xexp.
    def visitXexp(self, ctx:XMLExpParser.XexpContext):
        x = ctx.Identifier().accept(self)
        if x == "SKIP":
            posi = ctx.nextlevel().accept(self)
            return " SKIP "+posi
        elif x == "X":
            posi = ctx.nextlevel().accept(self)
            return " X "+posi
        elif x == "CU":
            posi = ctx.nextlevel().accept(self)
            return " CU "+posi


    # Visit a parse tree produced by XMLExpParser#vexp.
    def visitVexp(self, ctx:XMLExpParser.VexpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XMLExpParser#nextlevel.
    def visitNextlevel(self, ctx:XMLExpParser.NextlevelContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XMLExpParser#numexp.
    def visitNumexp(self, ctx:XMLExpParser.NumexpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XMLExpParser#typeexp.
    def visitTypeexp(self, ctx:XMLExpParser.TypeexpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by XMLExpParser#boolexp.
    def visitBoolexp(self, ctx:XMLExpParser.BoolexpContext):
        return self.visitChildren(ctx)

    # the only thing that matters will be 48 and 47
    def visitTerminal(self, node):
        if node.getSymbol().type == XMLExpParser.Identifier:
            return node.getText()
        if node.getSymbol().type == XMLExpParser.Number:
            return node.getText()
        return "None"