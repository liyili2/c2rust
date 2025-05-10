from RustParser.AST_Scripts.ast.ASTNode import ASTNode

class Type:
    pass

class BoolType:
    def __repr__(self):
        return "Bool"

    def __eq__(self, other):
        return isinstance(other, BoolType)

class IntType(Type):
    def __repr__(self):
        return "i32"

class StringType(Type):
    def __repr__(self):
        return "String"

class StructType(Type):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Struct<{self.name}>"

class RefType(Type):
    def __init__(self, inner):
        self.inner = inner

    def __repr__(self):
        return f"&{self.inner}"

class ArrayType(Type):
    def __init__(self, elem_type, size=None):
        self.elem_type = elem_type
        self.size = size

    def __repr__(self):
        return f"[{self.elem_type}; {self.size}]" if self.size else f"[{self.elem_type}]"

class PointerType:
    def __init__(self, mutability: str, pointee_type=None):
        self.mutability = mutability  # True if 'mut', False if 'const'
        self.pointee_type = pointee_type  # Another type node, or None if not provided

    def __repr__(self):
        mutability = "mut" if self.mutability else "const"
        pointee = repr(self.pointee_type) if self.pointee_type else "?"
        return f"*{mutability} {pointee}"

    def to_dict(self):
        return {
            "type": "PointerType",
            "mutability": self.mutability,
            "pointee": self.pointee_type.to_dict() if self.pointee_type else None
        }
    
class ExternStaticVarDecl:
    def __init__(self, name: str, mutable: bool, var_type: Type):
        self.name = name
        self.mutable = mutable
        self.var_type = var_type

    def __repr__(self):
        mut = "mut " if self.mutable else ""
        return f"<ExternStaticVarDecl {mut}{self.name}: {self.var_type}>"
