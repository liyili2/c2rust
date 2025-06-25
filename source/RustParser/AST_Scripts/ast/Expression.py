from dataclasses import dataclass, field
from typing import List, Optional
from RustParser.AST_Scripts.ast.ASTNode import ASTNode
from RustParser.AST_Scripts.ast.Type import IntType, StringType, FloatType

class Expression(ASTNode):
    def __init__(self, type=None):
        super().__init__()
        self.type = type

    def accept(self, visitor):
        method_name = f'visit_{self.__class__.__name__}'
        return getattr(visitor, method_name, visitor.generic_visit)(self)

class MutableExpr(Expression):
    def __init__(self, expr):
        super().__init__()
        self.expr = expr

    def accept(self, visitor):
        return visitor.visit_MutableExpr(self)

    def __repr__(self):
        return f"MutableExpr(expr={self.expr})"

class QualifiedExpression(Expression):
    def __init__(self, inner_expr):
        super().__init__()
        self.inner_expr = inner_expr

    def accept(self, visitor):
        return visitor.visit_QualifiedExpression(self)

class IdentifierExpr(Expression):
    def __init__(self, name, type=None):
        super().__init__(type)
        self.name = name

    def accept(self, visitor):
        return visitor.visit_PrimaryExpression(self)

class BinaryExpr(Expression):
    def __init__(self, left, op, right):
        super().__init__()
        self.left = left
        self.op = op
        self.right = right

    def accept(self, visitor):
        return visitor.visit_binaryExpr(self)

class LiteralExpr(Expression):
    def __init__(self, value):
        super().__init__()
        self.value = value
        self.type = self.get_type()

    def accept(self, visitor):
        return visitor.visit_LiteralExpr(self)

    def get_type(self):
        if isinstance(self.value, int):
            return IntType()
        elif isinstance(self.value, float):
            return FloatType()
        elif isinstance(self.value, str):
            return StringType()
        elif isinstance(self.value, bool):
            return BoolLiteral()
        elif isinstance(self.value, bytes):
            return bytes()
        else:
            return None

class FunctionCallExpr(Expression):
    def __init__(self, func, args, caller=None,):
        super().__init__()
        # self.caller = caller
        self.func = func
        self.args = args

    def accept(self, visitor):
        return visitor.visit_CallExpression(self)

class UnsafeExpression(Expression):
    def __init__(self, expr):
        super().__init__()
        self.expr = expr

    def accept(self, visitor):
        return super().accept(visitor)

class BasicTypeCastExpr(Expression):
    def __init__(self, basicType, typePath):
        self.basicType = basicType
        self.typePath = typePath

    def accept(self, visitor):
        return super().accept(visitor)

class TypeAccessExpr(Expression):
    def __init__(self, expr, typeExpr):
        super().__init__(type)
        self.expr = expr
        self.type = typeExpr

    def accept(self, visitor):
        return super().accept(visitor)
    
class TypeWrapperExpr(Expression):
    def __init__(self, expr):
        super().__init__(type)
        self.expr = expr

    def accept(self, visitor):
        return super().accept(visitor)

class BoxWrapperExpr(Expression):
    def __init__(self, expr, path):
        super().__init__(type)
        self.expr = expr
        self.path = path

    def accept(self, visitor):
        return super().accept(visitor)

class BorrowExpr(Expression):
    def __init__(self, expr, mutable=False):
        super().__init__()
        self.expr = expr
        self.mutable = mutable

    def accept(self, visitor):
        return visitor.visit_BorrowExpr(self)

class VariableRef(Expression):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def accept(self, visitor):
        return visitor.visit_VariableRef(self)

class BoolLiteral(Expression):
    def __init__(self, value: bool):
        super().__init__()
        self.value = value

    def accept(self, visitor):
        return visitor.visit_BoolLiteral(self)

class IntLiteral(Expression):
    def __init__(self, value: int):
        super().__init__()
        self.value = value

    def accept(self, visitor):
        return visitor.visit_IntLiteral(self)

class StrLiteral(Expression):
    def __init__(self, value: str):
        super().__init__()
        self.value = value

    def accept(self, visitor):
        return visitor.visit_StrLiteral(self)

class ArrayLiteral(Expression):
    def __init__(self, name, elements):
        super().__init__()
        self.name = name
        self.elements = elements
        # self.line = None
        # self.column = None

    def accept(self, visitor):
        return visitor.visit_ArrayLiteral(self)

    def __repr__(self):
        return f"ArrayLiteral({self.elements})"

class RepeatArrayLiteral(Expression):
    def __init__(self, elements, count, line=None, column=None):
        super().__init__()
        self.elements = elements
        self.count = count
        # self.line = line
        # self.column = column

class CastExpr(Expression):
    def __init__(self, expr, type):
        super().__init__(type)
        self.expr = expr
        self.type = type

    def accept(self, visitor):
        return visitor.visit_CastExpr(self)

class UnaryExpr(Expression):
    def __init__(self, op, expr):
        super().__init__()
        self.op = op
        self.expr = expr

    def accept(self, visitor):
        return visitor.visitExpression(self.expr)

class MethodCallExpr(Expression):
    def __init__(self, receiver, method_name, args, line=None, column=None):
        super().__init__()
        self.receiver = receiver
        self.method_name = method_name
        self.args = args or []
        # self.line = line
        # self.column = column

class DereferenceExpr(Expression):
    def __init__(self, expr):
        super().__init__()
        self.expr = expr

    def accept(self, visitor):
        return visitor.visitDereferenceExpr(self)

class BinaryExpr(Expression):
    def __init__(self, left, op, right):
        super().__init__()
        self.left = left
        self.op = op  # e.g., '!=', '==', '+', etc.
        self.right = right

class CharLiteralExpr(Expression):
    def __init__(self, value):
        super().__init__()
        self.value = value

    def accept(self, visitor):
        return visitor.visitCharLiteralExpr(self)
    
class FieldAccessExpr(Expression):
    def __init__(self, receiver, field_name):
        super().__init__()
        self.receiver = receiver
        self.name = field_name

    def accept(self, visitor):
        return visitor.visit_FieldAccessExpr(self)

class IndexExpr(Expression):
    def __init__(self, target, index):
        super().__init__()
        self.target = target
        self.index = index

    def accept(self, visitor):
        return visitor.visitIndexExpr(self)

class ParenExpr(Expression):
    def __init__(self, inner_expr):
        super().__init__()
        self.inner_expr = inner_expr

    def accept(self, visitor):
        return visitor.visitParenExpr(self)

    def __repr__(self):
        return f"ParenExpr({self.inner_expr})"
    
class StructLiteralField(Expression):
    def __init__(self, name, value, field_type=None):
        super().__init__()
        self.name = name
        self.value = value
        self.field_type = field_type

    def accept(self, visitor):
        return visitor.visit_StructLiteralField(self)

class StructLiteralExpr(Expression):
    def __init__(self, struct_name, fields):
        super().__init__()
        self.struct_name = struct_name
        self.fields = fields

    def accept(self, visitor):
        return visitor.visitStructLiteralExpr(self)

class Pattern(Expression):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def accept(self, visitor):
        return visitor.visitPattern(self)

class PatternExpr(Expression):
    def __init__(self, expression, pattern):
        super().__init__()
        self.expression = expression
        self.pattern = pattern
        # print("accept: ", self.pattern, self.expression)

    def accept(self, visitor):
        # print("accept: ", self.pattern, self.expression)
        return self

class TypePathExpression(Expression):
    def __init__(self, type_path):
        super().__init__()
        self.type_path = type_path  # list of strings

    def accept(self, visitor):
        return visitor.visitTypePathExpression(self)

    # def __repr__(self):
    #     return f"TypePathExpression(type_path={self.type_path}, value_expr={self.value_expr})"

class TypePathFullExpr(Expression):
    def __init__(self, type_path, value_expr):
        super().__init__()
        self.type_path = type_path
        self.value_expr = value_expr

    def accept(self, visitor):
        return visitor.visitExpression(self)

class ArrayDeclaration(Expression):
    def __init__(self, identifier, size, force, value):
        super().__init__()
        self.identifier = identifier
        self.size = size
        self.force = force
        self.value = value

    def accept(self, visitor):
        pass

class RangeExpression(Expression):
    def __init__(self, initial, last):
        super().__init__()
        self.initial = initial
        self.last = last

    def accept(self, visitor):
        pass

class StructDefInit(Expression):
    def __init__(self, name, expr):
        super().__init__()
        self.name = name  # e.g., 'my_struct'
        self.expr = expr

    def accept(self, visitor):
        pass