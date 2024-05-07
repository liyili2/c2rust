# type checker
from enum import Enum
from collections import ChainMap
from types import NoneType

from antlr4 import ParserRuleContext

from XMLExpParser import *
from XMLExpVisitor import *

class TypeName:
    pass  # TODO


class Nor(TypeName):

    def __str__(self):
        return "Nor"


class Phi(TypeName):

    def __init__(self, n: int):
        self.n = n
        #self.r2 = r2

    def get_num(self):
        return n

    def __str__(self):
        return "Phi"

class TypeInfer(XMLExpVisitor):

    # x, y, z, env : ChainMap{ x: n, y : m, z : v} , n m v are nat numbers 100, 100, 100, eg {x : 128}
    # st state map, {x : v1, y : v2 , z : v3}, eg {x : v1}: v1,
    # st {x : v1} --> Coq_nval case: v1 is a ChainMap of Coq_nval
    # v1 --> 128 length array v1: {0 : Coq_nval, 1 : Coq_nval, 2 : Coq_nval, ...., 127 : Coq_nval}, 2^128
    # x --> v1 --> cal(v1) --> integer
    # Coq_nval(b,r) b == |0> | |1>, r == e^(2 pi i * 1 / n), r = 0 Coq_nval(b, 0)
    # x -> v1 ----> run simulator -----> v2 ---> calInt(v2,128) == (x + 2^10) % 2^128
    def __init__(self, tenv: dict, env: dict):
        self.tenv = tenv
        self.env = env
        # self.rmax = rmax rmax is M_find(x,env), a map from var to int

    def get_type_env(self):
        return self.tenv

    # should do nothing
    def visitSkipexp(self, ctx: XMLExpParser.SkipexpContext):
        x = ctx.idexp().accept(self)
        p = ctx.vexp().accept(self)  # this will pass the visitor to the child of ctx
        return p < self.env.get(x)

    # X posi, changed the following for an example
    def visitXexp(self, ctx: XMLExpParser.XexpContext):
        x = ctx.idexp().accept(self)
        p = ctx.vexp().accept(self)  # this will pass the visitor to the child of ctx
        return p < self.env.get(x) and str(self.tenv.get(x)) == "Nor"
        # print(M_find(x, self.st))

    # we will first get the position in st and check if the state is 0 or 1,
    # then decide if we go to recucively call ctx.exp
    def visitCUexp(self, ctx: XMLExpParser.CuexpContext):
        x = ctx.idexp().accept(self)
        p = ctx.vexp().accept(self)  # this will pass the visitor to the child of ctx
        return p < self.env.get(x) and str(self.tenv.get(x)) == "Nor" and ctx.program().accept(self)

    # my previous rz parsing is wrong
    # it should be RZ q posi
    def visitRzexp(self, ctx: XMLExpParser.RzexpContext):
        q = int(ctx.vexp(0).accept(self))  # I guess then you need to define vexp
        # we can first define the var and integer case
        # I guess Identifier and int are all terminal
        # does it means that we do not need to define anything?
        x = ctx.idexp().accept(self)
        p = ctx.vexp(1).accept(self)  # this will pass the visitor to the child of ctx
        return p < self.env.get(x) and q < self.env.get(x) and str(self.tenv.get(x)) == "Nor"

    # SR n x, now variables are all string, are this OK?
    def visitSrexp(self, ctx: XMLExpParser.SrexpContext):
        n = int(ctx.vexp().accept(self))
        x = ctx.idexp().accept(self)
        return n <= self.env.get(x).get_num() <= self.env.get(x) and str(self.tenv.get(x)) == "Phi"

    def visitLshiftexp(self, ctx: XMLExpParser.LshiftexpContext):
        x = ctx.idexp().accept(self)
        return str(self.tenv.get(x)) == "Nor"

    def visitRshiftexp(self, ctx: XMLExpParser.RshiftexpContext):
        x = ctx.idexp().accept(self)
        return str(self.tenv.get(x)) == "Nor"

    def visitRevexp(self, ctx: XMLExpParser.RevexpContext):
        x = ctx.idexp().accept(self)
        return str(self.tenv.get(x)) == "Nor"

    # actually, we need to change the QFT function
    # the following QFT is only for full QFT, we did not have the case for AQFT
    def visitQftexp(self, ctx: XMLExpParser.QftexpContext):
        x = ctx.idexp().accept(self)
        b = int(ctx.vexp().accept(self))
        rb = b <= self.env.get(x) and str(self.tenv.get(x)) == "Nor"
        self.tenv.update({x: Phi(self.env.get(x)-b)})
        return rb

    def visitRqftexp(self, ctx: XMLExpParser.RqftexpContext):
        x = ctx.idexp().accept(self)
        b = int(ctx.vexp().accept(self))
        rb = b <= self.env.get(x) and str(self.tenv.get(x)) == "Phi"
        self.tenv.update({x: Nor})
        return rb

    def visit(self, ctx: ParserRuleContext):
        if ctx.getChildCount() > 0:
            return self.visitChildren(ctx)
        else:
            return self.visitTerminal(ctx)

    def visitIdexp(self, ctx: XMLExpParser.IdexpContext):
        return ctx.Identifier().accept(self)

    # Visit a parse tree produced by XMLExpParser#vexp.
    def visitVexp(self, ctx: XMLExpParser.VexpContext):
        return ctx.numexp().accept(self)

    # the only thing that matters will be 48 and 47
    def visitTerminal(self, node):
        if node.getSymbol().type == XMLExpParser.Identifier:
            return node.getText()
        if node.getSymbol().type == XMLExpParser.Number:
            return int(node.getText())
        return "None"
