from rust.ast.RustASTNodes import DeclarationASTNode
from rust.ast.RustASTVisitor import RustASTVisitor


class StructField(DeclarationASTNode):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def accept(self, visitor: RustASTVisitor):
        return visitor.visitStructField(self)
