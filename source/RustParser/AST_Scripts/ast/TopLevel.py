from RustParser.AST_Scripts.ast.ASTNode import ASTNode
from RustParser.AST_Scripts.ast.common import DeclarationInfo
from RustParser.AST_Scripts.ast.common import DeclarationInfo

class TopLevel(ASTNode):
    def __init__(self):
        pass

    def accept(self, visitor):
        method_name = f'visit_{self.__class__.__name__}'
        return getattr(visitor, method_name, visitor.generic_visit)(self)

class FunctionDef(TopLevel):
    def __init__(self, identifier, params, return_type, body, isUnsafe=False):
        super().__init__()
        self.identifier = identifier
        self.params = params
        self.return_type = return_type
        self.body = body
        self.isUnsafe = isUnsafe

    def accept(self, visitor):
        #method_Identifier = f'visit_{self.__class__.__name__}'
        return visitor.visit_FunctionDef(self)
    
    def getChildren(self):
        return self.body

    def setBody(self, body):
        self.body = body

    def setParamList(self, paramList):
        self.params = paramList

class StructDef(TopLevel):
    def __init__(self, name, fields):
        super().__init__()
        self.name = name
        self.fields = fields

    def accept(self, visitor):
        return visitor.visit_Struct(self)

    def getChildren(self):
        return self.fields

    def setChildren(self, fields):
        self.fields = fields

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
    pass

class ExternTypeDecl(ExternItem):
    def __init__(self, name: str, visibility: str = None):
        super().__init__()
        self.declarationInfo = DeclarationInfo(name=name, visibility=visibility)

    def __repr__(self):
        return f"<ExternTypeDecl {self.visibility or ''} type {self.name}>"
    
    def accept(self, visitor):
        pass

class StaticVarDecl(TopLevel):
    def __init__(self, name, var_type, isMutable, initial_value, visibility=None, isExtern=False):
        super().__init__()
        self.declarationInfo = DeclarationInfo(name=name, type=var_type, visibility=visibility)
        self.isMutable = isMutable
        self.initial_value = initial_value  # Expr: value assigned at declaration
        self.isExtern = isExtern

    def __repr__(self):
        return (
            f"StaticVarDecl(name={self.declarationInfo.name}, "
            f"type={self.declarationInfo.type}, "
            f"isMutable={self.isMutable}, "
            f"visibility={self.declarationInfo.visibility}, "
            f"initial_value={self.initial_value})")
    
    def accept(self, visitor):
        return visitor.visit_StaticVarDecl(self)

class ExternFunctionDecl(TopLevel):
    def __init__(self, name, params, return_type=None, variadic=False, visibility=None):
        self.name = name  # function name (string)
        self.params = params  # list of parameter types (AST nodes or strings)
        self.return_type = return_type  # return type (AST node or string), or None for `-> ()`
        self.visibility = visibility  # e.g., 'pub', or None

    def __repr__(self):
        return (
            f"ExternFunctionDecl(name={self.name!r}, params={self.params}, "
            f"return_type={self.return_type}, variadic={self.variadic}, "
            f"visibility={self.visibility})")

class TypeAliasDecl(TopLevel):
    def __init__(self, name, type, visibility=None):
        self.declarationInfo = DeclarationInfo(name=name, type=type, visibility=visibility)

class TopLevelVarDef(TopLevel):
    def __init__(self, name, fields, type, def_kind, isUnsafe=False, visibility=None):
        self.declarationInfo = DeclarationInfo(name=name, type=type, visibility=visibility)
        self.fields = fields
        self.def_kind = def_kind # union, const, etc.
        self.isUnsafe = isUnsafe

    def getChildren(self):
        return self.fields

class VarDefField(ASTNode):
    def __init__(self, name, type_, visibility=None):
        self.declarationInfo = DeclarationInfo(name=name, type=type_, visibility=visibility)

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

    def accept(self, visitor):
        return visitor.visit_InterfaceDef(self)

class UseDecl(TopLevel):
    def __init__(self, paths, aliases=None):
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