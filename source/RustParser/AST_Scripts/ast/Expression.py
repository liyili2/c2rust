from RustParser.AST_Scripts.ast.ASTNode import ASTNode
from RustParser.AST_Scripts.ast.Type import IntType, StringType

class Expression(ASTNode):
    pass

class IdentifierExpr(Expression):
    def __init__(self, name):
        self.name = name

    def accept(self, visitor):
        return visitor.visitPrimaryExpression(self)

class BinaryExpr(Expression):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def accept(self, visitor):
        return visitor.visit_binary_expr(self)

class LiteralExpr(Expression):
    def __init__(self, value):
        self.value = value

    def accept(self, visitor):
        return visitor.visit_LiteralExpr(self)
    
    def get_type(self):
        print("literal is ", self.value)
        if isinstance(self.value, int):
            return IntType()
        elif isinstance(self.value, str):
            return StringType()
        elif isinstance(self.value, bool):
            return BoolLiteral()
        else:
            raise Exception("Unknown literal type")

class FunctionCallExpr(Expression):
    def __init__(self, func, args):
        self.func = func
        self.args = args

    def accept(self, visitor):
        return visitor.visit_FunctionCallExpr(self)

class BorrowExpr(Expression):
    def __init__(self, name, mutable=False):
        self.name = name
        self.mutable = mutable

    def accept(self, visitor):
        return visitor.visit_BorrowExpr(self)

class VariableRef(Expression):
    def __init__(self, name):
        self.name = name

    def accept(self, visitor):
        return visitor.visit_VariableRef(self)

class BoolLiteral:
    def __init__(self, value: bool):
        self.value = value

    def accept(self, visitor):
        return visitor.visit_BoolLiteral(self)

class IntLiteral:
    def __init__(self, value: int):
        self.value = value

    def accept(self, visitor):
        return visitor.visit_IntLiteral(self)

class StrLiteral:
    def __init__(self, value: str):
        self.value = value

    def accept(self, visitor):
        return visitor.visit_StrLiteral(self)

class ArrayLiteral:
    def __init__(self, elements):
        self.elements = elements
        # self.line = None
        # self.column = None

    def accept(self, visitor):
        return visitor.visitArrayLiteral(self)

    def __repr__(self):
        return f"ArrayLiteral({self.elements})"

class RepeatArrayLiteral:
    def __init__(self, elements, count, line=None, column=None):
        self.elements = elements
        self.count = count
        # self.line = line
        # self.column = column

class CastExpr:
    def __init__(self, expr, target_type, line=None, column=None):
        self.expr = expr
        self.target_type = target_type
        # self.line = line
        # self.column = column

class UnaryExpr(Expression):
    def __init__(self, op, expr):
        self.op = op
        self.expr = expr

    def accept(self, visitor):
        return visitor.visitExpression(self.expr)

class MethodCallExpr:
    def __init__(self, receiver, method_name, args, line=None, column=None):
        self.receiver = receiver
        self.method_name = method_name
        self.args = args or []
        # self.line = line
        # self.column = column

class DereferenceExpr:
    def __init__(self, expr):
        self.expr = expr

    def accept(self, visitor):
        return visitor.visitDereferenceExpr(self)

class BinaryExpr:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op  # e.g., '!=', '==', '+', etc.
        self.right = right

class CharLiteralExpr(Expression):
    def __init__(self, value):
        self.value = value

    def accept(self, visitor):
        return visitor.visitCharLiteralExpr(self)
    
class FieldAccessExpr(Expression):
    def __init__(self, receiver, field_name):
        self.receiver = receiver
        self.field_name = field_name

    def accept(self, visitor):
        return visitor.visitFieldAccessExpr(self)

class IndexExpr(Expression):
    def __init__(self, target, index):
        self.target = target
        self.index = index

    def accept(self, visitor):
        return visitor.visitIndexExpr(self)

class ParenExpr(Expression):
    def __init__(self, inner_expr):
        self.inner_expr = inner_expr

    def accept(self, visitor):
        return visitor.visitParenExpr(self)

    def __repr__(self):
        return f"ParenExpr({self.inner_expr})"
    
class StructLiteralField:
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def accept(self, visitor):
        return visitor.visitStructLiteralField(self)

class StructLiteralExpr(Expression):
    def __init__(self, struct_name, fields):
        self.struct_name = struct_name
        self.fields = fields

    def accept(self, visitor):
        return visitor.visitStructLiteralExpr(self)