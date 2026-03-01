from typing import List
from rust.ast.ASTNode import CloneableASTNode
from rust.ast.RustASTVisitor import RustASTVisitor
from rust.ast.Statement import Statement


class Block(CloneableASTNode):

    def __init__(self, stmts: List[Statement], is_unsafe: bool):
        super().__init__()

        self.stmts = stmts
        self.is_unsafe = is_unsafe

    def accept(self, visitor: RustASTVisitor):
        return visitor.visitBlock(self)

    def statements(self):
        return self.stmts

    def is_unsafe(self):
        return self.is_unsafe
