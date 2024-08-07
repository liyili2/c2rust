from collections import ChainMap
from collections import deque
# from types import NoneType

from antlr4 import ParserRuleContext

from XMLExpParser import *
from XMLExpVisitor import *

NoneType = type(None)


class coq_val:
    pass  # TODO


class Coq_nval(coq_val):

    def __init__(self, b: [bool], r: int):
        self.b = b
        self.r = r

    def getBits(self):
        return self.b

    def getPhase(self):
        return self.r


class Coq_qval(coq_val):

    def __init__(self, r1: int, r2: int, n: int):
        self.r1 = r1
        self.r2 = r2
        self.n = n

    def getPhase(self):
        return self.r1

    def getLocal(self):
        return self.r2

    def getNum(self):
        return self.n


"""
Helper Functions
"""


def exchange(v: coq_val, n: int):
    if isinstance(v, Coq_nval):
        v.getBits()[n] = not v.getBits()[n]


def times_rotate(v, q, rmax):
    if isinstance(v, Coq_nval):
        if v.b:
            return Coq_nval(v.getBits(), rotate(v.getPhase(), q, rmax))
        else:
            return Coq_nval(v.getBits(), v.getPhase())
    else:
        return Coq_qval(v.r1, rotate(v.r2, q, rmax))


def addto(r, n, rmax):
    return (r + 2 ** max_helper(rmax, n)) % 2 ** rmax


def max_helper(x, y):
    return max(x - y, 0)


def rotate(r, n, rmax):
    return addto(r, n, rmax)


def addto_n(r, n, rmax):
    return max_helper(r + 2 ** rmax, 2 ** max_helper(rmax, n)) % 2 ** rmax


def r_rotate(r, n, rmax):
    return addto_n(r, n, rmax)


def times_r_rotate(v, q, rmax):
    if isinstance(v, Coq_nval):
        if v.b:
            return Coq_nval(v.getBits(), r_rotate(v.getPhase(), q, rmax))
        else:
            return Coq_nval(v.getBits(), v.getPhase())
    else:
        return Coq_qval(v.r1, r_rotate(v.r2, q, rmax))


def up_h(v, rmax):
    if isinstance(v, Coq_nval):
        b = v.b
        r = v.r
        if b:
            return Coq_qval(
                r,
                rotate(0, 1, rmax)
            )
        else:
            return Coq_qval(r, 0)
    else:
        r = v.r1
        f = v.r2
        return Coq_nval(
            2 ** max_helper(rmax, 1) <= f,
            r
        )


def natminusmod(x, v, a):
    if x - v < 0:
        return x - v + a
    else:
        return x - v


def calInt(v, n):
    val = 0
    for i in range(n):
        val += pow(2, i) * int(v[i])
    return val


def calBin(v, n):
    val = [False] * n
    for i in range(n):
        b = v % 2
        v = v // 2
        val[i] = bool(b)
    return val


class Simulator(XMLExpVisitor):
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

    def sr_rotate(self, x, n):
        val = self.st.get(x)
        if isinstance(val, Coq_qval):
            self.st.update(
                {x: Coq_qval(val.r1, (val.r2 + pow(2, val.getNum() - n - 1)) % pow(2, val.getNum()), val.getNum())})

    def srr_rotate(self, x, n):
        val = self.st.get(x)
        if isinstance(val, Coq_qval):
            self.st.update({x: Coq_qval(val.r1, natminusmod(val.r2, pow(2, val.getNum() - n - 1),
                                                            pow(2, val.getNum())), val.getNum())})

    # I need to write the function of these grammar now, not just print them out

    # this uses if statements to call the various visit functions
    def visitProgram(self, ctx: XMLExpParser.ProgramContext):
        # I will need to modify this so that block can tell when certain things happen?
        result = None
        if ctx.letstmt() is not None:
            result = ctx.letstmt().accept(self)
        elif ctx.exp() is not None:
            result = ctx.exp().accept(self)
        elif ctx.printstmt() is not None:
            result = ctx.printstmt().accept(self)
        elif ctx.blockstmt() is not None:
            result = ctx.blockstmt().accept(self)
        elif ctx.ifstmt() is not None:
            result = ctx.ifstmt().accept(self)
        elif ctx.breakstmt() is not None:
            result = ctx.breakstmt().accept(self)
        elif ctx.returnstmt() is not None:
            result = ctx.returnstmt().accept(self)
        elif ctx.loopstmt() is not None:
            result = ctx.loopstmt().accept(self)
        elif ctx.forstmt() is not None:
            result = ctx.forstmt().accept(self)

        return result

    # This is somewhat complicated to simulate
    def visitBlockstmt(self, ctx: XMLExpParser.BlockstmtContext):
        # This just calls visit program multiple times, it won't return?
        # only calls things? and break statement is where changes happen to loop, not block statement
        # Maybe only return certain things, e.g., result of a break statement.
        # This will need to be determined by the result of program, maybe something like, None is returned except
        # for certain things by program?

        i = 0
        while ctx.program(i) is not None:
            ctx.program(i).accept(self)
            i += 1


        return

    # Let statement should assign something?
    # For now, implement some of the expressions
    def visitLetstmt(self, ctx: XMLExpParser.LetstmtContext):
        x = ctx.idexp().accept(self) # make idexp return identifier
        y = ctx.exp().accept(self) # exp will return the value
        self.st.update({str(x) : y})

        return

    def visitPrintstmt(self, ctx: XMLExpParser.PrintstmtContext):
        # this prints the stringval, then does something with the exp?
        # This would call my printer, I will implement later (will be harder)
        return

    def visitIfstmt(self, ctx: XMLExpParser.IfstmtContext):
        if_result = ctx.vexp().accept(self)
        result = None

        if if_result:
            result = ctx.blockstmt.accept(self)
        else:
            result = ctx.blockstmt.accept(self)


        return result

    def visitBreakstmt(self, ctx: XMLExpParser.BreakstmtContext):
        # This will be more complicated due to the different types of loops
        self.stack_bools.pop()
        self.stack_bools.append(False)

        if ctx.vexp() is not None:
            return ctx.vexp().accept(self)
        return None # maybe this is better to return?

    def visitReturnstmt(self, ctx: XMLExpParser.ReturnstmtContext):
        if ctx.vexp() is None:
            return
        else:
            return ctx.vexp().accept(self)

    def visitLoopstmt(self, ctx: XMLExpParser.LoopstmtContext):
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

    def visitForstmt(self, ctx: XMLExpParser.ForstmtContext):
        # This is the traditional for loop

        return

    def visitExp(self, ctx: XMLExpParser.ExpContext):

        return ctx.vexp().accept(self)

    # def visitIdexp(self, ctx: XMLExpParser.IdexpContext):
    #     return

    def visitStringval(self, ctx: XMLExpParser.StringvalContext):
        return ctx.StrLiteral().accept(self)

    def visitVexp(self, ctx:XMLExpParser.VexpContext):
        # ctx.accept(self) # this likely won't work, so I will need to do a case analysis here as well.
        # Just get it to work for now.

        if ctx.idexp() is not None:
            return ctx.idexp().accept(self)
        elif ctx.numexp() is not None:
            return ctx.numexp().accept(self)
        elif ctx.boolexp() is not None:
            return ctx.boolexp().accept(self)
        elif ctx.binexp() is not None:
            return ctx.binexp().accept(self)


    def visitNumexp(self, ctx:XMLExpParser.NumexpContext):
        number = int(str(ctx.Number()))
        if ctx.Minus() is not None:
            number = -number

        return number

    def visitBinexp(self, ctx:XMLExpParser.BinexpContext):
        operator = str(ctx.OP())
        # This will be very complicated.
        a = ctx.vexp().accept(self)
        b = ctx.vexp().accept(self)
        # range is more complicated due to there being an = operator. I can forget about this case for now.
        # Now, I need to write out the cases for each operator.


        if operator == '+':
            return a + b
        elif operator == '-':
            return a - b
        elif operator == '*':
            return a * b
        elif operator == '/':
            return a / b
        elif operator == '%':
            return a % b
        elif operator == '^':
            return pow(a, b)
        elif operator == '&&':
            return a and b
        elif operator == '||':
            return a or b
        elif operator == '<':
            return a < b
        elif operator == '==':
            return a == b
        elif operator == '..':
            result = range(a, b)
            return result


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

    def visitIdexp(self, ctx: XMLExpParser.IdexpContext):
        return ctx.Identifier().accept(self)

    # Visit a parse tree produced by XMLExpParser#vexp.
    # def visitVexp(self, ctx: XMLExpParser.VexpContext):
    #     return ctx.numexp().accept(self)

    # the only thing that matters will be 48 and 47
    def visitTerminal(self, node):
        if node.getSymbol().type == XMLExpParser.Identifier:
            return node.getText()
        if node.getSymbol().type == XMLExpParser.Number:
            return int(node.getText())
        return "None"
