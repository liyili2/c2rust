from types import NoneType

import AbstractProgramVisitor


class QXTop:

    def accept(self, visitor):
        pass


class QXStmt(QXTop):

    def accept(self, visitor: AbstractProgramVisitor):
        pass

class QXExp(QXTop):

    def accept(self, visitor: AbstractProgramVisitor):
        pass

class QXType(QXTop):

    def accept(self, visitor: AbstractProgramVisitor):
        pass

class QXProgram(QXTop):
    def __init__(self, exps: list[QXStmt]):
        self.exps = exps

    def accept(self, visitor: AbstractProgramVisitor):
        visitor.visitProgram(self)

    def stmt(self, i: int = None):
        return self.exps[i] if len(self.exps) > i else None

class QXBlock(QXStmt):
    def __init__(self, program: QXProgram):
        self._program = program

    def accept(self, visitor: AbstractProgramVisitor):
        visitor.visitBlock(self)

    def program(self):
        return self._program


class QXVExp(QXExp):

    def accept(self, visitor: AbstractProgramVisitor):
        visitor.visit(self)

class QXIDExp(QXVExp):
    def __init__(self, id: str, type: QXType = None):
        self.id = id
        self.type = type

    def accept(self, visitor: AbstractProgramVisitor):
        visitor.visitIDExp(self)

    def ID(self):
        return self.id if self.id is str else self.id.getText()

    def type(self):
        return self.type

class Range_expr(QXExp):
    def __init__(self, v1: QXVExp, v2: QXVExp):
        self.s = v1
        self.e = v2
    def accept(self, visitor: AbstractProgramVisitor):
        visitor.visitRange_expr(self)

    def start(self):
        return self.s
    def end(self):
        return self.e

class QXFun(QXStmt):
    def __init__(self, id: str, args: list[QXIDExp],  stmt: QXBlock):
        self._id = id
        self._args = args
        self._stmt = stmt

    def accept(self, visitor: AbstractProgramVisitor):
        visitor.visitFun(self)

    def ID(self):
        return self._id

    def args(self, i : int = None):
        return self._args[i]

    def stmt(self):
        return self._stmt



class QXLet(QXStmt):
    def __init__(self, id: str, p: QXVExp):
        self._id = id
        self._vexp = p

    def accept(self, visitor: AbstractProgramVisitor):
        visitor.visitLet(self)

    def ID(self):
        return self._id if isinstance(self._id, str) else self._id.getText()

    def vexp(self):
        return self._vexp


class QXPrint(QXStmt):
    def __init__(self, s: str, vs: QXExp=None):
        self._s = s
        self._vs = vs

    def accept(self, visitor: AbstractProgramVisitor):
        visitor.visitPrint(self)

    def str(self) -> str:
        return self._s if isinstance(self._s, str) else self._s.getText()

    def exp(self):
        return self._vs


class QXIf(QXStmt):
    def __init__(self, v: QXVExp, left: QXBlock, right: QXBlock):
        self._v = v
        self._left = left
        self._right = right

    def accept(self, visitor: AbstractProgramVisitor):
        visitor.visitIfStmt(self)

    def vexp(self):
        return self._v

    def left(self):
        return self._left

    def right(self):
        return self._right


class QXBreak(QXStmt):
    def __init__(self, v: QXVExp=None):
        self.v = v

    def accept(self, visitor: AbstractProgramVisitor):
        visitor.visitBreak(self)

    def vexp(self):
        return self.v


class QXReturn(QXStmt):
    def __init__(self, v: QXVExp=None):
        self.v = v

    def accept(self, visitor: AbstractProgramVisitor):
        visitor.visitReturn(self)

    def vexp(self):
        return self.v


class QXLoop(QXStmt):
    def __init__(self, s: QXBlock):
        self._s = s

    def accept(self, visitor: AbstractProgramVisitor):
        visitor.visitLoop(self)

    def block(self):
        return self._s


class QXFor(QXStmt):
    def __init__(self, id: str, r: Range_expr, b:QXBlock):
        self.id = id
        self.r = r
        self.b = b

    def accept(self, visitor: AbstractProgramVisitor):
        visitor.visitFor(self)

    def ID(self):
        return self.id

    def range(self):
        return self.r

    def block(self):
        return self.b


class QXRef(QXVExp):
    def __init__(self, v: QXVExp):
        self._v = v

    def accept(self, visitor: AbstractProgramVisitor):
        visitor.visitRef(self) #Not exist

    def next(self):
        return self._v


class QXBin(QXVExp):
    def __init__(self, op: str, v1: QXVExp, v2: QXVExp):
        self._op = op
        self._v1 = v1
        self._v2 = v2

    def accept(self, visitor: AbstractProgramVisitor):
        visitor.visitBin(self) #Not exist

    def OP(self):
        return self._op

    def left(self):
        return self._v1

    def right(self):
        return self._v2


class QXString(QXVExp):
    def __init__(self, v: str):
        self.v = v

    def accept(self, visitor: AbstractProgramVisitor):
        visitor.visitString(self)

    def str(self):
        return self.v


class QXBool(QXVExp):
    def __init__(self, v: bool):
        self.v = v

    def accept(self, visitor: AbstractProgramVisitor):
        visitor.visitBool(self)

    def bool(self):
        return self.v

class QXNum(QXVExp):
    def __init__(self, v: int):
        self.v = v

    def accept(self, visitor: AbstractProgramVisitor):
        visitor.visitNum(self)

    def num(self):
        return self.v
    

class Bool(QXType):
    type = "Bool"

    def type(self):
        return "Bool"

    def accept(self, visitor: AbstractProgramVisitor):
        visitor.visitBoolType(self)


class Int(QXType):
    type = "Nat"

    def type(self):
        return "Nat"

    def accept(self, visitor: AbstractProgramVisitor):
        visitor.visitInt(self)


class Fun(QXType):

    def __init__(self, args: list[str], pre: dict, out: dict):
        self.args = args
        self.pre = pre
        self.out = out
        # self.r2 = r2

    def type(self):
        return ("Fun", (self.args, self.pre, self.out))

    def args(self):
        return self.args

    def pre(self):
        return self.pre

    def out(self):
        return self.out

    def __str__(self):
        return f"Fun(args={self.args}, pre={self.pre}, out={self.out})"

    def accept(self, visitor: AbstractProgramVisitor):
        visitor.visitFun(self)
