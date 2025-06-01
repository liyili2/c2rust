from RustParser.AST_Scripts.ast.ASTNode import ASTNode

class Type(ASTNode):
    pass

class BoolType:
    def __init__(self):
        super().__init__()

    def __repr__(self):
        return "Bool"

    def __eq__(self, other):
        return isinstance(other, BoolType)

class IntType(Type):
    def __init__(self):
        super().__init__()

    def __repr__(self):
        return "i32"

class StringType(Type):
    def __init__(self):
        super().__init__()

    def __repr__(self):
        return "String"

class FloatType(Type):
    def __init__(self):
        super().__init__()

    def __repr__(self):
        return "float"

class StructType(Type):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def __repr__(self):
        return f"Struct<{self.name}>"

class RefType(Type):
    def __init__(self, inner):
        super().__init__()
        self.inner = inner

    def __repr__(self):
        return f"&{self.inner}"

class ArrayType(Type):
    def __init__(self, var_type, size=None):
        super().__init__()
        self.var_type = var_type
        self.size = size

    def __repr__(self):
        return f"[{self.var_type}; {self.size}]" if self.size else f"[{self.elem_type}]"
    
    def accept(self, visitor):
        return visitor.visit_ArrayType(self)

class PointerType(Type):
    def __init__(self, mutability: str, pointee_type):
        super().__init__()
        self.mutability = mutability
        self.pointee_type = pointee_type

    def __repr__(self):
        mutability = "mut" if self.mutability else "const"
        pointee = repr(self.pointee_type) if self.pointee_type else "?"
        return f"*{mutability} {pointee}"
    
    def accept(self, visitor):
        return super().accept(visitor)

    def to_dict(self):
        return {
            "type": self.__class__.__name__,
            "pointee": self.pointee_type.to_dict() if isinstance(self.pointee_type, ASTNode) else self.pointee_type
        }

class ExternStaticVarDecl:
    def __init__(self, name: str, mutable: bool, var_type: Type):
        super().__init__()
        self.name = name
        self.mutable = mutable
        self.var_type = var_type

    def __repr__(self):
        mut = "mut " if self.mutable else ""
        return f"<ExternStaticVarDecl {mut}{self.name}: {self.var_type}>"

class PathType:
    def __init__(self, segments):
        super().__init__()
        self.segments = segments