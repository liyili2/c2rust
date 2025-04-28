from ast import FunctionDef
from AST_Scripts.ast.Type import ArrayType, BoolType, IntType, RefType, StringType
from AST_Scripts.ast.TypeEnv import TypeEnv
from AST_Scripts.ast.Expression import IdentifierExpr, LiteralExpr 

class TypeChecker:
    def __init__(self):
        self.env = TypeEnv()
        self.symbol_table = {}

    def resolve_function_return_type(self, node):
        func_name = node.func
        func_info = self.env.lookup_function(func_name)
        if func_info["kind"] != "function":
            return False
        return func_info["return_type"]

    def get_literal_type(self, value):
        if isinstance(value, int):
            return IntType()
        elif isinstance(value, str):
            return StringType()
        elif isinstance(value, bool):
            return BoolType()
        else:
            raise Exception(f"❌ Unknown literal type for value: {repr(value)}")

    def visit_Type(self, ctx):
        type_str = ctx.getText()
        if type_str == "i32":
            return IntType()
        elif ctx.getText() == "bool":
            return BoolType()
        elif type_str == "String":
            return StringType()
        else:
            raise Exception(f"Unknown type: {type_str}")

    def visit(self, node):
        if node is None:
            raise Exception("❌ TypeChecker received None as a node — check your Transformer.")
        if isinstance(node, list):
            return [self.visit(n) for n in node]
        if hasattr(node, 'accept'):
            return node.accept(self)
        return node

    def generic_visit(self, node):
        raise Exception(f"No visit method for {node.__class__.__name__}")

    def visit_Program(self, node):
        for item in node.items:
            if not self.visit(item):
                return False
        return True

    def visit_IntType(self, node):
        return node

    def visit_BoolType(self, node):
        return BoolType()

    def visit_LiteralExpr(self, node):
        if isinstance(node.value, int):
            return IntType()

        if isinstance(node.value, str):
            return StringType()
        
        if isinstance(node.value, bool):
            return BoolType()
        else:
            return False

    def visit_FunctionDef(self, ctx):
        name = ctx.Identifier
        if len(ctx.params) != 0:
            params = self.visit(ctx.params)  # should return List[(name, type)]
        else:
            params = []

        param_types = [typ for (name, typ) in params]
        if ctx.return_type != None:
            return_type = self.visit(ctx.return_type)
        else:
            return_type = None

        self.env.declare_function(name, param_types, return_type)
        body = self.visit(ctx.body)
        return FunctionDef(name=name, params=params, return_type=return_type, body=body)

    def visit_FunctionCallExpr(self, node):
        for arg in node.args:
            if isinstance(arg, IdentifierExpr):
                info = self.env.lookup(arg.name)
                if not info["owned"]:
                    return False
                info["owned"] = False

        return self.resolve_function_return_type(node)

    def visit_LetStmt(self, node):
        expr_type = self.visit(node.value)
        if node.declared_type is not None:
            declared_type = self.visit(node.declared_type)
            if declared_type.__class__ != expr_type.__class__:
                return False
        else:
            declared_type = expr_type

        self.env.declare(node.name, expr_type)
        self.symbol_table[node.name] = expr_type
        if isinstance(node.value, IdentifierExpr):
            try:
                value_info = self.env.lookup(node.value.name)
            except Exception:
                return False
            if value_info["borrowed"]:
                return False
            if not value_info["owned"]:
                return False
            value_info["owned"] = False

        return True

    def visit_Assignment(self, node):
        try:
            info = self.env.lookup(node.target)
        except Exception:
            return False
        if not info["owned"]:
            return False
        if info["borrowed"] :
            return False
        expr_type = self.visit(node.value)
        if type(info["type"]) != type(expr_type):
            return False
        if isinstance(node.value, IdentifierExpr):
            try:
                value_info = self.env.lookup(node.value.name)
            except Exception:
                return False
            if not value_info["owned"]:
                return False
            value_info["owned"] = False

        return True

    def visit_IfStmt(self, node):
        condition_type = self.visit(node.condition)
        if not isinstance(condition_type, BoolType):
            return False
        for stmt in node.then_branch:
            self.visit(stmt)
        if node.else_branch:
            for stmt in node.else_branch:
                self.visit(stmt)
        return True

    def visit_ForStmt(self, node):
        iterable_type = self.visit(node.iterable)
        if not isinstance(iterable_type, ArrayType):
            return False

        self.env.define(node.var, {"type": iterable_type.elem_type, "owned": True, "borrowed": False})
        for stmt in node.body:
            self.visit(stmt)
        return True

    def visit_identifier_expr(self, node):
        try:
            info = self.env.lookup(node.name)
        except Exception:
            return False
        if not info["owned"]:
            return False
        if node.name not in self.symbol_table:
            return False
        return self.symbol_table[node.name]

    def visit_BorrowExpr(self, node):
        info = self.env.lookup(node.name)
        if not info["owned"]:
            return False

        info["borrowed"] = True
        return RefType(info["type"])

    def visit_ArrayLiteral(self, node):
        first_elem = node.elements[0]
        return ArrayType(first_elem.__class__)

    def visit_BoolLiteral(self, node):
        return BoolType()

    def visit_IntLiteral(self, node):
        return IntType()

    def visit_StrLiteral(self, node):
        return StringType()
