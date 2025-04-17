from ASTNode import ASTNode

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

class FunctionCallExpr(Expression):
    def __init__(self, func, args):
        self.func = func
        self.args = args

    def accept(self, visitor):
        return visitor.visit_function_call_expr(self)
