import copy
import time
from abc import ABC, abstractmethod
from antlr4.tree.Tree import TerminalNodeImpl


class ASTNode(ABC):

    @abstractmethod
    def accept(self, visitor):
        pass


class CloneableASTNode(ASTNode):

    def __init__(self):
        self.uid = str(id(self)) + str(time.time())

    def set_id(self, uid: str):
        self.uid = uid

    def get_id(self) -> str:
        return self.uid

    def instance(self, uid: str):
        self.set_id(uid)
        return self

    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result

        for k, v in self.__dict__.items():
            if isinstance(v, TerminalNodeImpl):
                setattr(result, k, v)
            else:
                setattr(result, k, copy.deepcopy(v, memo))

        return result

    @abstractmethod
    def accept(self, visitor):
        pass
