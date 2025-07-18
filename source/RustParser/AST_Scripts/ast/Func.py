from RustParser.AST_Scripts.ast.ASTNode import ASTNode

class Param(ASTNode):
    def __init__(self, name, typ, mutable):
        super().__init__()
        self.name = name                  # str
        self.typ = typ                    # AST node (e.g., TypeNode)
        self.mutable = mutable              # bool
        self.parent = None

    def __repr__(self):
        return f"ParamNode(name={self.name}, type={self.typ}, mutable={self.mutable})"

    def accept(self, visitor):
        return visitor.visit_ParamNode(self)
    
    def set_parent(self, parent):
        self.parent = parent

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