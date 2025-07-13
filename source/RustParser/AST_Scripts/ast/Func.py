from RustParser.AST_Scripts.ast.ASTNode import ASTNode

class Param(ASTNode):
    def __init__(self, name, typ, is_mut):
        super().__init__()
        self.name = name                  # str
        self.typ = typ                    # AST node (e.g., TypeNode)
        self.is_mut = is_mut              # bool

    def __repr__(self):
        return f"ParamNode(name={self.name}, type={self.typ}, is_mut={self.is_mut})"

    def accept(self, visitor):
        return visitor.visit_ParamNode(self)

class FunctionParamList(ASTNode):
    def __init__(self, params):
        super().__init__()
        self.params = params
        self.param_len = len(self.params)

    def __iter__(self):
        return iter(self.params)
    def __repr__(self):
        return f"FunctionParamList(params={self.params})"
    def accept(self, visitor):
        return visitor.visit_FunctionParamList(self)