from typing import List
from rust.nodes.ASTNode import CloneableASTNode, ASTNode


class Program(CloneableASTNode):

    def __init__(self, exps: List[ASTNode]):
        super().__init__()
        self._items: List[ASTNode] = exps

    def accept(self, visitor):
        return visitor.visitProgram(self)

    def exp(self, i: int) -> ASTNode | None:
        if i < len(self._items):
            return self._items[i]
        else:
            return None

    def length(self) -> int:
        return len(self._items)
