from dataclasses import dataclass
from typing import Any
from rust.ast.ASTNode import CloneableASTNode

@dataclass
class MarkedASTNode(CloneableASTNode):
    node: CloneableASTNode

    def __post_init__(self):
        super().__init__()

    def __getattr__(self, name):
        return getattr(self.node, name)

    # def accept(self, visitor):
    #     return self.node.accept(visitor)
    def accept(self, visitor):
        handler = getattr(visitor, "visitMarkedASTNode", None)
        if callable(handler):
            return handler(self)
        return self.node.accept(visitor)

