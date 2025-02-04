from RustCode.AST_Scripts.ProgramVisitor import ProgramVisitor


class TypeChecker(ProgramVisitor):


    def __init__(self, st: dict):
        # need st --> state we are deling with
        self.st = st
        self.var = ""

    def visitFun(self, ctx: XMLProgrammer.QXFun):
        x = ctx.ID()
        i = 0
        tmp = []
        while ctx.args(i) is not None:
            v = ctx.args(i).ID()
            tmp.append([v])
            i = i + 1
        self.var = x
        self.st.update({x:tmp})
        ctx.stmt().accept(self)

    def addElements(self, x:str, y:str):
        tmp = self.st.get(self.var)
        i = 0
        while tmp[i] is not None:
            if x in tmp[i]:
                tmp[i].append(y)
                return
            else:
                i = i + 1

    def moveElements(self, x:str, y: [str]):
        tmp = self.st.get(self.var)
        i = 0
        while tmp[i] is not None:
            if x in tmp[i]:
                tmp[i] = y
            else:
                i = i + 1

    # Visit a parse tree produced by XMLExpParser#blockexp.
    def visitBlock(self, ctx: XMLProgrammer.QXBlock):
        vs = self.st.get(self.var).deepcopy()
        ctx.program().accept(self)
        self.st.update({self.var:vs})

    def visitLet(self, ctx: XMLProgrammer.QXLet):
        x = ctx.ID()
        if isinstance(ctx.vexp(), QXIDExp):
            y = ctx.vexp().ID()
            self.moveElements(y,[x])
        if isinstance(ctx.vexp(), QXRef):
            y = ctx.vexp().accept(self)
            self.addElements(y, x)


    def visitRef(self, ctx: XMLProgrammer.QXRef):
        return ctx.next().ID()