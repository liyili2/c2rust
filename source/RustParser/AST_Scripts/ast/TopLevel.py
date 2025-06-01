from RustParser.AST_Scripts.ast import Type
from RustParser.AST_Scripts.ast.ASTNode import ASTNode

class TopLevel(ASTNode):
    def __init__(self):
        pass

    def accept(self, visitor):
        method_name = f'visit_{self.__class__.__name__}'
        return getattr(visitor, method_name, visitor.generic_visit)(self)

class FunctionDef(TopLevel):
    def __init__(self, identifier, params, return_type, body):
        super().__init__()
        self.identifier = identifier
        self.params = params
        self.return_type = return_type
        self.body = body

    def accept(self, visitor):
        method_Identifier = f'visit_{self.__class__.__name__}'
        return getattr(visitor, method_Identifier, visitor.generic_visit)(self)

class StructDef(TopLevel):
    def __init__(self, name, fields):
        super().__init__()
        self.name = name
        self.fields = fields

    def accept(self, visitor):
        method_name = f'visit_{self.__class__.__name__}'
        return getattr(visitor, method_name, visitor.generic_visit)(self)

class Attribute(TopLevel):
    def __init__(self, name, args=None):
        super().__init__()
        self.name = name
        self.args = args or []

    def accept(self, visitor):
        method_name = f'visit_{self.__class__.__name__}'
        return getattr(visitor, method_name, visitor.generic_visit)(self)

class ExternBlock(TopLevel):
    def __init__(self, abi: str, items: list):
        super().__init__()
        self.abi = abi
        self.items = items

    def __repr__(self):
        return f"<ExternBlock abi={self.abi}, items={self.items}>"

class ExternItem(ASTNode):
    pass    

class ExternTypeDecl(ExternItem):
    def __init__(self, name: str, visibility: str = None):
        super().__init__()
        self.name = name
        self.visibility = visibility  # e.g., "pub" or None

    def __repr__(self):
        return f"<ExternTypeDecl {self.visibility or ''} type {self.name}>"
    
    def accept(self, visitor):
        pass

class ExternStaticVarDecl(ExternItem):
    def __init__(self, name: str, var_type: Type, mutable: bool, initial_value, visibility: str = None):
        self.name = name
        self.var_type = var_type
        self.mutable = mutable
        self.visibility = visibility
        self.value = initial_value

    def __repr__(self):
        mut = "mut " if self.mutable else ""
        return f"<ExternStaticVarDecl {self.visibility or ''} static {mut}{self.name}: {self.var_type}>"

    def accept(self, visitor):
        pass

class ExternFnDecl(ExternItem):
    def __init__(self, name: str, params: list, return_type: Type = None, visibility: str = None):
        self.name = name
        self.params = params
        self.return_type = return_type
        self.visibility = visibility

    def __repr__(self):
        return f"<ExternFnDecl {self.visibility or ''} fn {self.name}({self.params}) -> {self.return_type}>"

class ExternFunctionDecl(TopLevel):
    def __init__(self, name, params, return_type=None, variadic=False, visibility=None):
        self.name = name  # function name (string)
        self.params = params  # list of parameter types (AST nodes or strings)
        self.return_type = return_type  # return type (AST node or string), or None for `-> ()`
        self.variadic = variadic  # True if the function is variadic (`...` present)
        self.visibility = visibility  # e.g., 'pub', or None

    def __repr__(self):
        return (
            f"ExternFunctionDecl(name={self.name!r}, params={self.params}, "
            f"return_type={self.return_type}, variadic={self.variadic}, "
            f"visibility={self.visibility})"
        )

class TypeAliasDecl(TopLevel):
    def __init__(self, name, type, visibility=None):
        self.name = name
        self.type = type
        self.visibility = visibility

class TopLevelVarDef(TopLevel):
    def __init__(self, name, fields, type, visibility=None):
        self.name = name
        self.fields = fields
        self.visibility = visibility
        self.type_ = type

class InterfaceDef(TopLevel):
    def __init__(self, name: str, functions: list):
        super().__init__()
        self.name = name
        self.functions = functions or []

    def __repr__(self):
        return f"InterfaceDef(name={self.name}, functions={self.functions})"
