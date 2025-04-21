from ast import FunctionDef
from AST_Scripts.ast.Type import IntType, StringType
from AST_Scripts.ast.TypeEnv import TypeEnv 

class TypeChecker:
    def __init__(self):
        self.env = TypeEnv()
        self.symbol_table = {}

    def get_literal_type(self, value):
        if isinstance(value, int):
            return IntType()
        elif isinstance(value, str):
            return StringType()
        else:
            raise Exception(f"❌ Unknown literal type for value: {repr(value)}")
        
    def visit_Type(self, ctx):
        type_str = ctx.getText()
        if type_str == "i32":
            return IntType()
        elif type_str == "String":
            return StringType()
        else:
            raise Exception(f"Unknown type: {type_str}")

    def visit(self, node):
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
        return FunctionDef(name=name, params=params, return_type=return_type, body=body)

    def visit_LetStmt(self, node):
        expr_type = self.visit(node.value)
        if expr_type.__class__ != node.declared_type.__class__:
            raise Exception(f"Type mismatch in declaration of '{node.name}'")
        self.env.declare(node.name, expr_type)
        self.symbol_table[node.name] = expr_type
        print(f"✅ '{node.name}' declared with type {expr_type.__class__.__name__}")

    def visit_Assignment(self, node):
        var_type = self.symbol_table.get(node.target)
        expr_type = self.visit(node.value)
        if (var_type.__class__) != (expr_type.__class__):
            raise Exception(f"Type mismatch in assignment to '{node.target}'")
