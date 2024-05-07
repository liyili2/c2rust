from collections import ChainMap
from types import NoneType
from ExpVisitor import ExpVisitor
from ExpParser import ExpParser

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


def findVar(node: ExpParser.VexpContext):
    return node.Identifier().getText()
    #if isinstance(node, ExpParser.Number):
    #    return node.getText()
    #return "None"


class XMLVisitor(ExpVisitor):

    def __init__(self, tenv: ChainMap):
        self.tenv = tenv
        self.xml_output = ''
        self.indentation = 0

    def visitProgram(self, ctx):
        self.visitChildren(ctx)

    def visitExp(self, ctx):
        self.visitChildren(ctx)

    def visitVexp(self, ctx):
        self.xml_output += "  " * self.indentation + "<Vexp>\n"
        self.indentation += 1
        self.visitChildren(ctx)
        self.indentation -= 1
        self.xml_output += "  " * self.indentation + "</Vexp>\n"

    def visitBexp(self, ctx):
        self.xml_output += "  " * self.indentation + "<Bexp>\n"
        self.indentation += 1
        self.visitChildren(ctx)
        self.indentation -= 1
        self.xml_output += "  " * self.indentation + "</Bexp>\n"

    def visitPosiexp(self, ctx):
        self.xml_output += "  " * self.indentation + "<Pos>\n"
        self.indentation += 1
        self.visitChildren(ctx)
        self.indentation -= 1
        self.xml_output += "  " * self.indentation + "</Pos>\n"

    def visitSkipexp(self, ctx):
        self.xml_output += "  " * self.indentation + "<SKIP>\n"
        self.indentation += 1
        self.visitChildren(ctx)
        self.indentation -= 1
        self.xml_output += "  " * self.indentation + "</SKIP>\n"

    def visitXgexp(self, ctx: ExpParser.XgexpContext):
        x = findVar(ctx.posiexp().vexp(0))
        self.xml_output += "  " * self.indentation + "<X>\n"
        self.indentation += 1
        self.xml_output += "<type>" + str(M_find(x, self.tenv)) + "</type>"
        self.visitChildren(ctx)
        self.indentation -= 1
        self.xml_output += "  " * self.indentation + "</X>\n"

    def visitCuexp(self, ctx):
        x = findVar(ctx.posiexp().vexp(0))
        self.xml_output += "  " * self.indentation + "<CU>\n"
        self.indentation += 1
        self.xml_output += "<type>" + str(M_find(x, self.tenv)) + "</type>"
        self.visitChildren(ctx)
        self.indentation -= 1
        self.xml_output += "  " * self.indentation + "</CU>\n"

    def visitRzexp(self, ctx):
        x = findVar(ctx.posiexp().vexp(0))
        self.xml_output += "  " * self.indentation + "<RZ>\n"
        self.indentation += 1
        self.xml_output += "<type>" + str(M_find(x, self.tenv)) + "</type>"
        self.visitChildren(ctx)
        self.indentation -= 1
        self.xml_output += "  " * self.indentation + "</RZ>\n"

    def visitSrexp(self, ctx):
        x = findVar(ctx.vexp(1))
        self.xml_output += "  " * self.indentation + "<SR>\n"
        self.indentation += 1
        self.xml_output += "<type>" + str(M_find(x, self.tenv)) + "</type>"
        self.visitChildren(ctx)
        self.indentation -= 1
        self.xml_output += "  " * self.indentation + "</SR>\n"

    def visitLshiftexp(self, ctx):
        x = findVar(ctx.vexp())
        self.xml_output += "  " * self.indentation + "<Lshift>\n"
        self.indentation += 1
        self.xml_output += "<type>" + str(M_find(x, self.tenv)) + "</type>"
        self.visitChildren(ctx)
        self.indentation -= 1
        self.xml_output += "  " * self.indentation + "</Lshift>\n"

    def visitRshiftexp(self, ctx):
        x = findVar(ctx.vexp())
        self.xml_output += "  " * self.indentation + "<Rshift>\n"
        self.indentation += 1
        self.xml_output += "<type>" + str(M_find(x, self.tenv)) + "</type>"
        self.visitChildren(ctx)
        self.indentation -= 1
        self.xml_output += "  " * self.indentation + "</Rshift>\n"

    def visitRevexp(self, ctx):
        x = findVar(ctx.vexp())
        self.xml_output += "  " * self.indentation + "<Rev>\n"
        self.indentation += 1
        self.xml_output += "<type>" + str(M_find(x, self.tenv)) + "</type>"
        self.visitChildren(ctx)
        self.indentation -= 1
        self.xml_output += "  " * self.indentation + "</Rev>\n"

    def visitQftexp(self, ctx):
        x = findVar(ctx.vexp(0))
        self.xml_output += "  " * self.indentation + "<QFT>\n"
        self.indentation += 1
        self.xml_output += "<type>" + str(M_find(x, self.tenv)) + "</type>"
        self.visitChildren(ctx)
        self.indentation -= 1
        self.xml_output += "  " * self.indentation + "</QFT>\n"

    def visitRqftexp(self, ctx):
        x = findVar(ctx.vexp(0))
        self.xml_output += "  " * self.indentation + "<RQFT>\n"
        self.indentation += 1
        self.xml_output += "<type>" + str(M_find(x, self.tenv)) + "</type>"
        self.visitChildren(ctx)
        self.indentation -= 1
        self.xml_output += "  " * self.indentation + "</RQFT>\n"

    def visitNumexp(self, ctx):
        self.xml_output += "  " * self.indentation + "<Numexp>\n"
        self.indentation += 1
        self.visitChildren(ctx)
        self.indentation -= 1
        self.xml_output += "  " * self.indentation + "</Numexp>\n"

    def visitAddexp(self, ctx):
        self.xml_output += "  " * self.indentation + "<Addexp>\n"
        self.indentation += 1
        self.visitChildren(ctx)
        self.indentation -= 1
        self.xml_output += "  " * self.indentation + "</Addexp>\n"

    def visitSubexp(self, ctx):
        self.xml_output += "  " * self.indentation + "<Subexp>\n"
        self.indentation += 1
        self.visitChildren(ctx)
        self.indentation -= 1
        self.xml_output += "  " * self.indentation + "</Subexp>\n"

    def visitMultexp(self, ctx):
        self.xml_output += "  " * self.indentation + "<Multexp>\n"
        self.indentation += 1
        self.visitChildren(ctx)
        self.indentation -= 1
        self.xml_output += "  " * self.indentation + "</Multexp>\n"

    def visitDivexp(self, ctx):
        self.xml_output += "  " * self.indentation + "<Divexp>\n"
        self.indentation += 1
        self.visitChildren(ctx)
        self.indentation -= 1
        self.xml_output += "  " * self.indentation + "</Divexp>\n"

    def visitModexp(self, ctx):
        self.xml_output += "  " * self.indentation + "<Modexp>\n"
        self.indentation += 1
        self.visitChildren(ctx)
        self.indentation -= 1
        self.xml_output += "  " * self.indentation + "</Modexp>\n"

    def visitExpexp(self, ctx):
        self.xml_output += "  " * self.indentation + "<Expexp>\n"
        self.indentation += 1
        self.visitChildren(ctx)
        self.indentation -= 1
        self.xml_output += "  " * self.indentation + "</Expexp>\n"

    def visitVarexp(self, ctx):
        self.xml_output += "  " * self.indentation + "<Varexp>\n"
        self.indentation += 1
        self.visitChildren(ctx)
        self.indentation -= 1
        self.xml_output += "  " * self.indentation + "</Varexp>\n"

    def visitLetexp(self, ctx):
        self.xml_output += "  " * self.indentation + "<Letexp>\n"
        self.indentation += 1
        self.visitChildren(ctx)
        self.indentation -= 1
        self.xml_output += "  " * self.indentation + "</Letexp>\n"

    def visitMatchexp(self, ctx):
        self.xml_output += "  " * self.indentation + "<Matchexp>\n"
        self.indentation += 1
        self.visitChildren(ctx)
        self.indentation -= 1
        self.xml_output += "  " * self.indentation + "</Matchexp>\n"

    def visitBoolexp(self, ctx):
        self.xml_output += "  " * self.indentation + "<Boolexp>\n"
        self.indentation += 1
        self.visitChildren(ctx)
        self.indentation -= 1
        self.xml_output += "  " * self.indentation + "</Boolexp>\n"

    def visitCallexp(self, ctx):
        self.xml_output += "  " * self.indentation + "<Callexp>\n"
        self.indentation += 1
        self.visitChildren(ctx)
        self.indentation -= 1
        self.xml_output += "  " * self.indentation + "</Callexp>\n"

    def visitIfexp(self, ctx):
        self.xml_output += "  " * self.indentation + "<Ifexp>\n"
        self.indentation += 1
        self.visitChildren(ctx)
        self.indentation -= 1
        self.xml_output += "  " * self.indentation + "</Ifexp>\n"

    def visitLessexp(self, ctx):
        self.xml_output += "  " * self.indentation + "<Lessexp>\n"
        self.indentation += 1
        self.visitChildren(ctx)
        self.indentation -= 1
        self.xml_output += "  " * self.indentation + "</Lessexp>\n"

    def visitEqualexp(self, ctx):
        self.xml_output += "  " * self.indentation + "<Equalexp>\n"
        self.indentation += 1
        self.visitChildren(ctx)
        self.indentation -= 1
        self.xml_output += "  " * self.indentation + "</Equalexp>\n"

    def visitGreaterexp(self, ctx):
        self.xml_output += "  " * self.indentation + "<Greaterexp>\n"
        self.indentation += 1
        self.visitChildren(ctx)
        self.indentation -= 1
        self.xml_output += "  " * self.indentation + "</Greaterexp>\n"

    def visitAndexp(self, ctx):
        self.xml_output += "  " * self.indentation + "<Andexp>\n"
        self.indentation += 1
        self.visitChildren(ctx)
        self.indentation -= 1
        self.xml_output += "  " * self.indentation + "</Andexp>\n"

    def visitOrexp(self, ctx):
        self.xml_output += "  " * self.indentation + "<Orexp>\n"
        self.indentation += 1
        self.visitChildren(ctx)
        self.indentation -= 1
        self.xml_output += "  " * self.indentation + "</Orexp>\n"

    def visitTypea(self, ctx):
        self.xml_output += "  " * self.indentation + "<Typea>\n"
        self.indentation += 1
        self.visitChildren(ctx)
        self.indentation -= 1
        self.xml_output += "  " * self.indentation + "</Typea>\n"

    def visitBooleantype(self, ctx):
        self.xml_output += "  " * self.indentation + "<Booleantype>\n"
        self.indentation += 1
        self.visitChildren(ctx)
        self.indentation -= 1
        self.xml_output += "  " * self.indentation + "</Booleantype>\n"

    def visitNumtype(self, ctx):
        self.xml_output += "  " * self.indentation + "<Numtype>\n"
        self.indentation += 1
        self.visitChildren(ctx)
        self.indentation -= 1
        self.xml_output += "  " * self.indentation + "</Numtype>\n"

    def visitPairtype(self, ctx):
        self.xml_output += "  " * self.indentation + "<Pairtype>\n"
        self.indentation += 1
        self.visitChildren(ctx)
        self.indentation -= 1
        self.xml_output += "  " * self.indentation + "</Pairtype>\n"

    def visitFunct(self, ctx):
        self.xml_output += "  " * self.indentation + "<Funct>\n"
        self.indentation += 1
        self.visitChildren(ctx)
        self.indentation -= 1
        self.xml_output += "  " * self.indentation + "</Funct>\n"

    # the following visitChildren can be reomved,
    # Antlr4 has its own implementation of visitChildren
    # def visitChildren(self, ctx):
    #    for child in ctx.children:
    #        self.visit(child)

    def visitTerminal(self, node):
        # For leaf nodes
        if node.getSymbol().type == ExpParser.Identifier:
            self.xml_output += ""f'{node.getText()}\n'""
        if node.getSymbol().type == ExpParser.Number:
            self.xml_output += ""f'{node.getText()}\n'""
        self.xml_output += ""

    # def visit(self, ctx):
    #    if ctx.getChildCount() > 0:
    #        self.visitChildren(ctx)
    #    else:
    #        self.visitTerminal(ctx)

    def getXML(self):
        return "<program>" + self.xml_output + "</program>"
