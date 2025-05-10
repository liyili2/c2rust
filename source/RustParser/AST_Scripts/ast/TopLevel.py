from RustParser.AST_Scripts.ast import Type


class FunctionDef:
    def __init__(self, identifier, params, return_type, body):
        self.Identifier = identifier
        self.params = params  # list of (name, type)
        self.return_type = return_type
        self.body = body      # list of statements

    def accept(self, visitor):
        method_Identifier = f'visit_{self.__class__.__name__}'
        return getattr(visitor, method_Identifier, visitor.generic_visit)(self)

class StructDef:
    def __init__(self, name, fields):
        self.name = name
        self.fields = fields  # list of (name, type)

    def accept(self, visitor):
        method_name = f'visit_{self.__class__.__name__}'
        return getattr(visitor, method_name, visitor.generic_visit)(self)

class Attribute:
    def __init__(self, name, args=None):
        self.name = name
        self.args = args or []

    def accept(self, visitor):
        method_name = f'visit_{self.__class__.__name__}'
        return getattr(visitor, method_name, visitor.generic_visit)(self)

class ExternBlock:
    def __init__(self, abi: str, items: list):
        self.abi = abi
        self.items = items

    def __repr__(self):
        return f"<ExternBlock abi={self.abi}, items={self.items}>"

class ExternItem:
    pass    

class ExternTypeDecl(ExternItem):
    def __init__(self, name: str, visibility: str = None):
        self.name = name
        self.visibility = visibility  # e.g., "pub" or None

    def __repr__(self):
        return f"<ExternTypeDecl {self.visibility or ''} type {self.name}>"

class ExternStaticVarDecl(ExternItem):
    def __init__(self, name: str, var_type: Type, mutable: bool, visibility: str = None):
        self.name = name
        self.var_type = var_type
        self.mutable = mutable
        self.visibility = visibility

    def __repr__(self):
        mut = "mut " if self.mutable else ""
        return f"<ExternStaticVarDecl {self.visibility or ''} static {mut}{self.name}: {self.var_type}>"

class ExternFnDecl(ExternItem):
    def __init__(self, name: str, params: list, return_type: Type = None, visibility: str = None):
        self.name = name
        self.params = params
        self.return_type = return_type
        self.visibility = visibility

    def __repr__(self):
        return f"<ExternFnDecl {self.visibility or ''} fn {self.name}({self.params}) -> {self.return_type}>"
