from rust.nodes.RustASTNodes import DeclarationASTNode
# from rust.ast.RustASTVisitor import RustASTVisitor


class StructField(DeclarationASTNode):

    def __init__(self, name, dtype, visibility):
        super().__init__()
        # self._args = args # This should be the individual field names inside the struct
        # self._kwargs = kwargs
        self.name = name
        self.dtype = dtype
        self.visibility = visibility

    def accept(self, visitor):
        return visitor.visitStructField(self)

    # def args(self):
    #     return self._args
    #
    # def kwargs(self):
    #     return self._kwargs
