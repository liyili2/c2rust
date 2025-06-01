from ast import FunctionDef
from AST_Scripts.ast.Type import ArrayType, BoolType, IntType, RefType, StringType
from AST_Scripts.ast.TypeEnv import TypeEnv
from AST_Scripts.ast.Expression import BorrowExpr, FunctionCallExpr, IdentifierExpr, LiteralExpr 

class TypeChecker:
    def __init__(self):
        self.env = TypeEnv()
        self.symbol_table = {}
        self.error_count = 0

    def increase_error_count(self):
        self.error_count = self.error_count + 1

    def resolve_function_return_type(self, node):
        func_name = node.func
        func_info = self.env.lookup_function(func_name)
        if func_info["kind"] != "function":
            self.increase_error_count()
        return func_info["return_type"]

    def get_literal_type(self, value):
        if isinstance(value, int):
            return IntType()
        elif isinstance(value, str):
            return StringType()
        elif isinstance(value, bool):
            return BoolType()
        else:
            self.increase_error_count()

    def visit_Type(self, ctx):
        type_str = ctx.getText()
        if type_str == "i32":
            return IntType()
        elif ctx.getText() == "bool":
            return BoolType()
        elif type_str == "String":
            return StringType()
        else:
            self.increase_error_count()

    def visit(self, node):
        if node is None:
            self.increase_error_count()
        if isinstance(node, list):
            return [self.visit(n) for n in node]
        if hasattr(node, 'accept'):
            return node.accept(self)
        return node

    def visit_Program(self, node):
        for item in node.items:
            if not self.visit(item):
                self.increase_error_count()
        return True

    def visit_FunctionDef(self, ctx):
        name = ctx.Identifier
        if len(ctx.params) != 0:
            params = self.visit(ctx.params)
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
    
    def visit_LetStmt(self, node):
        expr_type = self.visit(node.value)
        if node.declared_type is not None:
            declared_type = self.visit(node.declared_type)
            if type(declared_type) != type(expr_type) and not isinstance(expr_type, RefType):
                self.increase_error_count()
        else:
            declared_type = expr_type

        self.env.declare(node.name, declared_type)
        self.symbol_table[node.name] = declared_type

        if isinstance(node.value, IdentifierExpr):
            try:
                value_info = self.env.lookup(node.value.name)
            except Exception:
                self.increase_error_count()
                value_info = None

            if value_info:
                if value_info["borrowed"]:
                    self.increase_error_count()
                if not value_info["owned"]:
                    self.increase_error_count()
                value_info["owned"] = False

        elif isinstance(node.value, BorrowExpr):
            try:
                value_info = self.env.lookup(node.value.name)
            except Exception:
                self.increase_error_count()
                value_info = None

            if value_info:
                if node.value.mutable and not value_info["mutable"]:
                    self.increase_error_count()
                if value_info["borrowed"]:
                    self.increase_error_count()
                value_info["borrowed"] = True
        return True        

    def visit_Assignment(self, node):
        try:
            info = self.env.lookup(node.target)
        except Exception:
            self.increase_error_count()
            return

        if not info["owned"]:
            self.increase_error_count()
        if info["borrowed"]:
            self.increase_error_count()

        expr_type = self.visit(node.value)

        if type(info["type"]) != type(expr_type):
            self.increase_error_count()

        if isinstance(node.value, IdentifierExpr):
            try:
                value_info = self.env.lookup(node.value.name)
            except Exception:
                self.increase_error_count()
                value_info = None

            if value_info:
                if not value_info["owned"]:
                    self.increase_error_count()
                value_info["owned"] = False

        if isinstance(node.value, BorrowExpr):
            try:
                value_info = self.env.lookup(node.value.name)
            except Exception:
                self.increase_error_count()
                value_info = None

            if value_info:
                if node.value.mutable and not value_info["mutable"]:
                    self.increase_error_count()
                if value_info["borrowed"]:
                    self.increase_error_count()
                value_info["borrowed"] = True
        return True

    def visit_IfStmt(self, node):
        condition_type = self.visit(node.condition)

        if not isinstance(condition_type, BoolType):
            self.increase_error_count()

        for stmt in node.then_branch:
            self.visit(stmt)

        if node.else_branch:
            for stmt in node.else_branch:
                self.visit(stmt)

        return True

    def visit_ForStmt(self, node):
        iterable_type = self.visit(node.iterable)

        if not isinstance(iterable_type, ArrayType):
            self.increase_error_count()
            return

        self.env.define(node.var, {
            "type": iterable_type.elem_type,
            "owned": True, "borrowed": False})

        for stmt in node.body:
            self.visit(stmt)

        return True

    def visit_FunctionCallExpr(self, node):
        func_info = self.env.lookup_function(node.func)
        if not func_info or func_info["kind"] != "function":
            self.increase_error_count()
            return None

        for arg in node.args:
            if isinstance(arg, IdentifierExpr):
                try:
                    info = self.env.lookup(arg.name)
                except Exception:
                    self.increase_error_count()
                    continue

                if not info["owned"] or info["borrowed"]:
                    self.increase_error_count()

                info["borrowed"] = True

        arg_types = [self.visit(arg) for arg in node.args]
        expected_types = func_info["param_types"]

        if len(arg_types) != len(expected_types):
            self.increase_error_count()
        else:
            for actual, expected in zip(arg_types, expected_types):
                if type(actual) != type(expected):
                    self.increase_error_count()

        for arg in node.args:
            if isinstance(arg, IdentifierExpr):
                info = self.env.lookup(arg.name)
                info["borrowed"] = False
                info["owned"] = False

        return func_info["return_type"]

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
            self.increase_error_count()

    def visit_IdentifierExpr(self, node):
        try:
            info = self.env.lookup(node.name)
        except Exception:
            self.increase_error_count()
            return None

        if not info["owned"]:
            self.increase_error_count()

        if node.name not in self.symbol_table:
            self.increase_error_count()
            return None

        return self.symbol_table[node.name]

    def visit_BorrowExpr(self, node):
        info = self.env.lookup(node.name)
        if not info["owned"]:
            self.increase_error_count()

        if node.mutable:
            if not info["mutable"]:
                self.increase_error_count()
            if info["borrowed"]:
                self.increase_error_count()
        else:
            if info["borrowed"]:
                self.increase_error_count()

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

    def visit_CallExpression(self, node):
        pass
        # return FunctionCallExpr(func=node.func, args=node.args)

    def visit_PrimaryExpression(self, node):
        pass