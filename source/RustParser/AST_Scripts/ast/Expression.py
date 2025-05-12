from RustParser.AST_Scripts.ast.ASTNode import ASTNode
from RustParser.AST_Scripts.ast.Type import IntType, StringType

class Expression(ASTNode):
    pass

class IdentifierExpr(Expression):
    def __init__(self, name):
        self.name = name

    def accept(self, visitor):
        return visitor.visit_identifier_expr(self)

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