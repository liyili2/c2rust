from ast import FunctionDef
from AST_Scripts.ast.Type import ArrayType, BoolType, FloatType, IntType, RefType, StringType, StructType
from AST_Scripts.ast.TypeEnv import TypeEnv
from AST_Scripts.ast.Expression import BorrowExpr, CastExpr, FunctionCallExpr, IdentifierExpr, LiteralExpr 

class TypeChecker:
    def __init__(self):
        self.env = TypeEnv()
        self.symbol_table = {}
        self.error_count = 0
        self.errors = []

    def error(self, node, message):
        error_msg = f"Type error: {message}"
        if hasattr(node, 'line'):
            error_msg = f"[Line {node.line}] {error_msg}"
        print(error_msg)
        self.errors.append(error_msg)
        self.increase_error_count()

    def increase_error_count(self):
        self.error_count = self.error_count + 1
    
    def is_type_compatible(self, expected, actual):
        return expected == actual

    def generic_visit(self, node):
        raise NotImplementedError(f"No visit_{type(node).__name__} method defined.")

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
        name = ctx.identifier

        if ctx.params is not None:
            params = self.visit(ctx.params)
        else:
            params = []

        param_types = [typ for (_, typ, _) in params]

        if ctx.return_type is not None:
            return_type = self.visit(ctx.return_type)
        else:
            return_type = None

        self.env.declare_function(name, param_types, return_type)
        body = self.visit(ctx.body)
        return FunctionDef(name=name, params=params, return_type=return_type, body=body)
    
    def visit_CastExpr(self, node: CastExpr):
        expr_type = self.visit(node.expr)
        target_type = self.visit(node.type)
        if expr_type == target_type:
            return target_type

        valid_numeric_types = (IntType, FloatType)
        if isinstance(expr_type, valid_numeric_types) and isinstance(target_type, valid_numeric_types):
            return target_type

        self.increase_error_count()
        return target_type
    
    def visit_StructLiteral(self, node):
        struct_type = self.visit(node.struct_type)
        if not isinstance(struct_type, StructType):
            self.error(node, f"{struct_type} is not a valid struct type")
            self.increase_error_count()
            return struct_type

        field_types = struct_type.fields
        used_fields = set()
        for field in node.fields:
            field_name = field.name
            if field_name not in field_types:
                self.error(field, f"Field '{field_name}' is not defined in struct '{struct_type.name}'")
                self.increase_error_count()
                continue

            expected_type = field_types[field_name]
            actual_type = self.visit(field.value)
            if not self.is_type_compatible(expected_type, actual_type):
                self.error(field, f"Type mismatch for field '{field_name}': expected {expected_type}, got {actual_type}")
                self.increase_error_count()
            used_fields.add(field_name)

        missing_fields = set(field_types.keys()) - used_fields
        if missing_fields:
            for mf in missing_fields:
                self.error(node, f"Missing field '{mf}' in struct literal of type '{struct_type.name}'")
                self.increase_error_count()

        return struct_type
    
    def visit_UnsafeBlock(self, node):
        result = self.visit(node.block)
        return result

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

    def visit_ReturnStmt(self, node):
        if node.value is None:
            return_type = "unit"  # or "void", depending on your type system
        else:
            return_type = self.visit(node.value)
        return return_type

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

    def visit_FunctionParamList(self, ctx):
        params = []
        for param_ctx in ctx.params:
            param = self.visit(param_ctx)
            params.append(param)
        return params

    def visit_VarDef(self, ctx):
        name = ctx.name
        typ = self.visit(ctx.var_type)
        return (name, typ)
    
    def visit_ParamNode(self, ctx):
        name = ctx.name
        typ = self.visit(ctx.typ)
        is_mut = ctx.is_mut
        return (name, typ, is_mut)

    def visit_FunctionParamList(self, ctx):
        params = []
        for param_ctx in ctx.params:
            name, typ, is_mut = self.visit(param_ctx)
            params.append((name, typ, is_mut))
        return params

    def visit_IntType(self, node):
        return node

    def visit_BoolType(self, node):
        return BoolType()
    
    def visit_binaryExpr(self, node):
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)

        if left_type != right_type:
            self.error(f"Type mismatch: cannot apply '{node.op}' to '{left_type}' and '{right_type}'")
            node.type = "error"
            return "error"

        if node.op in {"+", "-", "*", "/"}:
            if left_type != "int":
                self.error(f"Arithmetic operator '{node.op}' requires 'int' operands, got '{left_type}'")
                node.type = "error"
                return "error"
            node.type = "int"
            return "int"

        elif node.op in {"==", "!=", "<", ">", "<=", ">="}:
            node.type = "bool"
            return "bool"

        elif node.op in {"&&", "||"}:
            if left_type != "bool":
                self.error(f"Logical operator '{node.op}' requires 'bool' operands, got '{left_type}'")
                node.type = "error"
                return "error"
            node.type = "bool"
            return "bool"

        else:
            self.error(f"Unknown binary operator '{node.op}'")
            node.type = "error"
            return "error"
        
    def visit_ArrayType(self, node):
        elem_type = self.visit(node.elem_type)
        if node.size is not None:
            size_type = self.visit(node.size)
            if size_type != "i32":
                self.error(f"Array size must be of type i32, got {size_type}")
            if not isinstance(node.size, IntType):
                self.warning("Array size is not a constant literal — might be dynamic")
        return f"[{elem_type}; {node.size.value if hasattr(node.size, 'value') else '?'}]"
    
    def visit_MatchPattern(self, node):
        pattern_type = self.visit(node.value)
        if pattern_type not in ["i32", "bool", "char", "String", "enum_variant"]:
            self.error(f"Unsupported match pattern type: {pattern_type}")

        return pattern_type

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
    
    def visit_QualifiedExpression(self, node):
        inner_type = self.visit(node.inner_expr)
        return inner_type
    
    def visit_MutableExpr(self, node):
        inner_expr = self.visit(node.expr)
        if not isinstance(node.expr, IdentifierExpr):
            self.error(f"Only variables (identifiers) can be marked mutable. Got: {type(node.expr).__name__}")
            self.increase_error_count()
            return None

        var_name = node.expr.name
        if not self.env.is_declared(var_name):
            self.error(f"Variable '{var_name}' used before declaration.")
            self.increase_error_count()
            return None

        var_type = self.env.get_type(var_name)
        self.env.set_mutability(var_name, True)
        self.symbol_table[var_name]['mutable'] = True

        return var_type

    def visit_BorrowExpr(self, node):
        info = self.env.lookup(node.expr)
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
        if not node.elements:
            self.increase_error_count()
            return None

        elem_types = [self.visit(elem) for elem in node.elements]

        first_type = elem_types[0]
        for t in elem_types[1:]:
            if type(t) != type(first_type):
                self.increase_error_count()

        return ArrayType(first_type)
    
    def visit_CallStmt(self, node):
        expr_type = self.visit(node.callee)
        if not hasattr(node, 'call_postfix') or node.call_postfix is None:
            self.increase_error_count()
            return

        self.visit_callExpressionPostFix(node.call_postfix, node.expression)

    def visit_callExpressionPostFix(self, node, func_expr):
        if not hasattr(node, 'args'):
            self.increase_error_count()
            return

        args = self.visit(node.args) if hasattr(node, 'args') else []
        if isinstance(func_expr, IdentifierExpr):
            func_name = func_expr.name
        else:
            self.increase_error_count()
            return

        func_info = self.env.lookup_function(func_name)
        if not func_info or func_info["kind"] != "function":
            self.increase_error_count()
            return

        param_types = func_info["param_types"]
        if len(args) != len(param_types):
            self.increase_error_count()
            return

        for arg, expected_type in zip(args, param_types):
            if type(arg) != type(expected_type):
                self.increase_error_count()

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

        for arg in node.args:
            if isinstance(arg, IdentifierExpr):
                try:
                    info = self.env.lookup(arg.name)
                    info["borrowed"] = False
                except Exception:
                    self.increase_error_count()

    def visit_FieldAccessExpr(self, node):
        base_type = self.visit(node.receiver)

        if not isinstance(base_type, StructType):
            self.increase_error_count()
            return None

        struct_name = base_type.name
        struct_info = self.env.lookup_struct(struct_name)

        if struct_info is None:
            self.increase_error_count()
            return None

        field_type = struct_info.get(node.field)
        if field_type is None:
            self.increase_error_count()
            return None

        if isinstance(node.base, IdentifierExpr):
            try:
                var_info = self.env.lookup(node.base.name)
            except Exception:
                self.increase_error_count()
                return None

            if not var_info["owned"] or var_info["borrowed"]:
                self.increase_error_count()

        return field_type

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