import abc
from typing import List
from rust.ast.ASTNode import ASTNode, CloneableASTNode
from rust.ast.Expression import TypePath
from rust.ast.RustASTVisitor import RustASTVisitor


class Type(CloneableASTNode, abc.ABC):
    pass


class SignedIntType(Type):

    def __init__(self, ptype: str):
        super().__init__()
        self.ptype = ptype

    def accept(self, visitor: RustASTVisitor):
        return visitor.visitSignedIntType(self)


class UnsignedIntType(Type):

    def __init__(self, ptype: str):
        super().__init__()
        self.ptype = ptype

    def accept(self, visitor: RustASTVisitor):
        return visitor.visitUnsignedIntType(self)


class FloatingPointType(Type):

    def __init__(self, ptype: str):
        super().__init__()
        self.ptype = ptype

    def accept(self, visitor: RustASTVisitor):
        return visitor.visitFloatingPointType(self)


class BoolType(Type):

    def __init__(self):
        super().__init__()

    def accept(self, visitor: RustASTVisitor):
        return visitor.visitBoolType(self)


class CharType(Type):

    def __init__(self):
        super().__init__()

    def accept(self, visitor: RustASTVisitor):
        return visitor.visitCharType(self)


class StringType(Type):

    def __init__(self):
        super().__init__()

    def accept(self, visitor: RustASTVisitor):
        return visitor.visitStringType(self)


class SafeNonNullWrapper(Type):

    def __init__(self, dtype: Type):
        super().__init__()
        self.dtype = dtype

    def accept(self, visitor: RustASTVisitor):
        return visitor.visitSafeNonNullWrapper(self)


class ArrayType(Type):

    def __init__(self, dtype: Type, size: int = None):
        super().__init__()
        self.dtype = dtype
        self.size = size

    def accept(self, visitor: RustASTVisitor):
        return visitor.visitArrayType(self)


class PathType(Type):

    def __init__(self, type_path: TypePath, dtype: Type):
        super().__init__()
        self.type_path = type_path
        self.dtype = dtype

    def accept(self, visitor: RustASTVisitor):
        return visitor.visitPathType(self)


class GenericType(Type):

    def __init__(self, generic_dtypes: List[Type], type_path: TypePath = None):
        super().__init__()
        self.generic_dtypes = generic_dtypes
        self.type_path = type_path

    def accept(self, visitor: RustASTVisitor):
        return visitor.visitGenericType(self)


class ReferenceType(Type):

    def __init__(self, dtype: Type):
        super().__init__()
        self.dtype = dtype

    def accept(self, visitor: RustASTVisitor):
        return visitor.visitReferenceType(self)


class SliceType(Type):

    def __init__(self, dtype: Type):
        super().__init__()
        self.dtype = dtype

    def accept(self, visitor: RustASTVisitor):
        return visitor.visitSliceType(self)


class UnitType(Type):

    def __init__(self):
        super().__init__()

    def accept(self, visitor: RustASTVisitor):
        return super().accept(visitor)


class PointerType(Type):

    def __init__(self, mutable: bool, dtype: Type):
        super().__init__()
        self.mutable = mutable
        self.dtype = dtype
    
    def accept(self, visitor: RustASTVisitor):
        return visitor.visitPointerType(self)


class UnknownType(Type):

    def __init__(self, ptype: str):
        super().__init__()
        self.ptype = ptype

    def accept(self, visitor: RustASTVisitor):
        return visitor.visitUnknownType(self)


## TODO: Type Checker used Types which should be eliminated later

class NoneType(Type):

    def __init__(self):
        super().__init__()

    def accept(self, visitor):
        return None


class StructType(Type):

    def __init__(self, name, fields, isUnion=False):
        super().__init__()
        self.name = name
        self.fields = fields
        self.isUnion = isUnion

    def accept(self, visitor):
        return super().accept(visitor)
