from abc import ABC, abstractmethod

from antlr4 import ParseTreeVisitor



class AbstractProgramVisitor(ABC):


    @abstractmethod
    def visit(self, ctx):
        pass

    @abstractmethod
    def visitProgram(self, ctx):
        pass

    @abstractmethod
    def visitBlock(self, ctx):
        pass

    @abstractmethod
    def visitLet(self, ctx):
        pass

    @abstractmethod
    def visitPrint(self, ctx):
        pass

    @abstractmethod
    def visitIfStmt(self, ctx):
        pass

    @abstractmethod
    def visitBreak(self, ctx):
        pass

    @abstractmethod
    def visitReturn(self, ctx):
        pass

    @abstractmethod
    def visitLoop(self, ctx):
        pass

    @abstractmethod
    def visitFor(self, ctx):
        pass

    @abstractmethod
    def visitBin(self, ctx):
        pass

    @abstractmethod
    def visitIDExp(self, ctx):
        pass

    @abstractmethod
    def visitNum(self, ctx):
        pass

    @abstractmethod
    def visitBool(self, ctx):
        pass

    @abstractmethod
    def visitBoolType(self, ctx):
        pass

    @abstractmethod
    def visitInt(self, ctx):
        pass

    @abstractmethod
    def visitFun(self, ctx):
        pass

    @abstractmethod
    def visitString(self, ctx):
        pass
