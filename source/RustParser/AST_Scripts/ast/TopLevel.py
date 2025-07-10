from typing import List, Optional
from RustParser.AST_Scripts.ast.Program import Program
from RustParser.AST_Scripts.ast import Type
from RustParser.AST_Scripts.ast.ASTNode import ASTNode

class TopLevel(ASTNode):
    def __init__(self):
        # self.parent = program
        pass

    def accept(self, visitor):
        method_name = f'visit_{self.__class__.__name__}'
        return getattr(visitor, method_name, visitor.generic_visit)(self)

class FunctionDef(TopLevel):
    def __init__(self, identifier, params, return_type, body, unsafe=False):
        super().__init__()
        self.identifier = identifier
        self.params = params
        self.return_type = return_type
        self.body = body
        self.unsafe = unsafe

    def accept(self, visitor):
        method_Identifier = f'visit_{self.__class__.__name__}'
        return getattr(visitor, method_Identifier, visitor.generic_visit)(self)
    
    def getChildren(self):
        return self.body

    def setBody(self, body):
        self.body = body

class StructDef(TopLevel):
    def __init__(self, name, fields):
        super().__init__()
        self.name = name
        self.fields = fields

    def accept(self, visitor):
        method_name = f'visit_{self.__class__.__name__}'
        return getattr(visitor, method_name, visitor.generic_visit)(self)

class StructField(ASTNode):
    def __init__(self, name, typeExpr, visibility):
        super().__init__()
        self.name = name
        self.type = typeExpr
        self.visibility = visibility

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
    
    def getChildren(self):
        return self.items

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
    def __init__(self, name, fields, type, def_kind, visibility=None):
        self.name = name
        self.fields = fields
        self.visibility = visibility
        self.type_ = type
        self.def_kind = def_kind

class VarDefField(ASTNode):
    def __init__(self, name, type_, visibility=None):
        self.name       = name
        self.type_      = type_
        self.visibility = visibility

    def accept(self, visitor):
        return super().accept(visitor)

class InterfaceDef(TopLevel):
    def __init__(self, name: str, functions: list):
        super().__init__()
        self.name = name
        self.functions = functions or []

    def __repr__(self):
        return f"InterfaceDef(name={self.name}, functions={self.functions})"
    
    def getChildren(self):
        return self.functions
    
    def setFunctions(self, newFunctions):
        self.functions = newFunctions

class UseDecl(TopLevel):
    def __init__(self, paths, aliases=None):
        """
        :param paths: List of TypePath objects
        :param aliases: List of optional identifiers corresponding to each path
        """
        self.paths = paths  # list of TypePath
        self.aliases = aliases or [None] * len(paths)  # list of optional identifier strings

    def __repr__(self):
        parts = []
        for path, alias in zip(self.paths, self.aliases):
            if alias:
                parts.append(f"{path} as {alias}")
            else:
                parts.append(str(path))
        return f"UseDecl({', '.join(parts)})"

    def accept(self, visitor):
        return super().accept(visitor)