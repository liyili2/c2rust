from collections import ChainMap
from types import NoneType
from XMLExpVisitor import XMLExpVisitor
from XMLExpParser import XMLExpParser


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
    # if isinstance(node, ExpParser.Number):
    #    return node.getText()
    # return "None"


class XMLPrinter(XMLExpVisitor):

    def __init__(self, tenv: ChainMap):
        self.tenv = tenv
        self.xml_output = ''
        self.indentation = 0

    # should do nothing
    def visitSkipexp(self, ctx: ExpParser.SkipexpContext):
        self.xml_output += "  " * self.indentation + "<pexp gate = 'SKIP' "
        x = ""f'{ctx.idexp().Identifier().getText()}\n'""
        y = M_find(x, self.tenv)
        self.xml_output += "type = \'"+str(y)+"\' >\n"
        ctx.idexp().accept(self)
        ctx.vexp().accept(self)
        self.xml_output += "  " * self.indentation + "</pexp>\n"

    # X posi, changed the following for an example
    def visitXexp(self, ctx: ExpParser.XexpContext):
        self.xml_output += "  " * self.indentation + "<pexp gate = 'X' "
        x = ""f'{ctx.idexp().Identifier().getText()}\n'""
        y = M_find(x, self.tenv)
        self.xml_output += "type = \'"+str(y)+"\' >\n"
        ctx.idexp().accept(self)
        ctx.vexp().accept(self)
        self.xml_output += "  " * self.indentation + "</pexp>\n"

    # we will first get the position in st and check if the state is 0 or 1,
    # then decide if we go to recucively call ctx.exp
    def visitCUexp(self, ctx: ExpParser.CuexpContext):
        self.xml_output += "  " * self.indentation + "<pexp gate = 'CU' "
        x = ""f'{ctx.idexp().Identifier().getText()}\n'""
        y = M_find(x, self.tenv)
        self.xml_output += "type = \'"+str(y)+"\' >\n"
        ctx.idexp().accept(self)
        ctx.vexp().accept(self)  # this will pass the visitor to the child of ctx
        ctx.program().accept(self)
        self.xml_output += "  " * self.indentation + "</pexp>\n"

    # my previous rz parsing is wrong
    # it should be RZ q posi
    def visitRzexp(self, ctx: ExpParser.RzexpContext):
        self.xml_output += "  " * self.indentation + "<pexp gate = 'RZ' "
        x = ""f'{ctx.idexp().Identifier().getText()}\n'""
        y = M_find(x, self.tenv)
        self.xml_output += "type = \'"+str(y)+"\' >\n"
        ctx.vexp(0).accept(self)  # I guess then you need to define vexp
        ctx.idexp().accept(self)
        ctx.vexp(1).accept(self)  # this will pass the visitor to the child of ctx
        self.xml_output += "  " * self.indentation + "</pexp>\n"

    # SR n x, now variables are all string, are this OK?
    def visitSrexp(self, ctx: ExpParser.SrexpContext):
        self.xml_output += "  " * self.indentation + "<pexp gate = 'SR' "
        x = ""f'{ctx.idexp().Identifier().getText()}\n'""
        y = M_find(x, self.tenv)
        self.xml_output += "type = \'"+str(y)+"\' >\n"
        ctx.vexp().accept(self)  # I guess then you need to define vexp
        ctx.idexp().accept(self)  # this will pass the visitor to the child of ctx
        self.xml_output += "  " * self.indentation + "</pexp>\n"

    def visitLshiftexp(self, ctx: ExpParser.LshiftexpContext):
        self.xml_output += "  " * self.indentation + "<pexp gate = 'Lshift' "
        x = ""f'{ctx.idexp().Identifier().getText()}\n'""
        y = M_find(x, self.tenv)
        self.xml_output += "type = \'"+str(y)+"\' >\n"
        ctx.idexp().accept(self)  # this will pass the visitor to the child of ctx
        self.xml_output += "  " * self.indentation + "</pexp>\n"

    def visitRshiftexp(self, ctx: ExpParser.RshiftexpContext):
        self.xml_output += "  " * self.indentation + "<pexp gate = 'Rshift' "
        x = ""f'{ctx.idexp().Identifier().getText()}\n'""
        y = M_find(x, self.tenv)
        self.xml_output += "type = \'"+str(y)+"\' >\n"
        ctx.idexp().accept(self)  # this will pass the visitor to the child of ctx
        self.xml_output += "  " * self.indentation + "</pexp>\n"

    def visitRevexp(self, ctx: ExpParser.RevexpContext):
        self.xml_output += "  " * self.indentation + "<pexp gate = 'Rev' "
        x = ""f'{ctx.idexp().Identifier().getText()}\n'""
        y = M_find(x, self.tenv)
        self.xml_output += "type = \'"+str(y)+"\' >\n"
        ctx.idexp().accept(self)  # this will pass the visitor to the child of ctx
        self.xml_output += "  " * self.indentation + "</pexp>\n"


    # actually, we need to change the QFT function
    # the following QFT is only for full QFT, we did not have the case for AQFT
    def visitQftexp(self, ctx: ExpParser.QftexpContext):
        self.xml_output += "  " * self.indentation + "<pexp gate = 'QFT' "
        x = ""f'{ctx.idexp().Identifier().getText()}\n'""
        y = M_find(x, self.tenv)
        self.xml_output += "type = \'"+str(y)+"\' >\n"
        ctx.idexp().accept(self)  # this will pass the visitor to the child of ctx
        ctx.vexp().accept(self)  # I guess then you need to define vexp
        self.xml_output += "  " * self.indentation + "</pexp>\n"

    def visitRqftexp(self, ctx: ExpParser.RqftexpContext):
        self.xml_output += "  " * self.indentation + "<pexp gate = 'RQFT' "
        x = ""f'{ctx.idexp().Identifier().getText()}\n'""
        y = M_find(x, self.tenv)
        self.xml_output += "type = \'"+str(y)+"\' >\n"
        ctx.idexp().accept(self)  # this will pass the visitor to the child of ctx
        ctx.vexp().accept(self)  # I guess then you need to define vexp
        self.xml_output += "  " * self.indentation + "</pexp>\n"


    def visitTerminal(self, node):
        # For leaf nodes
        if node.getSymbol().type == XMLExpParser.Identifier:
            self.xml_output += ""f'{node.getText()}\n'""
        if node.getSymbol().type == XMLExpParser.Number:
            self.xml_output += ""f'{node.getText()}\n'""
        self.xml_output += ""

    # def visit(self, ctx):
    #    if ctx.getChildCount() > 0:
    #        self.visitChildren(ctx)
    #    else:
    #        self.visitTerminal(ctx)

    def getXML(self):
        return self.xml_output
