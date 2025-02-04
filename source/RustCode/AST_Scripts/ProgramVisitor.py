#from RustCode.AST_Scripts import XMLProgrammer
from XMLProgrammer import *

from AbstractProgramVisitor import AbstractProgramVisitor


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
            case QXFun():
                return self.visitFun(ctx)
            case QXLoop():
                return self.visitLoop(ctx)
            case QXFor():
                return self.visitFor(ctx)
            case QXBool():
                return self.visitBool(ctx)
            case QXString():
                return self.visitString(ctx)
            case QXRef():
                return self.visitRef(ctx)
            case Range_expr():
                return self.visitRange_expr(ctx)
            case _:
                raise NotImplementedError(f"No visit method defined for {type(ctx)}")


    # Visit a parse tree produced by XMLExpParser#program.
    def visitProgram(self, ctx: QXProgram):
        result = []
#        print('\nVisiting program', ctx.exps)
        for i in range(len(ctx.exps)):
            result.append(self.visit(ctx.stmt(i)))
        # while ctx.stmt(i) is not None:
        #     ctx.stmt(i).accept(self) # ===> self.visit(ctx.stmt(i))
        #     i = i + 1
        #print('result', result)
        return result

    def visitFun(self, ctx: QXFun):
#        print(f"Visiting function: {ctx._id}, Args: {ctx._args}")
        for arg in ctx._args:
            arg.accept(self)
        self.visit(ctx._stmt)
    #    ctx.stmt().accept(self)

    # Visit a parse tree produced by XMLExpParser#exp.

    # Visit a parse tree produced by XMLExpParser#blockexp.
    def visitBlock(self, ctx: QXBlock):
#        print(f"\nVisiting block: {ctx._program}")
        return self.visit(ctx._program)
 #       return ctx._program.accept(self)

    def visitLet(self, ctx: QXLet):
        return ctx.exp().accept(self)

    def visitPrint(self, ctx: QXPrint):
#        print(f"\nVisiting Print: {ctx._s.str()}")
        if ctx.exp() is not None:
            return ctx.exp().accept(self)
        else: return ctx._s.str()

    def visitBreak(self, ctx: QXBreak):
        if ctx.vexp() is not None:
            return ctx.vexp().accept(self)

    def visitIfStmt(self, ctx: QXIf):
        ctx.vexp().accept(self)
        ctx.left().accept(self)
        ctx.right().accept(self)

    def visitReturn(self, ctx: QXReturn):
        if ctx.vexp() is not None:
            return self.visit(ctx.vexp())

    def visitLoop(self, ctx: QXLoop):
        ctx.block().accept(self)

    def visitFor(self, ctx: QXFor):
#        print('\nVisiting For', self.visitRange_expr(ctx.range()), ctx.block())
        i = ctx.ID()
        r = self.visit(ctx.range())
        b = self.visit(ctx.block())
#        return i, r, b
    
    def visitRange_expr(self, ctx: Range_expr):
        print(f"\nVisiting Range: {ctx.s}, {ctx.e}")
        return ctx

    def visitBin(self, ctx: QXBin):
        self.visit(ctx.vexp())
        ctx.left().accept(self)
        ctx.right().accept(self)


    def visitRef(self, ctx: QXRef):
        ctx.next().accept(self)

    def visitIDExp(self, ctx: QXIDExp):
        return ctx.id

    def visitNum(self, ctx: QXNum):
        return ctx.getText()

    def visitBoolType(self, ctx: Bool):
        return ctx.bool()   
    
    def visitInt(self, ctx: Int):
        return ctx.getText()
    
    def visitBool(self, ctx: QXBool):
        return ctx.bool()
    
    def visitString(self, ctx: QXString):
        return ctx.str()
