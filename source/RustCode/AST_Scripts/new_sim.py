from collections import ChainMap
from collections import deque
# from types import NoneType

from ProgramVisitor import *
from XMLProgrammer import *

NoneType = type(None)

class Simulator(ProgramVisitor):
    # x, y, z, env : ChainMap{ x: n, y : m, z : v} , n m v are nat numbers 100, 100, 100, eg {x : 128}
    # st state map, {x : v1, y : v2 , z : v3}, eg {x : v1}: v1,
    # st {x : v1} --> Coq_nval case: v1 is a ChainMap of Coq_nval
    # v1 --> 128 length array v1: {0 : Coq_nval, 1 : Coq_nval, 2 : Coq_nval, ...., 127 : Coq_nval}, 2^128
    # x --> v1 --> cal(v1) --> integer
    # Coq_nval(b,r) b == |0> | |1>, r == e^(2 pi i * 1 / n), r = 0 Coq_nval(b, 0)
    # x -> v1 ----> run simulator -----> v2 ---> calInt(v2,128) == (x + 2^10) % 2^128
    def __init__(self, st: dict):
        # need st --> state we are dealing with
        self.st = st
        self.stack_bools = deque()


    def get_state(self):
        return self.st

    # I need to write the function of these grammar now, not just print them out

    # Let statement should assign something?
    # For now, implement some of the expressions
    def visitLet(self, ctx: XMLProgrammer.QXLet):
        x = ctx.idexp().ID() # make idexp return identifier
        y = ctx.exp().accept(self) # exp will return the value
        self.st.update({str(x) : y})
        return

    def visitPrint(self, ctx: XMLProgrammer.QXPrint):
        # this prints the stringval, then does something with the exp?
        # This would call my printer, I will implement later (will be harder)
        print(ctx.str())
        return

    def visitIfStmt(self, ctx: XMLProgrammer.QXIf):
        if_result = ctx.vexp().accept(self)
        result = None
        if if_result:
            result = ctx.blockstmt.accept(self)
        else:
            result = ctx.blockstmt.accept(self)


        return result

    def visitBreak(self, ctx: XMLProgrammer.QXBreak):
        # This will be more complicated due to the different types of loops
        self.stack_bools.pop()
        self.stack_bools.append(False)

        if ctx.vexp() is not None:
            return ctx.vexp().accept(self)
        return None # maybe this is better to return?

    def visitReturn(self, ctx: XMLProgrammer.QXReturn):
        if ctx.vexp() is None:
            return
        else:
            return ctx.vexp().accept(self)

    def visitLoop(self, ctx: XMLProgrammer.QXLoop):
        # This is the loop keyword. For this type of loop, break statement can return a value
        # A loop statement contains a block statement, and if a break appears in the immediate block statement,
        # this loop will end?
        # The result of a loop comes only from the break statement.
        self.stack_bools.append(True)

        # now, the loop goes into the block
        block_result = ctx.blockstmt().accept(self)

        top = self.stack_bools.pop()
        if not top:
            return block_result # this means break statement was called and it is returned back?
        else:
            # call this function again?
            self.visitLoopstmt(ctx) # is this correct?

        return None

    def visitFor(self, ctx: XMLProgrammer.QXFor):
        # This is the traditional for loop
        x = ctx.ID()
        v = self.visit(ctx.vexp())
        tmp = self.st.get(x)
        i = 0
        while i < v:
            self.st.update({x: v})
            ctx.block().accept(self)
            i = i + 1

        self.st.update({x: tmp})

    # def visitIdexp(self, ctx: XMLExpParser.IdexpContext):
    #     return

    def visitString(self, ctx: XMLProgrammer.QXString):
        return ctx.str()


    def visitNum(self, ctx: XMLProgrammer.QXNum):
        return ctx.num()

    def visitBool(self, ctx: XMLProgrammer.QXBool):
        return ctx.bool()

    def visitBinexp(self, ctx:XMLExpParser.BinexpContext):
        operator = str(ctx.OP())
        # This will be very complicated.
        a = ctx.vexp().accept(self)
        b = ctx.vexp().accept(self)
        # range is more complicated due to there being an = operator. I can forget about this case for now.
        # Now, I need to write out the cases for each operator.

        if operator == 'Plus':
            return a + b
        elif operator == 'Minus':
            return a - b
        elif operator == 'Times':
            return a * b
        elif operator == 'Div':
            return a / b
        elif operator == 'Mod':
            return a % b
        elif operator == 'Exp':
            return pow(a, b)
        elif operator == 'And':
            return a and b
        elif operator == 'Or':
            return a or b
        elif operator == '<':
            return a < b
        elif operator == '==':
            return a == b
        elif operator == '..':
            return range(a, b)
            #return result

        return None

    def visitBoolexp(self, ctx: XMLExpParser.BoolexpContext):
        if ctx.TrueLiteral() is not None:
            return True
        else:
            return False

    def visit(self, ctx: ParserRuleContext):
        if ctx.getChildCount() > 0:
            return self.visitChildren(ctx)
        else:
            return self.visitTerminal(ctx)

    def visitIDExp(self, ctx: XMLProgrammer.QXIDExp):
        return ctx.ID()

    # Visit a parse tree produced by XMLExpParser#vexp.
    # def visitVexp(self, ctx: XMLExpParser.VexpContext):
    #     return ctx.numexp().accept(self)
