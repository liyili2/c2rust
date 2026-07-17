from typing import Any, List, Tuple
from rust.ast.ASTNode import ASTNode, CloneableASTNode
# from rust.ast.RustASTVisitor import RustASTVisitor
from rust.ast.Type import *


class Expression(CloneableASTNode):

    def __init__(self, dtype: Type = None, is_mutable: bool = False, is_unsafe: bool = False):
        super().__init__()
        self._dtype = dtype
        self._is_mutable = is_mutable
        self._is_unsafe = is_unsafe

    def accept(self, visitor):
        return visitor.visit(self)

    def type(self):
        return self._dtype

    def is_mutable(self):
        return self._is_mutable

    def is_unsafe(self):
        return self._is_unsafe


class QualifiedExpression(Expression):

    def __init__(self, expression: Expression):
        super().__init__()
        self._expression = expression

    def accept(self, visitor):
        return visitor.visitQualifiedExpression(self)

    def expression(self):
        return self._expression


class IdentifierExpression(Expression):

    def __init__(self, name: str, dtype: Type = None):
        super().__init__( dtype = dtype)
        self._name = name

    def accept(self, visitor):
        return visitor.visitIdentifierExpression(self)

    def name(self):
        return self._name


class VarDef(Expression):
    def __init__(self, name, isMutable=False, by_ref=False, var_type=None):
        # self.declarationInfo = DeclarationInfo(name=name, type=var_type)
        super().__init__(dtype=var_type, is_mutable=isMutable)
        self._name = name
        self._by_ref = by_ref

    def accept(self, visitor):
        return visitor.visitVarDef(self)

    def name(self):
        return self._name

    def by_ref(self):
        return self._by_ref


class BinaryExpression(Expression):

    def __init__(self, left: Expression, op: str, right: Expression):
        super().__init__()
        self._left = left
        self._op = op
        self._right = right

    def accept(self, visitor):
        return visitor.visitBinaryExpression(self)

    def left(self):
        return self._left

    def op(self):
        return self._op

    def right(self):
        return self._right


class ByteLiteralExpression(Expression):

    def __init__(self, expression: str):
        super().__init__()
        self._value = expression

    def accept(self, visitor):
        return visitor.visitByteLiteralExpression(self)

    def value(self):
        return self._value


class FunctionCallExpression(Expression):

    def __init__(self, caller: Expression,  args: List[Expression], callee: Expression = None):
        super().__init__()
        self._caller = caller
        self._callee = callee
        self._args = args

    def accept(self, visitor):
        return visitor.visitFunctionCallExpression(self)

    def callee(self):
        return self._callee

    def args(self):
        return self._args

    def caller(self):
        return self._caller


class CastExpression(Expression):

    def __init__(self, expression: Any = None, type_expressions: List[Expression] = None):
        super().__init__()
        self._expression = expression
        self._type = type_expressions

    def accept(self, visitor):
        return visitor.visitCastExpression(self)

    def expression(self):
        return self._expression

    def type(self):
        return self._type


class BorrowExpression(Expression):

    def __init__(self, expression: Any, is_mutable : bool = False):
        super().__init__(is_mutable = is_mutable)
        self._expression = expression

    def accept(self, visitor):
        return visitor.visitBorrowExpression(self)

    def expression(self):
        return self._expression


class Literal(Expression):
    def __init__(self, value, dtype):
        super().__init__(dtype = dtype)
        self._value = value

    def value(self):
        return self._value

    def accept(self, visitor):
        return visitor.visitLiteral(self)

class BooleanLiteral(Literal):

    def __init__(self, value):
        super().__init__(value = value, dtype = BoolType())


class CharLiteral(Literal):
    def __init__(self, value):
        super().__init__(value = value, dtype = CharType())
        # self.type = CharLiteral(value=value)

class IntLiteral(Literal):
    def __init__(self, value):
        super().__init__(value = value, dtype = SignedIntType("int"))

class StrLiteral(Literal):
    def __init__(self, value):
        super().__init__(value = value, dtype = StringType())


class ArrayLiteral(Literal):
    def __init__(self, elements,name=None, count=None):
        super().__init__(value = elements, dtype = ArrayType(name, count))

    def __repr__(self):
        return f"ArrayLiteral({self.value()})"
    def len(self):
        return len(self.value())
    def __len__(self):
        return len(self.value())

class ArrayDeclaration(Expression):
    def __init__(self, identifier, size, force, value):
        super().__init__()
        self._identifier = identifier
        self._size = size
        self._force = force
        self._value = value

    def accept(self, visitor):
        pass
        return visitor.visit_StrLiteral(self)


    def value(self):
        return self._value


    def id(self):
        return self._identifier

    def size(self):
        return self._size

    def force(self):
        return self._force

    
class ArrayAccess(Expression):
    def __init__(self, name, expression, dtype=None, is_mutable=False, is_unsafe=False):
        super().__init__(dtype, is_mutable, is_unsafe)
        self._expression = expression
        self._name = name

    def accept(self, visitor):
        return visitor.visitArrayAccess(self) # visitArrayAccess

    def name(self):
        return self._name

    def expression(self):
        return self._expression

class UnaryExpr(Expression):
    def __init__(self, op, expression):
        super().__init__()
        self._op = op
        self._expr = expression

    def accept(self, visitor):
        return visitor.visit_UnaryExpr(self)

    def op(self):
        return self._op

    def expression(self):
        return self._expr

class DereferenceExpr(Expression):
    def __init__(self, expression):
        super().__init__()
        self._expr = expression

    def accept(self, visitor):
        return visitor.visit_DereferenceExpr(self)

    def expression(self):
        return self._expr

class FieldAccessExpr(Expression):
    def __init__(self, receiver, next):
        super().__init__()
        self._receiver = receiver
        self._next = next

    def accept(self, visitor):
        return visitor.visitFieldAccessExpr(self)

    def receiver(self):
        return self._receiver

    def next(self):
        return self._next

class ParenExpr(Expression): 
    def __init__(self, expression):
        super().__init__()
        self._expr = expression

    def accept(self, visitor):
        return visitor.visit_ParenExpr(self)

    def __repr__(self):
        return f"ParenExpr({self.expression()})"

    def expression(self):
        return self._expr

class StructLiteralField(Expression):
    def __init__(self, name, value, field_type=None):
        super().__init__(dtype = field_type)
        # self.declarationInfo = DeclarationInfo(name=name, type=field_type)
        self._value = value
        self._name = name

    def accept(self, visitor):
        return visitor.visit_StructLiteralField(self)

    def name(self):
        return self._name

    def value(self):
        return self._value


class PatternExpr(Expression):
    def __init__(self, expression, pattern):
        super().__init__()
        self._expr = expression
        self._pattern = pattern

    def accept(self, visitor):
        return visitor.visit_PatternExpr(self)

    def expression(self):
        return self._expr

    def pattern(self):
        return self._pattern


class TypePath(Expression):

    def __init__(self, types: List[str]):
        super().__init__()
        self._types = types

    def accept(self, visitor):
        return visitor.visitTypePath(self)

    def types(self):
        return self._types

class TypePathExpression(Expression):
    def __init__(self, type_path, last_type):
        super().__init__(dtype = last_type)
        self._type_path = type_path

    def accept(self, visitor):
        return visitor.visit_TypePathExpression(self)

    def type_path(self):
        return self._type_path

class RangeExpression(Expression):
    def __init__(self, initial, last):
        super().__init__()
        self._initial = initial
        self._last = last

    def accept(self, visitor):
        return visitor.visitRangeExpression(self)

    def initial(self):
        return self._initial

    def last(self):
        return self._last

class SafeWrapper(Expression):
    def __init__(self, expression):
        super().__init__()
        self._expr = expression

    def accept(self, visitor):
        return visitor.visit_SafeWrapper(self)

    def expression(self):
        return self._expr
    
class TypeWrapper(Expression):
    def __init__(self, expression):
        super().__init__()
        self._expr = expression

    def accept(self, visitor):
        return super().accept(visitor)

    def expression(self):
        return self._expr