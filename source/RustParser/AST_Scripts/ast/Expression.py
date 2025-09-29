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
        return visitor.visit(self)

class QualifiedExpression(Expression):
    def __init__(self, expr):
        super().__init__()
        self.expr = expr

    def accept(self, visitor):
        return visitor.visit_QualifiedExpression(self)

class IdentifierExpr(Expression):
    def __init__(self, name, type=None):
        super().__init__(type)
        self.name = name

    def accept(self, visitor):
        return visitor.visit_IdentifierExpr(self)

class BinaryExpr(Expression):
    def __init__(self, left, op, right):
        super().__init__()
        self.left = left
        self.op = op
        self.right = right

    def accept(self, visitor):
        return visitor.visit_BinaryExpr(self)

class LiteralExpr(Expression):
    def __init__(self, expr):
        super().__init__()
        self.expr = expr
        self.expr = expr
        self.type = self.get_type()

    def accept(self, visitor):
        return visitor.visit_LiteralExpr(self)

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

class BorrowExpr(Expression):
    def __init__(self, expr, isMutable=False):
        super().__init__()
        self.expr = expr
        self.isMutable = isMutable
        self.isMutable = isMutable

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
        pass

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
        self.count = count
        self.name = name
        self.elements = elements

    def accept(self, visitor):
        return visitor.visit_ArrayLiteral(self)

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

class FieldAccessExpr(Expression):
    def __init__(self, receiver, field_name):
        super().__init__()
        self.receiver = receiver
        self.name = field_name

    def accept(self, visitor):
        return visitor.visit_FieldAccessExpr(self)

class ParenExpr(Expression):
    def __init__(self, expr):
        super().__init__()
        self.expr = expr
        self.expr = expr

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
    def __init__(self, expr, pattern):
        super().__init__()
        self.expr = expr
        self.pattern = pattern

    def accept(self, visitor):
        return self

class TypePathExpression(Expression):
    def __init__(self, type_path, last_type):
        super().__init__()
        self.last_type = last_type
        self.type_path = type_path

    def accept(self, visitor):
        return visitor.visit_TypePathExpression(self)

    def __repr__(self):
        return f"TypePathExpression(type_path={self.type_path}, value_expr={self.value_expr})"

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
        return visitor.visit_SafeWrapper(self)
    
class TypeWrapper(Expression):
    def __init__(self, expr):
        super().__init__(type)
        self.expr = expr

    def accept(self, visitor):
        return super().accept(visitor)