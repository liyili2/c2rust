from ast import FunctionDef
from types import NoneType
from RustParser.AST_Scripts.ast.Block import Block
from RustParser.AST_Scripts.ast.Type import ArrayType, BoolType, FloatType, IntType, PointerType, RefType, StringType, StructType, VoidType
from RustParser.AST_Scripts.ast.TypeEnv import TypeEnv
from RustParser.AST_Scripts.ast.Expression import BinaryExpr, BorrowExpr, CastExpr, FunctionCallExpr, IdentifierExpr, IntLiteral, LiteralExpr, RangeExpression 

class TypeChecker:
    def __init__(self):
        self.env = TypeEnv()
        self.symbol_table = {}
        self.error_count = 0
        self.errors = []
        self.reports = []

    def error(self, node, message):
        error_msg = f"Type error: {message}"
        if hasattr(node, 'line'):
            error_msg = f"[Line {node.line}] {error_msg}"
        print(error_msg)
        self.errors.append(error_msg)
        self.error_count = self.error_count + 1

    def report(self, node, message):
        self.reports.append((node, message))

    def increase_error_count(self):
        self.error_count = self.error_count + 1
    
    def is_type_compatible(self, expected, actual):
        return expected == actual

    def generic_visit(self, node):
        raise NotImplementedError(f"No visit_{type(node).__name__} method defined.")
    
    def visit_StructField(self, node):
        if isinstance(node.type, PointerType):
            self.error(node, "raw pointer usage in a struct field")
        # print("visit_StructField", node.name, node.type)
    
    def visit_TopLevelVarDef(Self, node):
        pass

    def visit_InterfaceDef(self, node):
        pass

    def visit_Attribute(self, node):
        pass

    def visit_StructDef(self, node):
        for field in node.fields:
            fiels_type = self.visit(field)
        #TODO
        pass

    def visit_TypeFullPathExpression(self, node):
        pass

    def visit_StructLiteral(self, node):
        pass

    def visit_FunctionDef(self, node: FunctionDef):
        print("visit_function_def", self.error_count)

        fn_name = node.identifier
        param_types = [param.typ for param in node.params]
        return_type = node.return_type or VoidType()

        if self.env.top().get(fn_name) is None:
            self.env.top()[fn_name] = {
                "kind": "function",
                "param_types": param_types,
                "return_type": return_type
            }
        else:
            self.error(node, f"redefinition of function '{fn_name}'")

        self.env.enter_scope()
        for i, param in enumerate(node.params):
            param_name = param.name
            param_type = param.typ
            is_mut = param.is_mut

            if i == 0 and param_name == "self":
                if not self.in_method_context():
                    self.error(param, "`self` used outside of method context")

                if not isinstance(param_type, RefType):
                    self.error(param, f"`self` must be a reference type, found: {param_type}")

                if is_mut and not getattr(param_type, "mutable", False):
                    self.error(param, "`self` is marked mutable, but its type is not a mutable reference")

            if param_name in self.env.top():
                self.error(param, f"duplicate parameter name '{param_name}'")

            self.env.top()[param_name] = {
                "type": param_type,
                "mutable": is_mut,
                "owned": True,
                "borrowed": False
            }

        saved_return = getattr(self, "current_function_return", None)
        self.current_function_return = return_type

        for stmt in node.body.getChildren():
            self.visit(stmt)

        if not isinstance(return_type, VoidType) and not self.body_has_terminating_return(node.body):
            self.error(node, f"missing return in function '{fn_name}'")

        self.current_function_return = saved_return
        self.env.exit_scope()

        # print("visit_function_def2", self.error_count)
        return None

    def body_has_terminating_return(self, stmts):
        pass
        # for s in reversed(stmts):
        #     if isinstance(s, ReturnStmt):
        #         return True
        #     if isinstance(s, IfStmt):
        #         return (self.body_has_terminating_return(s.then_body) and
        #                 self.body_has_terminating_return(s.else_body or []))
        #     if isinstance(s, WhileStmt):
        #         continue
        # return False

    def resolve_function_return_type(self, node):
        func_name = node.func
        func_info = self.env.lookup_function(func_name)
        if func_info["kind"] != "function":
            self.error(node, "wrong function return type")
        return func_info["return_type"]

    def get_literal_type(self, value):
        if isinstance(value, int):
            return IntType()
        elif isinstance(value, str):
            return StringType()
        elif isinstance(value, bool):
            return BoolType()
        else:
            self.error(self, "unknown literal type")

    def visit_Type(self, ctx):
        print("visit_Type")
        type_str = ctx.getText()
        if type_str == "i32":
            return IntType()
        elif ctx.getText() == "bool":
            return BoolType()
        elif type_str == "String":
            return StringType()
        else:
            self.error(self, "unknown primitive type")

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
            self.visit(item)

    def visit_WhileStmt(self, node):
        cond_type = self.visit(node.condition)
        if not isinstance(cond_type, BoolType):
            self.error(node, "wrong while condition type")

        for stmt in node.body:
            self.visit(stmt)

    def visit_CastExpr(self, node: CastExpr):
        expr_type = self.visit(node.expr)
        target_type = self.visit(node.type)
        if expr_type == target_type:
            return target_type

        valid_numeric_types = (IntType, FloatType)
        if isinstance(expr_type, valid_numeric_types) and isinstance(target_type, valid_numeric_types):
            return target_type

        # self.increase_error_count()
        return target_type
    
    def visit_StructLiteral(self, node):
        struct_type = self.visit(node.type_name)
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
        expr_types = [self.visit(expr) for expr in node.values]

        if node.is_destructuring():
            if len(node.var_defs) != len(expr_types):
                self.error(node, "number of group-let of values and targets do not match")
                return

            for var_def, expr_type in zip(node.var_defs, expr_types):
                declared_type = self.visit(var_def.type) if var_def.type else expr_type

                if var_def.type and type(declared_type) != type(expr_type) and not isinstance(expr_type, RefType):
                    self.error(node, "in the group-let, type of one of the values do not match its target")

                self.env.declare(var_def.name, declared_type)
                self.symbol_table[var_def.name] = declared_type
                self._handle_borrowing(var_def, node.values[0])

        else:
            var_def = node.var_defs[0]
            expr_type = expr_types[0]
            # print(var_def.type.__class__, expr_type.__class__, (var_def.type.__class__ is expr_type.__class__))
            if var_def.type:
                declared_type = self.visit(var_def.type)
            else:
                declared_type = expr_type

            if isinstance(var_def.type, NoneType):
                var_def.type = expr_type

            if isinstance(expr_type, NoneType):
                expr_type = var_def.type

            if not (var_def.type.__class__ is expr_type.__class__):
                # print(var_def.type.__class__, expr_type.__class__)
                self.error(node, "type of the value and target do not match")

            self.env.declare(var_def.name, declared_type, mutable=var_def.mutable)
            self.symbol_table[var_def.name] = declared_type

            self._handle_borrowing(var_def, node.values[0])

    def visit_BinaryExpr(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        op = node.op

        # print("visit_BinaryExpr", right.__class__, left.__class__)
        if op in ['+', '-', '*', '/', '>>', '<<']:
            if isinstance(left, IntType) and isinstance(right, IntType):
                return IntType()
            else:
                self.error(node, "binary expression target and value type mismatch #1")
                return IntType()

        elif op in ['==', '!=', '<', '>', '<=', '>=']:
            if type(left) == type(right):
                return BoolType()
            else:
                self.error(node, "binary expression target and value type mismatch #2")
                return BoolType()

        elif op in ['&&', '||']:
            if isinstance(left, BoolType) and isinstance(right, BoolType):
                return BoolType()
            else:
                self.error(node, "binary expression target and value type mismatch #3")
                return BoolType()
            
        elif op in ['&']:
            if isinstance(left, IntType) and isinstance(right, IntType):
                return IntType()
            else:
                self.error(node, "binary expression target and value type mismatch #3")
                return IntType()
        else:
            self.error(node, f"Unknown binary operator: {op}")
            return IntType()

    def visit_Block(self, node):
        result_stmts = []
        if isinstance(node.stmts, Block):
            self.visit(node.stmts)
        if node.isUnsafe:
            self.error(node, "unsafe blcok error")
        for stmt in node.stmts:
            result_stmt = self.visit(stmt)
            result_stmts.append(result_stmt)

    def visit_UnsafeExpression(self, node):
        self.error(node, "unsafe expression error")

    def visit_ExternBlock(self, node):
        pass

    def visit_TypeAliasDecl(self, node):
        pass

    def visit_CompoundAssignment(self, node):
        target_type = self.visit(node.target)
        value_type = self.visit(node.value)

        # Check mutability
        if isinstance(node.target, IdentifierExpr):
            try:
                target_info = self.env.lookup(node.target.name)
                print(";;", target_info)
            except Exception:
                self.error(node, "usage of undefined variable in compound assignment")
                return

            if not target_info.get("mutable", False):
                self.error(node, "assignment target must be mutable in compound assignment")

            if target_info.get("borrowed", False):
                self.error(node, "usage of not borrowed variable in compound assignment")

        # Type compatibility check for compound ops
        if node.op in ['+=', '-=', '*=', '/=']:
            if not (isinstance(target_type, IntType) and isinstance(value_type, IntType)):
                self.error(node, "ops not compatible in compound assignment")

        else:
            self.error(node, f"Unknown compound operator: {node.op}")

    def _handle_borrowing(self, var_def, value_expr):
        if isinstance(value_expr, IdentifierExpr):
            try:
                value_info = self.env.lookup(value_expr.name)
            except Exception:
                self.increase_error_count()
                return

            if value_info:
                if value_info["borrowed"]:
                    self.increase_error_count()
                if not value_info["owned"]:
                    self.increase_error_count()
                value_info["owned"] = False

        elif isinstance(value_expr, BorrowExpr):
            try:
                value_info = self.env.lookup(value_expr.name)
            except Exception:
                self.increase_error_count()
                return

            if value_info:
                if value_expr.mutable and not value_info["mutable"]:
                    self.increase_error_count()
                if value_info["borrowed"]:
                    self.increase_error_count()
                value_info["borrowed"] = True

    def visit_Assignment(self, node):
        visited_target = self.visit(node.target)
        expr_type = self.visit(node.value)

        try:
            info = self.env.lookup(node.target)
        except Exception:
            self.increase_error_count()
            return

        if not info["owned"]:
            self.increase_error_count()
        if info["borrowed"]:
            self.increase_error_count()

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

        self.symbol_table[node.target] = { "type": expr_type,
        "owned": True, "borrowed": False, "mutable": info["mutable"]}
        return True

    def visit_IfStmt(self, node):
        condition_type = self.visit(node.condition)

        if not isinstance(condition_type, BoolType):
            self.error(node, "if condition type is not a boolean")

        self.visit(node.then_branch)

        if node.else_branch:
            for stmt in node.else_branch.getChildren():
                self.visit(stmt)
        return True

    def visit_ForStmt(self, node):
        iterable_type = self.visit(node.iterable)

        if not isinstance(node.iterable, ArrayType) and not isinstance(node.iterable, RangeExpression):
            self.error(node, "wrong iterative type")
            return

        range_type = None
        if isinstance(node.iterable, ArrayType):
            range_type = iterable_type.var_type
        else:
            range_type = node.iterable.initial.__class__
        self.env.define(node.var, {
            "type": range_type,
            "owned": True, "borrowed": False})

        for stmt in node.body.getChildren():
            self.visit(stmt)

        return True

    def visit_RangeExpression(self, node):
        # print("visit_RangeExpression", node.initial, node.last)
        return RangeExpression(node.initial, node.last)

    def visit_ReturnStmt(self, node):
        if node.value is None:
            return_type = "unit"
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
        # print("visit_IntType")
        return IntType()

    def visit_BoolType(self, node):
        return BoolType()

    def visit_ArrayType(self, node: ArrayType):
        elem_type = self.visit(node.var_type)

        if node.size is not None:
            size_type = self.visit(node.size)

            if (not self.is_compile_time_constant(node.size)) and (not isinstance(size_type, IntType)):
                self.error(node.size, "array size must be an integer")

        return ArrayType(elem_type, size=node.size)

    def is_compile_time_constant(self, node):
        if isinstance(node, IntLiteral) or isinstance(node, int):
            return True
        if isinstance(node, BinaryExpr):
            return self.is_compile_time_constant(node.left) and self.is_compile_time_constant(node.right)
        return False

    def visit_MatchPattern(self, node):
        pattern_type = self.visit(node.value)
        if pattern_type not in ["i32", "bool", "char", "String", "enum_variant"]:
            self.error(f"Unsupported match pattern type: {pattern_type}")

        return pattern_type

    def visit_LiteralExpr(self, node):
        print("visit_LiteralExpr")
        if isinstance(node.value, int):
            return IntType()

        if isinstance(node.value, str):
            return StringType()
        
        if isinstance(node.value, bool):
            return BoolType()
        else:
            self.increase_error_count()

    def visit_IdentifierExpr(self, node):
        info = None
        try:
            info = self.env.lookup(node.name)
        except Exception:
            self.error(node, "identifier "+ node.name +" not defined")
            return

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
        pass

    def visit_callExpressionPostFix(self, node, func_expr):
        # if not hasattr(node, 'args'):
        #     self.increase_error_count()
        #     return

        # args = self.visit(node.args) if hasattr(node, 'args') else []
        # if isinstance(func_expr, IdentifierExpr):
        #     func_name = func_expr.name
        # else:
        #     self.increase_error_count()
        #     return

        # func_info = self.env.lookup_function(func_name)
        # if not func_info or func_info["kind"] != "function":
        #     self.increase_error_count()
        #     return

        # param_types = func_info["param_types"]
        # if len(args) != len(param_types):
        #     self.increase_error_count()
        #     return

        # for arg, expected_type in zip(args, param_types):
        #     if type(arg) != type(expected_type):
        #         self.increase_error_count()

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
        print("visit_FieldAccessExpr", base_type, node.receiver.name, node.name)

        if not isinstance(base_type, StructType):
            self.error(node, "access to a wrong type of variable (not a struct)")
            return None

        struct_name = base_type.name
        struct_info = self.env.lookup_struct(struct_name)

        if struct_info is None:
            self.error(node, "access to an undefined struct")
            return None

        field_type = struct_info.get(node.field)
        if field_type is None:
            self.error(node, "no such a field to access")
            return None

        if isinstance(node.base, IdentifierExpr):
            try:
                var_info = self.env.lookup(node.base.name)
            except Exception:
                self.error(node, "no such a identifier to access")
                return None

            if not var_info["owned"] or var_info["borrowed"]:
                self.error(node, "the identifier is not owned or borrowed")

        return field_type

    def visit_MatchStmt(self, node):
        self.visit(node.expr)
        for arm in node.arms:
            self.visit(arm.body)

    def visit_TypePathExpression(self, node):
        self.error(node, "type path expression instead of simple types")

    def visit_BoolLiteral(self, node):
        return BoolType()

    def visit_IntLiteral(self, node):
        # print("visit_IntLiteral")
        return IntType()

    def visit_StrLiteral(self, node):
        return StringType()

    def visit_CallExpression(self, node):
        pass
        # return FunctionCallExpr(func=node.func, args=node.args)

    def visit_PrimaryExpression(self, node):
        pass

    def visit_typeWrapper(self, node):
        pass

    def visit_UseDecl(self, node):
        pass

    def visit_StaticVarDecl(self, node):
        pass