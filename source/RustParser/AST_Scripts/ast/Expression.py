from dataclasses import dataclass, field
from typing import List, Optional
from RustParser.AST_Scripts.ast.ASTNode import ASTNode
from RustParser.AST_Scripts.ast.Type import BoolType, IntType, StringType, FloatType
from RustParser.AST_Scripts.ast.common import DeclarationInfo

class Expression(ASTNode):
    def __init__(self, expr=None, type=None, isMutable=False, isUnsafe=False):
        super().__init__()
        self.type = type
        self.isMutable = isMutable
        self.expr = expr
        self.isUnsafe=isUnsafe

    def accept(self, visitor):
        #method_name = f'visit_{self.__class__.__name__}'
        return visitor.visit(self)
        #return getattr(visitor, method_name, visitor.generic_visit)(self)

class QualifiedExpression(Expression):
    def __init__(self, expr):
        super().__init__()
        self.expr = expr

    def accept(self, visitor):
        return visitor.visitQualifiedExpression(self)

class IdentifierExpr(Expression):
    def __init__(self, name, type=None):
        super().__init__(type)
        self.name = name

    def accept(self, visitor):
        return visitor.visitIdentifierExpr(self)

class BinaryExpr(Expression):
    def __init__(self, left, op, right):
        super().__init__()
        self.left = left
        self.op = op
        self.right = right

    def accept(self, visitor):
        return visitor.visiBbinaryExpr(self)

class LiteralExpr(Expression):
    def __init__(self, expr):
        super().__init__()
        self.expr = expr
        self.type = self.get_type()

    def accept(self, visitor):
        return visitor.visitLiteralExpr(self)

    def get_type(self):
        if isinstance(self.expr, int):
            return IntType()
        elif isinstance(self.expr, float):
            return FloatType()
        elif isinstance(self.expr, str):
            return StringType()
        elif isinstance(self.expr, bool):
            return BoolLiteral()
        elif isinstance(self.expr, bytes):
            return bytes()
        else:
            return None

class FunctionCall(Expression):
    def __init__(self, callee, args, caller=None):
        super().__init__()
        self.caller = caller
        self.callee = callee
        self.args = args

    def accept(self, visitor):
        return visitor.visit_FunctionCall(self)

class CastExpr(Expression):
    def __init__(self, type, expr=None, typePath=None):
        super().__init__(type)
        self.expr = expr
        self.type = type
        self.typePath = typePath

    def accept(self, visitor):
        return visitor.visit_CastExpr(self)

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
    def __init__(self, expr, isMutable=False):
        super().__init__()
        self.expr = expr
        self.isMutable = isMutable

    def accept(self, visitor):
        return visitor.visitBorrowExpr(self)

class BoolLiteral(Expression):
    def __init__(self, value: bool):
        super().__init__()
        self.value = value
        self.type = BoolType()

    def accept(self, visitor):
        return visitor.visitBoolLiteral(self)

class CharLiteral(Expression):
    def __init__(self, value: bool):
        super().__init__()
        self.value = value
        # self.type = CharLiteral(value=value)

    def accept(self, visitor):
        pass

class IntLiteral(Expression):
    def __init__(self, value: int):
        super().__init__()
        self.type = IntType()
        self.value = value

    def accept(self, visitor):
        return visitor.visitIntLiteral(self)

class StrLiteral(Expression):
    def __init__(self, value: str):
        super().__init__()
        self.value = value
        self.type = StringType()

    def accept(self, visitor):
        return visitor.visitStrLiteral(self)

class ArrayLiteral(Expression):
    def __init__(self, elements,name=None, count=None):
        super().__init__()
        self.count = count
        self.name = name
        self.elements = elements

    def accept(self, visitor):
        return visitor.visitArrayLiteral(self)

    def __repr__(self):
        return f"ArrayLiteral({self.elements})"

class UnaryExpr(Expression):
    def __init__(self, op, expr):
        super().__init__()
        self.op = op
        self.expr = expr

    def accept(self, visitor):
        return visitor.visit_UnaryExpr(self.expr)

class DereferenceExpr(Expression):
    def __init__(self, expr):
        super().__init__()
        self.expr = expr

    def accept(self, visitor):
        return visitor.visit_DereferenceExpr(self)

class BinaryExpr(Expression):
    def __init__(self, left, op, right):
        super().__init__()
        self.left = left
        self.op = op
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
        self.declarationInfo = DeclarationInfo(name=name, type=field_type)
        self.value = value

    def accept(self, visitor):
        return visitor.visit_StructLiteralField(self)

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
    def __init__(self, type_path, last_type):
        super().__init__()
        self.last_type = last_type
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
        return visitor.visit_TypeFullPathExpression(self)

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
        visitor.visit_RangeExpression(self)

class SafeWrapper(Expression):
    def __init__(self, expr):
        self.expr = expr

    def accept(self, visitor):
        visitor.visitSafeWrapper(self)