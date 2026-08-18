from rust.nodes.ASTNode import ASTNode, CloneableASTNode


class Param(CloneableASTNode):

    def __init__(self, name, typ, is_mutable):
        super().__init__()
        self._name = name
        self._type = typ
        self._is_mutable = is_mutable

    def accept(self, visitor):
        return visitor.visitParam(self)

    def name(self):
        return self._name

    def type(self):
        return self._type

    def is_mutable(self):
        return self._is_mutable


class FunctionParamList(CloneableASTNode):

    def __init__(self, params):
        super().__init__()
        self._params = params

    def accept(self, visitor):
        return visitor.visitFunctionParamList(self)

    def params(self):
        return self._params
