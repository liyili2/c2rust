from abc import abstractmethod
from rust.ast.ASTNode import CloneableASTNode


class DeclarationASTNode(CloneableASTNode):

    def __init__(self, name: str, dtype: str = None, visibility: str = None):
        super().__init__()

        self.name = name
        self.type = dtype
        self.visibility = visibility

    @abstractmethod
    def accept(self, visitor):
        pass
