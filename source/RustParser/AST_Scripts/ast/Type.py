from RustParser.AST_Scripts.ast.ASTNode import ASTNode

class Type:
    pass

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
