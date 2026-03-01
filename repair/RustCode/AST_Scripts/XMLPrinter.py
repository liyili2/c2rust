from collections import ChainMap
from types import NoneType

from XMLExpVisitor import XMLExpVisitor
from XMLExpParser import XMLExpParser
from XMLProgrammer import *
from ProgramVisitor import ProgramVisitor
import XMLProgrammer


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


def findVar(node: XMLExpParser.VexpContext):
    return node.Identifier().getText()
    # if isinstance(node, ExpParser.Number):
    #    return node.getText()
    # return "None"


class XMLPrinter(ProgramVisitor):

    def __init__(self):
        # self.tenv = tenv
        self.xml_output = ''
        self.indentation = 0

    def visitProgram(self, ctx: XMLProgrammer.QXProgram):
        # This doesn't automatically find the correct one to call, rather it creates an infinite loop
        # I will likely just need to use a case analysis
        re = ""
        for i in range(len(ctx.stmt())):
            elem = ctx.stmt(i)
            re += elem.accept(self) + ";\n"
        return re

        # ctx.accept(self) # This will automatically detect and find the corresponding context to call the visit func of

    def visitFun(self, ctx: XMLProgrammer.QXFun):
        re = ""
        re += ctx.ID() + "("
        for i in range(len(ctx.args())):
            elem = ctx.args(i)
            re += elem.accept(self)
            if i != len(ctx.args()) - 1:
                re += ", "

        re += ")\n"
        re += ctx.stmt().accept(self)
        re += "\n"
        return re

    def visitBlock(self, ctx: XMLProgrammer.QXBlock):
        re = "{\n"
        re += ctx.program().accept(self)
        re += "\n}"
        return re

    def visitLet(self, ctx: XMLProgrammer.QXLet):
        re = "let " + ctx.ID()
        re += ctx.vexp().accept(self)
        return re

    def visitPrint(self, ctx: XMLProgrammer.QXPrint):
        re = "println("
        re += ctx.str() + ", "
        re += ctx.exp().accept(self)
        re += ")"
        return re

    def visitBreak(self, ctx: XMLProgrammer.QXBreak):
        if ctx.vexp() is None:
            return "break"
        else:
            re =  "break" + ctx.vexp().accept(self)
            return re

    def visitIfStmt(self, ctx: XMLProgrammer.QXIf):
        re = "if " + ctx.vexp().accept(self)
        re += ctx.left().accept(self)
        re += " else " + ctx.right().accept(self)
        return re

    def visitReturn(self, ctx: XMLProgrammer.QXReturn):
        if ctx.vexp() is None:
            return "return"
        else:
            re =  "return" + ctx.vexp().accept(self)
            return re

    def visitLoop(self, ctx: XMLProgrammer.QXLoop):
        re = "loop "+ctx.block()
        return re

    def visitFor(self, ctx: XMLProgrammer.QXFor):
        re = "for " + ctx.ID() + " in "
        re += ctx.vexp().accept(self) + " "
        re += ctx.block().accept(self)
        return re

    def visitBin(self, ctx: XMLProgrammer.QXBin):
        re = "(" + ctx.left().accept(self)
        re += " " + ctx.OP() + " "
        re += ctx.right().accept(self) + ")"
        return re


    def visitRef(self, ctx: XMLProgrammer.QXRef):
        re = "& "+ ctx.next().accept(self)
        return re

    def visitIDExp(self, ctx: XMLProgrammer.QXIDExp):
        re = ctx.ID() + " : " + ctx.type().accept(self)
        return re

    def visitNum(self, ctx: XMLProgrammer.QXNum):
        return str(ctx.num())

    def visitBoolType(self, ctx: XMLProgrammer.Bool):
        return "bool"

