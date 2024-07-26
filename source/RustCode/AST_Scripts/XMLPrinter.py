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


def findVar(node: XMLExpParser.VexpContext):
    return node.Identifier().getText()
    # if isinstance(node, ExpParser.Number):
    #    return node.getText()
    # return "None"


class XMLPrinter(XMLExpVisitor):

    def __init__(self):
        # self.tenv = tenv
        self.xml_output = ''
        self.indentation = 0

    def visitProgram(self, ctx: XMLExpParser.ProgramContext):
        # This doesn't automatically find the correct one to call, rather it creates an infinite loop
        # I will likely just need to use a case analysis
        if ctx.letstmt() is not None:
            ctx.letstmt().accept(self)
        elif ctx.exp() is not None:
            ctx.exp().accept(self)
        elif ctx.printstmt() is not None:
            ctx.printstmt().accept(self)
        elif ctx.blockstmt() is not None:
            ctx.blockstmt().accept(self)
        elif ctx.ifstmt() is not None:
            ctx.ifstmt().accept(self)
        elif ctx.breakstmt() is not None:
            ctx.breakstmt().accept(self)
        elif ctx.returnstmt() is not None:
            ctx.returnstmt().accept(self)
        elif ctx.loopstmt() is not None:
            ctx.loopstmt().accept(self)
        elif ctx.forstmt() is not None:
            ctx.forstmt().accept(self)

        # ctx.accept(self) # This will automatically detect and find the corresponding context to call the visit func of

    def visitBlockstmt(self, ctx: XMLExpParser.BlockstmtContext):
        self.xml_output += "  " * self.indentation + "<stmt type = block>"
        # x = ""f'{ctx.Block().getText()}\n'""
        # y = M_find(x, self.tenv) # This may not be needed
        # self.xml_output += "type = \'"+str(y)+"\' >\n"
        i = 0
        while ctx.program(i) is not None:
            ctx.program(i).accept(self)
            i += 1
        self.xml_output += "  " * self.indentation + "</stmt>\n"

    def visitLetstmt(self, ctx: XMLExpParser.LetstmtContext):
        self.xml_output += "  " * self.indentation + "<stmt type = let>"
        # x = ""f'{ctx.Let().getText()}\n'""
        # y = M_find(x, self.tenv)
        # self.xml_output += "type = \'"+str(y)+"\' >\n"
        ctx.idexp().accept(self)
        ctx.exp().accept(self)
        self.xml_output += "  " * self.indentation + "</stmt>\n"

    def visitPrintstmt(self, ctx: XMLExpParser.PrintstmtContext):
        self.xml_output += "  " * self.indentation + "<stmt type = print>"
        # x = ""f'{ctx.Print().getText()}\n'""
        # y = M_find(x, self.tenv)
        # self.xml_output += "type = \'"+str(y)+"\' >\n"
        ctx.stringval().accept(self)
        ctx.exp().accept(self)
        self.xml_output += "  " * self.indentation + "</stmt>\n"

    def visitIfstmt(self, ctx: XMLExpParser.IfstmtContext):
        self.xml_output += "  " * self.indentation + "<stmt type = if>"
        # x = ""f'{ctx.IF().getText()}\n'""
        # y = M_find(x, self.tenv)
        # self.xml_output += "type = \'"+str(y)+"\' >\n"
        ctx.vexp().accept(self)
        ctx.blockstmt().accept(self)
        ctx.blockstmt().accept(self)
        self.xml_output += "  " * self.indentation + "</stmt>\n"

    def visitBreakstmt(self, ctx: XMLExpParser.BreakstmtContext):
        self.xml_output += "  " * self.indentation + "<stmt type = break>"
        # x = ""f'{ctx.Break().getText()}\n'""
        # y = M_find(x, self.tenv)
        # self.xml_output += "type = \'"+str(y)+"\' >\n"
        if ctx.vexp() is not None:
            ctx.vexp().accept(self)
        self.xml_output += "  " * self.indentation + "</stmt>\n"

    def visitReturnstmt(self, ctx: XMLExpParser.ReturnstmtContext):
        self.xml_output += "  " * self.indentation + "<stmt type = return>"
        # x = ""f'{ctx.Return().getText()}\n'""
        # y = M_find(x, self.tenv)
        # self.xml_output += "type = \'"+str(y)+"\' >\n"
        if ctx.vexp() is not None:
            ctx.vexp().accept(self)
        self.xml_output += "  " * self.indentation + "</stmt>\n"

    def visitLoopstmt(self, ctx: XMLExpParser.LoopstmtContext):
        self.xml_output += "  " * self.indentation + "<stmt type = loop>"
        # x = ""f'{ctx.Loop().getText()}\n'""
        # y = M_find(x, self.tenv)
        # self.xml_output += "type = \'"+str(y)+"\' >\n"
        ctx.blockstmt().accept(self)
        self.xml_output += "  " * self.indentation + "</stmt>\n"

    def visitForstmt(self, ctx: XMLExpParser.ForstmtContext):
        self.xml_output += "  " * self.indentation + "<stmt type = for>"
        # x = ""f'{ctx.For().getText()}\n'""
        # y = M_find(x, self.tenv)
        # self.xml_output += "type = \'" + str(y) + "\' >\n"
        ctx.idexp().accept(self)
        ctx.vexp().accept(self)
        ctx.blockstmt().accept(self)
        self.xml_output += "  " * self.indentation + "</stmt>\n"

    def visitExp(self, ctx: XMLExpParser.ExpContext):
        ctx.vexp().accept(self)

    def visitIdexp(self, ctx: XMLExpParser.IdexpContext):
        self.xml_output += "  " * self.indentation + "<id>"
        # x = ""f'{ctx.Identifier().getText()}\n'""
        # y = M_find(x, self.tenv)
        self.xml_output += " \'" + ctx.Identifier().getText() + "\' \n"
        self.xml_output += "  " * self.indentation + "</id>\n"

    def visitStringval(self, ctx: XMLExpParser.StringvalContext):
        self.xml_output += "  " * self.indentation + "<value>"
        # x = ""f'{ctx.StrLiteral().getText()}\n'""
        # y = M_find(x, self.tenv)
        self.xml_output += " \'" + ctx.StrLiteral().getText() + "\' \n"
        self.xml_output += "  " * self.indentation + "</value>\n"

    def visitVexp(self, ctx:XMLExpParser.VexpContext):
        ctx.accept(self)

    def visitNumexp(self, ctx:XMLExpParser.NumexpContext):
        self.xml_output += "  " * self.indentation + "<num>"
        neg = ""
        if ctx.Minus() is not None:
            neg += '-'
        # x = ""f'{ctx.Number().getText()}\n'""
        # y = M_find(x, self.tenv)
        self.xml_output += " \'" + neg + ctx.Number().getText() + "\' \n"
        self.xml_output += "  " * self.indentation + "</num>\n"

    def visitBinexp(self, ctx:XMLExpParser.BinexpContext):
        self.xml_output += "  " * self.indentation + "<vexp op = "
        self.xml_output += ""f'{ctx.op().accept(self).getText()}>\n'""
        ctx.vexp().accept(self)
        ctx.vexp().accept(self)
        self.xml_output += "  " * self.indentation + "</vexp>\n"

    def visitBoolexp(self, ctx: XMLExpParser.BoolexpContext):
        self.xml_output += "  " * self.indentation + "<bool>"
        if ctx.TrueLiteral() is not None:
            x = ""f'{ctx.TrueLiteral().getText()}'""
        else:
            x = ""f'{ctx.FalseLiteral().getText()}'""
        # y = M_find(x, self.tenv)
        self.xml_output += " \'" + x + "\' \n"
        self.xml_output += "  " * self.indentation + "</bool>\n"



    # Old code

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
