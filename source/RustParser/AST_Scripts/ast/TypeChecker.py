from ast import FunctionDef
from RustParser.AST_Scripts.ast.Type import IntType, StringType
from RustParser.AST_Scripts.ast.TypeEnv import TypeEnv 

class TypeChecker:
    def __init__(self):
        self.env = TypeEnv()

    def visit(self, node):
        print("node is ", node)
        if node is None:
            raise Exception("❌ TypeChecker received None as a node — check your Transformer.")
        if isinstance(node, list):
            return [self.visit(n) for n in node]
        return node.accept(self)

    def generic_visit(self, node):
        raise Exception(f"No visit method for {node.__class__.__name__}")

    def visit_Program(self, node):
        print("📦 Visiting Program node")
        return self.visit(node.items)

    def visit_IntType(self, node):
        return node

    def visit_LiteralExpr(self, node):
        if isinstance(node.value, int):
            return IntType()

        if isinstance(node.value, str):
            return StringType()
        else:
            raise Exception(f"Unknown literal type: {node.value}")

    def visit_FunctionDef(self, ctx):
        name = ctx.Identifier
        if len(ctx.params) != 0:
            params = self.visit(ctx.params)  # should return List[(name, type)]
        else:
            params = []

        if ctx.return_type != None:
            return_type = self.visit(ctx.return_type)
        else:
            return_type = None

        body = self.visit(ctx.body)  # should be a List[Stmt]
        print("#2: block is ", body)
        return FunctionDef(name=name, params=params, return_type=return_type, body=body)

    def visit_LetStmt(self, node):
        expr_type = self.visit(node.value)
        if node.declared_type and not isinstance(expr_type, node.declared_type.__class__):
            raise Exception(f"Type mismatch in declaration of '{node.name}'")
        self.env.declare(node.name, expr_type)
        print(f"✅ '{node.name}' declared with type {expr_type.__class__.__name__}")
