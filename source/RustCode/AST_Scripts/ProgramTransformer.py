# type checker
import copy
from enum import Enum
from collections import ChainMap
from types import NoneType

from antlr4 import ParserRuleContext

from XMLExpLexer import *
from XMLExpVisitor import *
from XMLExpParser import *
#from XMLTypeSearch import *
from XMLProgrammer import *

class ProgramTransformer(XMLExpVisitor):

    def visitProgram(self, ctx: XMLExpParser.ProgramContext):
        i = 0
        tmp = []
        while ctx.stmt(i) is not None:
            v = self.visitStmt(ctx.stmt(i))
            tmp.append(v)
            i += 1
        return QXProgram(tmp)
    
    def visitStmt(self, ctx: XMLExpParser.StmtContext):
        if ctx.functionstmt() is not None:
            return self.visitFunctionstmt(ctx.functionstmt())
        elif ctx.letstmt() is not None:
            return self.visitLetstmt(ctx.letstmt())
        elif ctx.exp() is not None:
            return self.visitExp(ctx.exp())
        elif ctx.ifstmt() is not None:
            return self.visitIfstmt(ctx.ifstmt())
        elif ctx.printstmt() is not None:
            return self.visitPrintstmt(ctx.printstmt())
        elif ctx.blockstmt() is not None:
            return self.visitBlockstmt(ctx.blockstmt())
        elif ctx.breakstmt() is not None:
            return self.visitBreakstmt(ctx.breakstmt())
        elif ctx.returnstmt() is not None:
            return self.visitReturnstmt(ctx.returnstmt())
        elif ctx.loopstmt() is not None:
            return self.visitLoopstmt(ctx.loopstmt())
        elif ctx.forstmt() is not None:
            return self.visitForstmt(ctx.forstmt())

    def visitFunctionstmt(self, ctx:XMLExpParser.FunctionstmtContext):
        i=0
        x = ctx.Identifier()
        tmp = []
        while ctx.parameters().idexp(i) is not None:          
    #        print('params', ctx.parameters(), i, ctx.parameters().idexp(i)) 
            v = ctx.parameters().idexp(i).accept(self)
            tmp.append(v)
            i += 1
        exp = ctx.blockstmt().accept(self)
 #       print('\n funstmt_in_transformer', x, type(x), tmp, exp)
        return QXFun(x,tmp,exp)


    def visitBlockstmt(self, ctx: XMLExpParser.BlockstmtContext):
        v = self.visitProgram(ctx.program())
#        print( '\n blockstmt_in_transformer', type(v), v.exps)
        return QXBlock(v)
     

    def visitPrintstmt(self, ctx: XMLExpParser.PrintstmtContext):
        s = ctx.stringval().accept(self)
        if ctx.exp() is not None:
            e = ctx.exp().accept(self)
    #        print('\n printstatement_in_transformer', s, e, type(QXPrint(s,e)))
            return QXPrint(s,e)
        else: return QXPrint(s)


    # def visitAtype(self, ctx: XMLExpParser.AtypeContext):
    #     if ctx.Nat() is not None:
    #         return Nat()
    #     elif ctx.Qt() is not None:
    #         v = self.visitElement(ctx.element(0))
    #         return Qty(v)
    #     elif ctx.Nor() is not None:
    #         v = self.visitElement(ctx.element(0))
    #         return Qty(v, "Nor")
    #     elif ctx.Phi() is not None:
    #         v = self.visitElement(ctx.element(0))
    #         v1 = v = self.visitElement(ctx.element(1))
    #         return Qty(v, "Phi", v1)
    #     return Nat()

    def visitLetstmt(self, ctx: XMLExpParser.LetstmtContext):
        f = ctx.Identifier()
        fv = self.visitExp(ctx.exp())
        return QXLet(f.getText(), fv)

    def visitIfstmt(self, ctx:XMLExpParser.IfstmtContext):
        f = self.visitVexp(ctx.vexp())
        left = self.visitBlockexp(ctx.blockstmt(0))
        right = self.visitBlockexp(ctx.blockstmt(1))
        return QXIf(f,left,right)

    def visitBreakstmt(self, ctx:XMLExpParser.BreakstmtContext):
        v = None
        if ctx.vexp() is not None:
            v = ctx.vexp().accept(self)
        return QXBreak(v)

    def visitReturnstmt(self, ctx:XMLExpParser.ReturnstmtContext):
        v = None
        if ctx.vexp() is not None:
            v = ctx.vexp().accept(self)
        return QXReturn(v)

    def visitLoopstmt(self, ctx:XMLExpParser.LoopstmtContext):
        e = ctx.blockstmt().accept(self)
        return QXLoop(e)

    # should do nothing
    def visitForstmt(self, ctx:XMLExpParser.ForstmtContext):

        s = ctx.Identifier()
        r = ctx.range_expr().accept(self)
        e = ctx.blockstmt().accept(self)
#        print('\n forstmt_in_transformer', s, r, e)
        return QXFor(s.getText(), r, e)
    

    def visitExp(self, ctx:XMLExpParser.ExpContext):
        if ctx.vexp() is not None:
            return self.visitVexp(ctx.vexp())
        elif ctx.funccallexp() is not None:
            return self.visitFunccallexp(ctx.funccallexp())
        elif ctx.macroexp() is not None:
            return self.visitMacroexp(ctx.macroexp())
        
    def visitRange_expr(self, ctx: XMLExpParser.Range_exprContext):
        s = self.visitVexp(ctx.vexp(0))
        e = self.visitVexp(ctx.vexp(1))
#        print('\n range_exp_in_transformer', s, e)
        return Range_expr(s, e)

    # X posi, changed the following for an example
    def visitStringval(self, ctx:XMLExpParser.StringvalContext):
        s = ctx.StrLiteral() if ctx.StrLiteral() is not None else ctx.Identifier()
#        print('\n stringval_in_transformer', s.getText())
        return QXString(s.getText())


    def visitIdexp(self, ctx: XMLExpParser.IdexpContext):
        x = ctx.Identifier()
        if ctx.atype() is not None:
            t = self.visitAtype(ctx.atype())
            return QXIDExp(x.getText(), t)
        else:
            return QXIDExp(x.getText(), None)

    # Visit a parse tree produced by XMLExpParser#vexp.
    def visitVexp(self, ctx: XMLExpParser.VexpContext):
        if ctx.idexp() is not None:
            return self.visitIdexp(ctx.idexp())
        if ctx.stringval() is not None:
            v = self.visitStringval(ctx.stringval())
            return QXString(v)
        if ctx.numexp() is not None:
            v = self.visitNumexp(ctx.numexp())
            return QXNum(v)
        if ctx.TrueLiteral() is not None:
            return QXBool(True)
        if ctx.FalseLiteral() is not None:
            return QXBool(False)
        if ctx.vexp(1) is None:
            v = self.visitVexp(ctx.vexp(0))
            return QXRef(v)
        else:
            op = self.visitOp(ctx.op())
            v1 = self.visitVexp(ctx.vexp(0))
            v2 = self.visitVexp(ctx.vexp(1))
            return QXBin(op, v1, v2)
    # the only thing that matters will be 48 and 47

    def visitOp(self, ctx:XMLExpParser.OpContext):
        if ctx.Plus() is not None:
            return ctx.getText()
 #           return "Plus"
        elif ctx.Minus() is not None:
            return ctx.getText()
 #           return "Minus"
        elif ctx.Times() is not None:
            return ctx.getText()
 #           return "Times"
        elif ctx.Div() is not None:
            return "Div"
        elif ctx.Mod() is not None:
            return "Mod"
        elif ctx.Exp() is not None:
            return "Exp"
        elif ctx.And() is not None:
            return "And"
        elif ctx.Less() is not None:
            return "Less"
        elif ctx.Equal() is not None:
            return "Equal"
        elif ctx.Or() is not None:
            return "Or"
        elif ctx.Range() is not None:
            return "Range"

    def visitAtype(self, ctx:XMLExpParser.AtypeContext):
        if ctx.Int() is not None:
            return ctx.getText()
        if ctx.Bool() is not None:
            return ctx.getText()

    def visitNumexp(self, ctx:XMLExpParser.NumexpContext):
        return ctx.getText()
    
