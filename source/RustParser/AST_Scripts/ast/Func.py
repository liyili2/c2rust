from RustParser.AST_Scripts.ast.ASTNode import ASTNode
from RustParser.AST_Scripts.ast.common import DeclarationInfo
from RustParser.AST_Scripts.ast.common import DeclarationInfo

class Param(ASTNode):
    def __init__(self, name, typ, isMutable):
        super().__init__()
        self.declarationInfo = DeclarationInfo(name=name, type=typ)
        self.isMutable = isMutable
        self.parent = None

    def __repr__(self):
        return f"ParamNode(name={self.declarationInfo.name}, type={self.declarationInfo.type}, mutable={self.isMutable})"

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