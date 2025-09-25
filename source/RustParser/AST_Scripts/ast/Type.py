from RustParser.AST_Scripts.ast.ASTNode import ASTNode

class Type(ASTNode):
    pass

class VoidType:
    def __init__(self):
        self.name = "void"

    def __repr__(self):
        return "Void"

    def __eq__(self, other):
        return isinstance(other, VoidType)

    def __hash__(self):
        return hash("void")

    def accept(self, visitor):
        return super().accept(visitor)

class BoolType:
    def __init__(self):
        super().__init__()

    def __repr__(self):
        return "Bool"

    def __eq__(self, other):
        return isinstance(other, BoolType)
    
    def accept(self, visitor):
        return super().accept(visitor)

class IntType(Type):
    def __init__(self):
        super().__init__()

    def __repr__(self):
        return "i32"

    def accept(self, visitor):
        return visitor.visit_IntType(self)

class StringType(Type):
    def __init__(self):
        super().__init__()

    def __repr__(self):
        return "String"

    def accept(self, visitor):
        return super().accept(visitor)
    
class CharType(Type):
    def __init__(self):
        super().__init__()

    def __repr__(self):
        return "char"

    def accept(self, visitor):
        return super().accept(visitor)

class FloatType(Type):
    def __init__(self):
        super().__init__()

    def __repr__(self):
        return "float"
    
    def accept(self, visitor):
        return super().accept(visitor)

class StructType(Type):
    def __init__(self, name, fields, isUnion=False):
        super().__init__()
        self.name = name
        self.fields = fields
        self.isUnion = isUnion

    def __repr__(self):
        return f"Struct<{self.name}>"
    
    def accept(self, visitor):
        return super().accept(visitor)

class RefType(Type):
    def __init__(self, inner):
        super().__init__()
        self.inner = inner

    def __repr__(self):
        return f"&{self.inner}"
    
    def accept(self, visitor):
        return super().accept(visitor)

class ArrayType(Type):
    def __init__(self, var_type, size=None):
        super().__init__()
        self.var_type = var_type
        self.size = size

    def __repr__(self):
        return f"[{self.var_type}; {self.size}]" if self.size else f"[{self.var_type}]"
    
    def accept(self, visitor):
        return visitor.visit_ArrayType(self)

class PointerType(Type):
    def __init__(self, isMutable: str, pointee_type):
        super().__init__()
        self.isMutable = isMutable
        self.pointee_type = pointee_type

    def __repr__(self):
        isMutable = "mut" if self.isMutable else "const"
        pointee = repr(self.pointee_type) if self.pointee_type else "?"
        return f"*{isMutable} {pointee}"
    
    def accept(self, visitor):
        return visitor.visit_PointerType(self)

    def to_dict(self):
        return {
            "type": self.__class__.__name__,
            "pointee": self.pointee_type.to_dict() if isinstance(self.pointee_type, ASTNode) else self.pointee_type
        }

class PathType:
    def __init__(self, segments):
        super().__init__()
        self.segments = segments

class SafeNonNullWrapper(Type):
    def __init__(self, typeExpr):
        super().__init__()
        self.type = typeExpr

    def accept(self, visitor):
        return visitor.visit_SafeNonNullWrapper(self)
