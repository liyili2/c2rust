from RustCode.AST_Scripts import XMLProgrammer
from RustCode.AST_Scripts.XMLProgrammer import *

from RustCode.AST_Scripts.AbstractProgramVisitor import AbstractProgramVisitor


class ProgramVisitor(AbstractProgramVisitor):

    def visit(self, ctx):
        match ctx:
            case QXBlock():
                return self.visitBlock(ctx)
            case QXProgram():
                return self.visitProgram(ctx)
            case QXLet():
                return self.visitLet(ctx)
            case QXPrint():
                return self.visitPrint(ctx)
            case QXIf():
                return self.visitIfStmt(ctx)
            case QXBreak():
                return self.visitBreak(ctx)
            case QXReturn():
                return self.visitReturn(ctx)
            case QXBin():
                return self.visitBin(ctx)
            case QXIDExp():
                return self.visitIDExp(ctx)
            case QXNum():
                return self.visitNum(ctx)
            case Int():
                return self.visitInt(ctx)
            case Bool():
                return self.visitBoolType(ctx)
            case Fun():
                return self.visitFun(ctx)
            case QXLoop():
                return self.visitLoop(ctx)
            case QXFor():
                return self.visitFor(ctx)
            case QXBool():
                return self.visitBool(ctx)
            case QXString():
                return self.visitString(ctx)
            case _:
                raise NotImplementedError(f"No visit method defined for {type(ctx)}")


    # Visit a parse tree produced by XMLExpParser#program.
    def visitProgram(self, ctx: XMLProgrammer.QXProgram):
        i = 0
        while ctx.stmt(i) is not None:
            ctx.stmt(i).accept(self)
            i = i + 1

    def visitFun(self, ctx: XMLProgrammer.QXFun):
        i = 0
        while ctx.args(i) is not None:
            ctx.args(i).accept(self)
            i = i + 1
        ctx.stmt().accept(self)

    # Visit a parse tree produced by XMLExpParser#exp.

    # Visit a parse tree produced by XMLExpParser#blockexp.
    def visitBlock(self, ctx: XMLProgrammer.QXBlock):
        return ctx.program().accept(self)

    def visitLet(self, ctx: XMLProgrammer.QXLet):
        return ctx.exp().accept(self)

    def visitPrint(self, ctx: XMLProgrammer.QXPrint):
        return ctx.exp().accept(self)

    def visitBreak(self, ctx: XMLProgrammer.QXBreak):
        if ctx.vexp() is not None:
            return ctx.vexp().accept(self)

    def visitIfStmt(self, ctx: XMLProgrammer.QXIf):
        ctx.vexp().accept(self)
        ctx.left().accept(self)
        ctx.right().accept(self)

    def visitReturn(self, ctx: XMLProgrammer.QXReturn):
        if ctx.vexp() is not None:
            return self.visit(ctx.vexp())

    def visitLoop(self, ctx: XMLProgrammer.QXLoop):
        ctx.block().accept(self)

    def visitFor(self, ctx: XMLProgrammer.QXFor):
        self.visit(ctx.vexp())
        return ctx.block().accept(self)

    def visitBin(self, ctx: XMLProgrammer.QXBin):
        self.visit(ctx.vexp())
        ctx.left().accept(self)
        ctx.right().accept(self)


    def visitRef(self, ctx: XMLProgrammer.QXRef):
        ctx.next().accept(self)

    def visitIDExp(self, ctx: XMLProgrammer.QXIDExp):
        self.visit(ctx.type())

    def visitNum(self, ctx: XMLProgrammer.QXNum):
        pass

    def visitBoolType(self, ctx: XMLProgrammer.Bool):
        pass
