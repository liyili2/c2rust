from Type import IntType
from TypeEnv import TypeEnv 

class TypeChecker:
    def __init__(self):
        self.env = TypeEnv()

    def visit(self, node):
        return node.accept(self)

    def generic_visit(self, node):
        raise Exception(f"No visit method for {node.__class__.__name__}")

    def visit_LiteralExpr(self, node):
        if isinstance(node.value, int):
            return IntType()
        else:
            raise Exception(f"Unknown literal type: {node.value}")

    def visit_LetStmt(self, node):
        expr_type = self.visit(node.value)
        if node.declared_type and not isinstance(expr_type, node.declared_type.__class__):
            raise Exception(f"Type mismatch in declaration of '{node.name}'")
        self.env.declare(node.name, expr_type)
        print(f"✅ '{node.name}' declared with type {expr_type.__class__.__name__}")
