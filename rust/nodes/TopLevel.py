from rust.nodes.ASTNode import ASTNode, CloneableASTNode
from rust.commons.DeclarationInfo import DeclarationInfo
from rust.nodes.Program import Program


class TopLevel(CloneableASTNode):

    def __init__(self):
        super(TopLevel, self).__init__()

    def accept(self, visitor):
        return visitor.visit(self)


class FunctionDefinition(TopLevel):

    def __init__(self, identifier, params, return_type, body, is_unsafe=False):
        super().__init__()
        self._identifier = identifier
        self._params = params
        self._return_type = return_type
        self._body = body
        self._is_unsafe = is_unsafe

    def accept(self, visitor):
        return visitor.visitFunctionDefinition(self)

    def identifier(self):
        return self._identifier

    def params(self):
        return self._params

    def return_type(self):
        return self._return_type

    def body(self):
        return self._body

    def is_unsafe(self):
        return self._is_unsafe


class StructDef(TopLevel):

    def __init__(self, name, fields, vis=None):
        super().__init__()
        self._name = name
        self._fields = fields
        self._visibility = vis # Just leave the struct def and remove the struct field, move it into here instead

    def accept(self, visitor):
        return visitor.visitStruct(self)

    def name(self):
        return self._name

    def fields(self):
        return self._fields

    def visibility(self):
        return self._visibility


class Attribute(TopLevel):

    def __init__(self, name, args=None):
        super().__init__()
        self._name = name
        self._args = args or []

    def accept(self, visitor):
        return visitor.visitAttribute(self)

    def name(self):
        return self._name

    def args(self):
        return self._args


class ExternBlock(TopLevel):

    def __init__(self, name: str, program: Program):
        super().__init__()
        self._name = name
        self._program = program

    def accept(self, visitor):
        return visitor.visitExternBlock(self)

    def name(self):
        return self._name

    def program(self):
        return self._program


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
            f"type={self.declarationInfo.dtype}, "
            f"isMutable={self.isMutable}, "
            f"visibility={self.declarationInfo.visibility}, "
            f"initial_value={self.initial_value})")
    
    def accept(self, visitor):
        return visitor.visit_StaticVarDecl(self)


class ExternFunctionDeclaration(TopLevel):

    def __init__(self, name, params, return_type=None, visibility=None):
        super().__init__()
        self._name = name  # function name (string)
        self._params = params  # list of parameter types (AST nodes or strings)
        self._return_type = return_type  # return type (AST node or string), or None for `-> ()`
        self._visibility = visibility  # e.g., 'pub', or None

    def accept(self, visitor):
        return visitor.visitExternFunctionDeclaration(self)

    def name(self):
        return self._name

    def params(self):
        return self._params

    def return_type(self):
        return self._return_type

    def visibility(self):
        return self._visibility


class TypeAliasDecl(TopLevel):
    def __init__(self, name, type, visibility=None):
        self.declarationInfo = DeclarationInfo(name=name, type=type, visibility=visibility)

class TopLevelVarDef(TopLevel):
    def __init__(self, name, initial_val, fields, type, def_kind, isUnsafe=False, visibility=None):
        self.declarationInfo = DeclarationInfo(name=name, type=type, visibility=visibility)
        self.fields = fields
        self.def_kind = def_kind # union, const, etc.
        self.isUnsafe = isUnsafe
        self.initial_val = initial_val

    def accept(self, visitor):
        return visitor.visit_TopLevelVarDef(self)

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
        super().__init__()
        self._paths = paths  # list of TypePath
        self._aliases = aliases or [None] * len(paths)

    def accept(self, visitor):
        return super().accept(visitor)

    def paths(self):
        return self._paths

    def aliases(self):
        return self._aliases