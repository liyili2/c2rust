from rust.ast.ASTNode import ASTNode
from rust.ast.RustASTVisitor import RustASTVisitor
from rust.ast.common import DeclarationInfo


class Param(ASTNode):

    def __init__(self, name, typ, isMutable):
        super().__init__()
        self.declarationInfo = DeclarationInfo(name=name, type=typ)
        self.isMutable = isMutable
        self.parent = None

    def accept(self, visitor: RustASTVisitor):
        return visitor.visitParam(self)


class FunctionParamList(ASTNode):

    def __init__(self, params):
        super().__init__()
        self.params = params

    def accept(self, visitor: RustASTVisitor):
        return visitor.visitFunctionParamList(self)
