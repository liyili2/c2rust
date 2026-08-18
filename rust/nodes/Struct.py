from rust.nodes.ASTNode import CloneableASTNode


class StructField(CloneableASTNode):

    def __init__(self, name, dtype, visibility):
        super().__init__()
        self._name = name
        self._dtype = dtype
        self._visibility = visibility

    def accept(self, visitor):
        return visitor.visitStructField(self)

    def name(self):
        return self._name

    def type(self):
        return self._dtype

    def visibility(self):
        return self._visibility
