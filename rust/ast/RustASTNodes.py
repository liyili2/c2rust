from abc import abstractmethod
from rust.ast.ASTNode import CloneableASTNode


class DeclarationASTNode(CloneableASTNode):

    def __init__(self, name: str = None, dtype: str = None, visibility: str = None):
        super().__init__()

        self._name = name
        self._type = dtype
        self._visibility = visibility

    @abstractmethod
    def accept(self, visitor):
        pass

    def name(self):
        return self._name

    def type(self):
        return self._type

    def visibility(self):
        return self._visibility
