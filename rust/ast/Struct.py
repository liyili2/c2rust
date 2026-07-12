from rust.ast.RustASTNodes import DeclarationASTNode
# from rust.ast.RustASTVisitor import RustASTVisitor


class StructField(DeclarationASTNode):

    def __init__(self, args, kwargs):
        super().__init__()
        self._args = args
        self._kwargs = kwargs

    def accept(self, visitor):
        return visitor.visitStructField(self)

    def args(self):
        return self._args

    def kwargs(self):
        return self._kwargs
