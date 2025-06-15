class VarDef:
    def __init__(self, name, mutable=False, by_ref=False, var_type=None):
        self.name = name
        self.mutable = mutable
        self.by_ref = by_ref
        self.type = var_type
    
    def accept(self, visitor):
        return visitor.visit_VarDef(self)
