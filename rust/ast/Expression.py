from typing import Any, List
from rust.ast.ASTNode import ASTNode, CloneableASTNode
from rust.ast.RustASTVisitor import RustASTVisitor
from rust.ast.Type import BoolType, IntType, StringType, FloatType, Type


class Expression(CloneableASTNode):

    def __init__(self, expression: Any = None, dtype: Type = None, is_mutable: bool = False, is_unsafe: bool = False):
        super().__init__()

        self.expression = expression
        self.dtype = dtype
        self.is_mutable = is_mutable
        self.is_unsafe = is_unsafe

    def accept(self, visitor: RustASTVisitor):
        return visitor.visit(self)

    def expression(self):
        return self.expression

    def type(self):
        return self.dtype

    def is_mutable(self):
        return self.is_mutable

    def is_unsafe(self):
        return self.is_unsafe


class QualifiedExpression(Expression):

    def __init__(self, expression: Any):
        super().__init__(expression = expression)

    def accept(self, visitor: RustASTVisitor):
        return visitor.visitQualifiedExpression(self)


class IdentifierExpression(Expression):
    def __init__(self, name: str, dtype: Type = None):
        super().__init__(dtype = dtype)
        self.name = name

    def accept(self, visitor: RustASTVisitor):
        return visitor.visitIdentifierExpr(self)


class BinaryExpression(Expression):

    def __init__(self, left: Expression, op: str, right: Expression):
        super().__init__()
        self.left = left
        self.op = op
        self.right = right

    def accept(self, visitor: RustASTVisitor):
        return visitor.visitBinaryExpr(self)


class ByteLiteralExpression(Expression):

    def __init__(self, expression: str):
        super().__init__(expression = expression)

    def accept(self, visitor: RustASTVisitor):
        return visitor.visitByteLiteralExpression(self)


class FunctionCallExpression(Expression):

    def __init__(self, callee: Expression, args: List[Expression], caller: Expression = None):
        super().__init__()
        self.caller = caller
        self.callee = callee
        self.args = args

    def accept(self, visitor: RustASTVisitor):
        return visitor.visitFunctionCallExpression(self)


class CastExpression(Expression):

    def __init__(self, dtype: Type, expression: Any = None, typePath: TypePathExpression = None):
        super().__init__(expression = expression, dtype = dtype)
        self.expr = expression
        self.type = dtype
        self.typePath = typePath

    def accept(self, visitor: RustASTVisitor):
        return visitor.visitCastExpression(self)


class BorrowExpr(Expression):
    def __init__(self, expression, is_mutable=False):
        super().__init__()
        self.expr = expression
        self.isMutable = is_mutable

    def accept(self, visitor):
        return visitor.visit_BorrowExpr(self)

class BoolLiteral(Expression):
    def __init__(self, value: bool):
        super().__init__()
        self.value = value
        self.type = BoolType()

    def accept(self, visitor):
        return visitor.visit_BoolLiteral(self)

class CharLiteral(Expression):
    def __init__(self, value: bool):
        super().__init__()
        self.value = value
        # self.type = CharLiteral(value=value)

    def accept(self, visitor):
        return visitor.visit_CharLiteral(self)

class IntLiteral(Expression):
    def __init__(self, value: int):
        super().__init__()
        self.type = IntType()
        self.value = value

    def accept(self, visitor):
        return visitor.visit_IntLiteral(self)

class StrLiteral(Expression):
    def __init__(self, value: str):
        super().__init__()
        self.value = value
        self.type = StringType()

    def accept(self, visitor):
        return visitor.visit_StrLiteral(self)
    
class ArrayDeclaration(Expression):
    def __init__(self, identifier, size, force, value):
        super().__init__()
        self.identifier = identifier
        self.size = size
        self.force = force
        self.value = value

    def accept(self, visitor):
        pass
        return visitor.visit_StrLiteral(self)
    
class ArrayDeclaration(Expression):
    def __init__(self, identifier, size, force, value):
        super().__init__()
        self.identifier = identifier
        self.size = size
        self.force = force
        self.value = value

    def accept(self, visitor):
        pass

class ArrayLiteral(Expression):
    def __init__(self, elements,name=None, count=None):
        super().__init__()
        self.count = count
        self.name = name
        self.elements = elements

    def accept(self, visitor):
        return visitor.visit_ArrayLiteral(self)

    def __repr__(self):
        return f"ArrayLiteral({self.elements})"
    def len(self):
        return len(self.elements)
    def __len__(self):
        return len(self.elements)
    
class ArrayAccess(Expression):
    def __init__(self, name, expression, dtype=None, is_mutable=False, is_unsafe=False):
        super().__init__(expression, dtype, is_mutable, is_unsafe)
        self.name = name

    def accept(self, visitor):
        return visitor.visit_ArrayAccess(self)

class UnaryExpr(Expression):
    def __init__(self, op, expression):
        super().__init__()
        self.op = op
        self.expr = expression

    def accept(self, visitor):
        return visitor.visit_UnaryExpr(self)

class DereferenceExpr(Expression):
    def __init__(self, expression):
        super().__init__()
        self.expr = expression

    def accept(self, visitor):
        return visitor.visit_DereferenceExpr(self)

class FieldAccessExpr(Expression):
    def __init__(self, receiver, field_name):
        super().__init__()
        self.receiver = receiver
        self.name = field_name

    def accept(self, visitor):
        return visitor.visit_FieldAccessExpr(self)

class ParenExpr(Expression): 
    def __init__(self, expression):
        super().__init__()
        self.expr = expression

    def accept(self, visitor):
        return visitor.visit_ParenExpr(self)

    def __repr__(self):
        return f"ParenExpr({self.expr})"

class StructLiteralField(Expression):
    def __init__(self, name, value, field_type=None):
        super().__init__()
        self.declarationInfo = DeclarationInfo(name=name, type=field_type)
        self.value = value

    def accept(self, visitor):
        return visitor.visit_StructLiteralField(self)

class PatternExpr(Expression):
    def __init__(self, expression, pattern):
        super().__init__()
        self.expr = expression
        self.pattern = pattern

    def accept(self, visitor):
        return visitor.visit_PatternExpr(self)

class TypePathExpression(Expression):
    def __init__(self, type_path, last_type):
        super().__init__()
        self.last_type = last_type
        self.type_path = type_path

    def accept(self, visitor):
        return visitor.visit_TypePathExpression(self)

class RangeExpression(Expression):
    def __init__(self, initial, last):
        super().__init__()
        self.initial = initial
        self.last = last

    def accept(self, visitor):
        return visitor.visit_RangeExpression(self)

class SafeWrapper(Expression):
    def __init__(self, expression):
        self.expr = expression

    def accept(self, visitor):
        return visitor.visit_SafeWrapper(self)
    
class TypeWrapper(Expression):
    def __init__(self, expression):
        super().__init__(type)
        self.expr = expression

    def accept(self, visitor):
        return super().accept(visitor)