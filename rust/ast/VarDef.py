from rust.commons.DeclarationInfo import DeclarationInfo
from rust.ast.ASTNode import ASTNode

class VarDef(ASTNode):
    def __init__(self, name, isMutable=False, by_ref=False, var_type=None):
        # self.declarationInfo = DeclarationInfo(name=name, type=var_type)
        self.name = name
        self.vardef_type = var_type
        self.isMutable = isMutable
        self.by_ref = by_ref

    def accept(self, visitor):
        return visitor.visitVarDef(self)
