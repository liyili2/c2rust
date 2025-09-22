from RustParser.AST_Scripts.ast.common import DeclarationInfo

class VarDef:
    def __init__(self, name, mutable=False, by_ref=False, var_type=None):
        self.declarationInfo = DeclarationInfo(name=name, type=var_type)
        self.mutable = mutable
        self.by_ref = by_ref

    def accept(self, visitor):
        return visitor.visit_VarDef(self)
