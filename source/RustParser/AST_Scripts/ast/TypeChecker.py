from ast import FunctionDef
from types import NoneType
from RustParser.AST_Scripts.ast.Block import *
from RustParser.AST_Scripts.ast.Type import *
from RustParser.AST_Scripts.ast.TypeEnv import *
from RustParser.AST_Scripts.ast.Expression import *
from RustParser.AST_Scripts.ast.Expression import FunctionCall as FunctionCallExpr
from RustParser.AST_Scripts.ast.Statement import *
from RustParser.AST_Scripts.ast.TopLevel import *
from RustParser.AST_Scripts.ast.utils import *

class TypeChecker:
    def __init__(self):
        self.env = TypeEnv()
        self.symbol_table = {}
        self.error_count = 0
        self.errors = []
        self.reports = []
        self.root = None

    def error(self, node, message, error_weight=1):
        # error_weight=1
        error_msg = f"Type error: {message}"
        if hasattr(node, 'line'):
            error_msg = f"[Line {node.line}] {error_msg}"
        print(error_msg)
        self.errors.append(error_msg)
        self.error_count = self.error_count + (error_weight)

    def report(self, node, message):
        self.reports.append((node, message))

    def increase_error_count(self):
        self.error_count = self.error_count + 1

    def is_type_compatible(self, expected, actual):
        return expected == actual

    def generic_visit(self, node):
        raise NotImplementedError(f"No visit_{type(node).__name__} method defined.")

    def visit_StructField(self, node):
        if isinstance(node.declarationInfo.type, PointerType):
            self.error(node, "raw pointer usage in a struct field")

    def visit_TopLevelVarDef(self, node):
        if node.def_kind:
            isUnion = str.__eq__(node.def_kind, "union")
            self.env.declare(name=node.declarationInfo.name, 
                            typ=StructType(name=node.declarationInfo.name, fields=node.fields, isUnion=isUnion))

    def visit_Expression(self, node):
        return self.visit(node.expr)

    def visit_InterfaceDef(self, node):
        for item in node.functions:
            self.visit(item)

    def visit_Attribute(self, node):
        pass

    def visit_SafeWrapper(self, node):
        pass

    def visit_FunctionDef(self, node: FunctionDef):
        if node.isUnsafe:
            self.error(node, "unsafe function definition", error_weight=len(node.body.stmts)/10)

        fn_name = node.identifier
        param_types = [param.declarationInfo.type for param in node.params]
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
            param_name = param.declarationInfo.name
            param_type = self.visit(param.declarationInfo.type)
            is_mut = param.isMutable
            self.visit(param)

            if i == 0 and param_name == "self":
                if not isinstance(param_type, RefType) and param_type is not None:
                    self.error(param, f"`self` must be a reference type, found: {param_type}")

                if is_mut and not getattr(param_type, "mutable", False):
                    self.error(param, "`self` is marked mutable, but its type is not a mutable reference")
                if is_mut and isinstance (param.declarationInfo.type, PointerType):
                    self.error(node, f"raw pointer passed as argument to function {node.name}")

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

        # if not isinstance(return_type, VoidType) and not self.body_has_terminating_return(node.body.getChildren()):
        #     self.error(node, f"missing return in function '{fn_name}'")

        self.current_function_return = saved_return
        self.env.exit_scope()

        return None

    def body_has_terminating_return(self, stmts):
        for s in reversed(stmts):
            if isinstance(s, ReturnStmt):
                return True
            if isinstance(s, IfStmt):
                then_has = self.body_has_terminating_return(s.then_branch.getChildren())
                # else_branch = s.else_branch.getChildren() if s.else_branch is not None else []
                # else_has = self.body_has_terminating_return(else_branch)
                return then_has
            if isinstance(s, WhileStmt):
                continue
        return False

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
        if not isinstance(ctx, str):
            type_str = ctx.getText()
        else:
            type_str = ctx
        if type_str == "i32":
            return IntType()
        elif type_str == "bool":
            return BoolType()
        elif type_str == "String":
            return StringType()
        else:
            pass
            # self.error(self, "unknown primitive type")

    def visit(self, node):
        if self.root is None:
            self.root = node
        # if node is None:
        #     self.error(node, "none node found")
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
        # self.visit(node.condition)
        self.visit(node.body)

    def visit_CastExpr(self, node: CastExpr):
        if isinstance(node.expr, DereferenceExpr):
            self.error(node, "raw pointer dereference in a cast expression")
        expr_type = self.visit(node.expr)
        target_type = self.visit(node.type)
        if expr_type == target_type:
            return target_type

        valid_numeric_types = (IntType, FloatType)
        if isinstance(expr_type, valid_numeric_types) and isinstance(target_type, valid_numeric_types):
            return target_type

        return target_type

    def visit_Struct(self, node):
        if isinstance(node, TopLevel):
            self.visit_StructDef(node)
        if isinstance(node, Statement):
            self.visit_StructLiteral(node)
        else:
            return None

    def visit_StructDef(self, node):
        field_dict = {}
        for field in node.fields:
            field_type = self.visit(field)
            field_name = field.declarationInfo.name
            field_dict[field_name] = field_type

        self.env.declare(name=node.name, typ=StructType(name=node.name, fields=field_dict))

    def visit_StructLiteral(self, node):
        struct_type = self.visit(node.type_name)
        info = self.env.lookup(struct_type)
        if not isinstance(info['type'], StructType):
            self.error(node, f"{struct_type} is not a valid struct type")
            return

        field_types = info['type'].fields
        used_fields = set()
        for field in node.fields:
            field_name = field.name
            if field_name not in field_types:
                # self.error(field, f"Field '{field_name}' is not defined in struct")
                continue

            expected_type = field_types[field_name]
            actual_type = self.visit(field.value)
            if not self.is_type_compatible(expected_type, actual_type) and expected_type is not None:
                pass
                # self.error(field, f"Type mismatch for field '{field_name}': expected {expected_type}, got {actual_type}")
            used_fields.add(field_name)

        missing_fields = set(field_types) - used_fields
        # if missing_fields:
        #     for mf in missing_fields:
        #         self.error(node, f"Missing field '{mf}' in struct literal of type '{struct_type}'")
        return

    def visit_StructLiteralField(self, node):
        pass

    def visit_LetStmt(self, node):
        expr_types = []
        for expr in node.values:
            expr_types.append(self.visit(expr))

        if node.is_destructuring():
            if len(node.var_defs) != len(expr_types):
                self.error(node, "number of group-let of values and targets do not match")
                return

            for var_def, expr_type in zip(node.var_defs, expr_types):
                declared_type = self.visit(var_def.declarationInfo.type) if var_def.declarationInfo.type else expr_type

                if var_def.declarationInfo.type and type(declared_type) != type(expr_type) and not isinstance(expr_type, RefType):
                    self.error(node, "in the group-let, type of one of the values do not match its target")

                self.env.declare(var_def.declarationInfo.name, declared_type)
                self.symbol_table[var_def.declarationInfo.name] = declared_type
                self._handle_borrowing(var_def, node.values[0])

        else:
            var_def = node.var_defs[0]
            expr_type = self.visit(expr_types[0])

            if isinstance(var_def.declarationInfo.type, str):
                var_def_type = self.visit_Type(var_def.declarationInfo.type)
            else:
                var_def_type = self.visit(var_def.declarationInfo.type)

            if var_def_type is None:
                var_def_type = expr_type

            if isinstance(var_def_type, NoneType):
                var_def_type = expr_type
            self.detect_raw_pointer_definition(var_def.declarationInfo.name, var_def.declarationInfo.type, var_def.isMutable)

            if isinstance(expr_type, NoneType):
                expr_type = var_def_type

            if (
                node.values[0] is not None and
                not isinstance(expr_type, var_def_type.__class__) and
                not isinstance(var_def_type, SafeNonNullWrapper) and
                not node.values[0].isUnsafe == True
            ):
                self.error(node, f"type of the value and target do not match: {(var_def_type.__class__)} and {(expr_type.__class__)}")

            self.env.declare(var_def.declarationInfo.name, var_def_type, mutable=var_def.isMutable)
            self.symbol_table[var_def.declarationInfo.name] = var_def_type
            self._handle_borrowing(var_def, node.values[0])

    def detect_raw_pointer_definition(self, name, type, isMutable):
        if isinstance(type, PointerType) and isMutable:
            self.error(self, f"raw pointer definition: {name} = *mut {type.accept(self)}")

    def visit_PointerType(self, node):
        return self.visit(node.pointee_type)

    def visit_DereferenceExpr(self, node):
        self.error(node, f"unsafe pointer dereferencing {node.expr.name}", 2)
        return self.visit(node.expr)

    def visit_SafeNonNullWrapper(self, node):
        return node

    def visit_ByteLiteralExpr(self, node):
        return node
    
    def visit_ArrayAccess(self, node):
        return node
    
    def visit_TopLevelVarDef(self, node):
        return node
    
    def visit_BreakStmt(self, node):
        pass

    def visit_ContinueStmt(self, node):
        pass

    def visit_BinaryExpr(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        op = node.op

        if isinstance(node.left, PointerType) or isinstance(node.left, DereferenceExpr):
            self.error(node, "usage of raw pointers in a binary expression's left operand")
        if isinstance(node.right, PointerType) or isinstance(node.right, DereferenceExpr):
            self.error(node, "usage of raw pointers in a binary expression's right operand")

        # print("visit_BinaryExpr", node.op, node.left, node.right)
        if isinstance(node.left, FunctionCallExpr) or isinstance(node.right, FunctionCallExpr):
            return

        if op in ['+', '-', '*', '/', '>>', '<<']:
            if isinstance(left, IntType) and isinstance(right, IntType):
                return IntType()
            else:
                # self.error(node, f"binary expression target and value type mismatch #1: {left} {op} {right}")
                return IntType()

        elif op in ['==', '!=', '<', '>', '<=', '>=']:
            if type(left) == type(right) or isinstance(right, NoneType) or isinstance(left, NoneType):
                return BoolType()
            else:
                # self.error(node, f"binary expression target and value type mismatch #2: {left} {op} {right}")
                return BoolType()

        elif op in ['&&', '||']:
            if isinstance(left, BoolType) and isinstance(right, BoolType):
                return BoolType()
            else:
                # self.error(node, f"binary expression target and value type mismatch #3: {left} {op} {right}")
                return BoolType()
            
        elif op in ['&']:
            if isinstance(left, IntType) and isinstance(right, IntType):
                return IntType()
            else:
                # self.error(node, "binary expression target and value type mismatch #3")
                return IntType()
        else:
            self.error(node, f"Unknown binary operator: {op}")
            return IntType()

    def visit_Block(self, node):
        result_stmts = []
        if isinstance(node.stmts, Block):
            self.visit(node.stmts)
        if node.isUnsafe:
            self.error(node, "unsafe blcok observed", error_weight=len(node.stmts)/10)
        for stmt in node.stmts:
            result_stmt = self.visit(stmt)
            result_stmts.append(result_stmt)

    def visit_ExternBlock(self, node):
        pass

    def visit_TypeAliasDecl(self, node):
        pass

    def visit_CompoundAssignment(self, node):
        target_type = self.visit(node.target)
        value_type = self.visit(node.value)
        target_name = self.get_expr_identifier(node.target)
        try:
            target_type = self.env.lookup(target_name)["type"]
        except Exception:
            return
            # self.error(node, "undefined variable in compound assignment")

        # Check mutability
        if isinstance(node.target, IdentifierExpr):
            try:
                target_info = self.env.lookup(node.target.name)
            except Exception:
                # self.error(node, "usage of undefined variable in compound assignment")
                return

            if not target_info.get("mutable", False):
                self.error(node, "assignment target must be mutable in compound assignment")

            if target_info.get("borrowed", False):
                self.error(node, "usage of not borrowed variable in compound assignment")

            if target_info.get("owned", False):
                self.error(node, "usage of not owned variable in compound assignment", 2)

        # Type compatibility check for compound ops
        if node.op in ['+=', '-=', '*=', '/=']:
            if (not isinstance(target_type, IntType)) or (not isinstance(value_type, IntType)):
                pass
                # self.error(node, "ops not compatible in compound assignment")
        else:
            self.error(node, f"Unknown compound operator: {node.op}")

    def _handle_borrowing(self, var_def, value_expr):
        if isinstance(value_expr, IdentifierExpr):
            try:
                value_info = self.env.lookup(value_expr.name)
            except Exception:
                # self.error(self, f"undefined variable: {value_expr.name}")
                return

            if value_info:
                if value_info["borrowed"]:
                    self.error(self, f"usage of a borrowed variable {value_expr.name}")
                if not value_info["owned"]:
                    self.error(self, f"usage of a variable which ownership was moved: {value_expr.name}", 2)
                value_info["owned"] = False

        elif isinstance(value_expr, BorrowExpr):
            try:
                value_info = self.env.lookup(value_expr.name)
            except Exception:
                # self.error(self, f"undefined variable: {value_expr.name}")
                return

            if value_info:
                if value_expr.isMutable and not value_info["mutable"]:
                    self.error(self, f"cannot mutably borrow an immutable variable in a let stmt: {value_expr.name}")
                if value_info["borrowed"]:
                    self.error(self, f"usage of a borrowed variable {value_expr.name}")
                value_info["borrowed"] = True

    def get_expr_identifier(self,expr):
        if isinstance(expr, IdentifierExpr):
            return expr.name
        elif isinstance(expr, DereferenceExpr):
            return self.get_expr_identifier(expr.expr)
        elif isinstance(expr, FieldAccessExpr):
            receiver = expr.receiver
            return self.get_expr_identifier(receiver)
        elif isinstance(expr, Expression):
            return self.get_expr_identifier(expr.expr)

    def visit_Assignment(self, node):
        try:
            if self.get_expr_identifier(node.target) is not None:
                info = self.env.lookup(self.get_expr_identifier(node.target))
                if info is None:
                    return
            else:
                return
        except Exception:
            # self.error(node, f"undefined variable {self.get_expr_identifier(node.target)} in assignment {self.get_expr_identifier(node.target)} = {self.get_expr_identifier(node.value)}")
            return

        if not info["owned"]:
            self.error(node, f"assigning to a not-owned variable in {self.get_expr_identifier(node.target)} = {self.get_expr_identifier(node.value)}")
        if info["borrowed"]:
            self.error(node, f"assigning to a borrowed variable {self.get_expr_identifier(node.target)} = {self.get_expr_identifier(node.value)}")

        target_type = self.visit(node.target)

        value_type = self.visit(node.value)
        if type(info["type"]) != type(value_type) and not isinstance(node.value, FunctionCallExpr) and not isinstance(node.target, FieldAccessExpr) and type(value_type) != NoneType:
            if info["type"] != value_type:
                pass
                # self.error(node, f"type mismatch in assignemnt {self.get_expr_identifier(node.target)} = {self.get_expr_identifier(node.value)}")

        if isinstance(node.value, IdentifierExpr):
            try:
                value_info = self.env.lookup(node.value.name)
            except Exception:
                # self.error(node, f"undefined variable in assignment value : {self.get_expr_identifier(node.target)} = {self.get_expr_identifier(node.value)}")
                value_info = None

            #TODO: Check it better
            if ( value_type is IntType) or ( value_type is BoolType) or ( value_type is CharType):
                if value_info:
                    if not value_info["owned"]:
                        self.error(node, f"assigning a not-owned variable to target : {self.get_expr_identifier(node.target)} = {self.get_expr_identifier(node.value)}", 2)
                    value_info["owned"] = False

        if isinstance(node.value, BorrowExpr):
            try:
                value_info = self.env.lookup(node.value.name)
            except Exception:
                # self.error(node.value, f"usage of undeclared variable")
                value_info = None

            if value_info:
                # if node.value.mutable and not value_info["mutable"]:
                #     self.increase_error_count()
                # if value_info["borrowed"]:
                #     self.increase_error_count()
                # value_info["borrowed"] = True

                self.symbol_table[node.target] = { "type": value_info['type'],
                "owned": True, "borrowed": False, "mutable": info["mutable"]}
        return

    def visit_LoopStmt(self, node):
        self.visit(node.body)

    def visit_UnaryExpr(self, node):
        pass

    def visit_IfStmt(self, node):
        self.visit(node.condition)
        self.visit(node.then_branch)
        if node.else_branch is not None:
            self.visit(node.else_branch)
        return

    def check_iterable_type(self, node):
        return True

    def visit_ForStmt(self, node):
        for stmt in node.body.getChildren():
            self.visit(stmt)
        return True

    def visit_RangeExpression(self, node):
        return RangeExpression(node.initial, node.last)

    def visit_ReturnStmt(self, node):
        if node.value is None:
            return_type = "unit"
        else:
            return_type = self.visit(node.value)
        return return_type

    def visit_FunctionCall(self, node):
        if isinstance(node, Expression):
            func_info = self.env.lookup_function(node.callee)
            if not func_info or func_info["kind"] != "function":
                # self.error(node.func, f"calling an undefined function")
                return None

            for arg in node.args:
                if isinstance(arg, IdentifierExpr):
                    try:
                        info = self.env.lookup(arg.name)
                    except Exception:
                        # self.error(arg.name, f"undefined arg in {node.func}")
                        continue
            for arg in node.args:
                if isinstance(arg, IdentifierExpr):
                    try:
                        info = self.env.lookup(arg.name)
                    except Exception:
                        # self.error(arg.name, f"undefined arg in {node.func}")
                        continue

                    if not info["owned"] or info["borrowed"]:
                        self.error(arg.name, f"no owners found for the argument {arg.name} in {node.callee}")
                    if not info["owned"] or info["borrowed"]:
                        self.error(arg.name, f"no owners found for the argument {arg.name} in {node.callee}")

                    info["borrowed"] = True
                    info["borrowed"] = True

            arg_types = [self.visit(arg) for arg in node.args]
            expected_types = func_info["param_types"]
            arg_types = [self.visit(arg) for arg in node.args]
            expected_types = func_info["param_types"]

            if len(arg_types) != len(expected_types):
                self.error(node.callee, f"wrong number of arguments")
            else:
                for actual, expected in zip(arg_types, expected_types):
                    if type(actual) != type(expected):
                        self.error(node.callee, f"wrong number of arguments")

            for arg in node.args:
                if isinstance(arg, IdentifierExpr):
                    info = self.env.lookup(arg.name)
                    info["borrowed"] = False
                    info["owned"] = False

            return func_info["return_type"]

    def visit_VarDef(self, ctx):
        name = ctx.name
        typ = self.visit(ctx.var_type)
        return (name, typ)

    def visit_ParamNode(self, node):
        name = node.declarationInfo.name
        if isinstance(node.declarationInfo.type, PointerType) and(node.isMutable or node.declarationInfo.type.isMutable):
            self.error(node, "raw pointer usage in the function signature")
        isMutable = node.isMutable 
        self.env.declare(name, node.declarationInfo.type, isMutable)
        return (name, node.declarationInfo.type, isMutable)

    def visit_FunctionParamList(self, ctx):
        params = []
        for param_ctx in ctx.params:
            name, typ, mutable = self.visit(param_ctx)
            params.append((name, typ, mutable))
        return params

    def visit_IntType(self, node):
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
        if isinstance(node.expr, int):
            return IntType()
        if isinstance(node.expr, str):
            return StringType()
        if isinstance(node.expr, bool):
            return BoolType()
        if isinstance(node.expr, NoneType):
            return NoneType()
        else:
            self.error(node, f"unknown literal type for {node.expr}")

    def visit_IdentifierExpr(self, node):
        info = None
        try:
            info = self.env.lookup(node.name)
        except Exception:
            # self.error(node, "identifier "+ node.name +" not defined")
            return

        return info["type"]

    def visit_QualifiedExpression(self, node):
        inner_type = self.visit(node.expr)
        return inner_type

    def visit_BorrowExpr(self, node):
        info = self.env.lookup(self.get_expr_identifier(node.expr))
        if not info["owned"]:
            self.error(node, "cannot borrow a variable which ownership already moved")

        if node.isMutable:
            if not info["mutable"]:
                self.error(node, "cannot mutably borrow an immutable variable")
            if info["borrowed"]:
                self.error(node, "cannot mutably borrow a variable that's already borrowed", 2)
        else:
            if info["borrowed"]:
                self.error(node, "cannot immutably borrow a variable that's already borrowed", 2)

        if not isinstance(node, FieldAccessExpr):
            info["borrowed"] = True
        return RefType(info["type"])

    def visit_PatternExpr(self, node):
        pass
    
    def visit_FunctionCallExpression(self, node):
        pass

    def visit_ArrayLiteral(self, node):
        if not node.elements:
            return None
        elem_types = [self.visit(elem) for elem in node.elements]

        first_type = elem_types[0]
        for t in elem_types[1:]:
            if type(t) != type(first_type):
                pass
                # self.error(node, "wrong element type in the array literal", 1)

        return ArrayType(first_type)

    def visit_callExpressionPostFix(self, node, func_expr):
        for arg in node.args:
            if isinstance(arg, IdentifierExpr):
                try:
                    info = self.env.lookup(arg.name)
                except Exception:
                    # self.error(node, f"undefined argument {arg.name}")
                    continue
                if not info["owned"] or info["borrowed"]:
                    self.error(node, f"no owners found for the argument {arg.name}")
                info["borrowed"] = True

        for arg in node.args:
            if isinstance(arg, IdentifierExpr):
                try:
                    info = self.env.lookup(arg.name)
                    info["borrowed"] = False
                except Exception:
                    # self.error(node, f"undefined argument {arg.name}")
                    continue

    def visit_FieldAccessExpr(self, node):
        base_type = self.visit(node.receiver)
        field_type = self.visit(node.name)
        field = node.name.name

        if isinstance(node.receiver, FunctionCall):
            base_type = self.visit(node.receiver.callee)
            try:
                base_info = self.env.lookup(base_type)
                base_type = base_info["type"]
            except Exception:
                self.error(node, f"access to an undefined struct {node.receiver}")
                return

        if isinstance(node.receiver, DereferenceExpr):
            self.error(node, "unprotected dereference in a field access expression")
            base_type = self.visit(node.receiver.expr)
            try:
                base_info = self.env.lookup(base_type)
                base_type = base_info["type"]
            except Exception:
                self.error(node, f"access to an undefined struct {node.receiver}")
                return

        # parent_list = get_all_parents(target_node=node, ast_root=self.root, parent=None)
        # check_done = False
        # for p in parent_list:
        #     if isinstance(p, InterfaceDef):
        #         info = self.env.lookup(p.name)
        #         if isinstance(info["type"], StructType):
        #             for f in info["type"].fields:
        #                 if str.__eq__(field, f):
        #                     check_done = True

        # if not check_done:
        #     if not( isinstance(base_type, StructType) or isinstance(base_type, StructDef)):
        #         # self.error(node, "access to a wrong type of variable (not a struct)")
        #         return

        #     if isinstance(base_type, StructType) and base_type.isUnion:
        #         self.error(node, f"union struct {base_type.name} field {node.name.name} access ")

        #     for field in base_info["type"].fields:
        #         if isinstance(field, str):
        #             if str.__eq__(field, node.name.name):
        #                 field_type = field.__class__
        #                 break
        #         else:
        #             if str.__eq__(field.declarationInfo.name, node.name.name):
        #                 field_type = field.declarationInfo.type
        #                 break
        #     if field_type is None:
        #         self.error(node, "no such a field to access")
        #         return None

        return field_type

    def visit_MatchStmt(self, node):
        self.visit(node.expr)
        for arm in node.arms:
            self.visit(arm.body)

    def visit_Statement(self, node):
        return self.visit(node.body)

    def visit_ConditionalAssignmentStmt(self, node):
        return self.visit(node.body)

    def visit_TypePathExpression(self, node):
        if isinstance(node.last_type, IdentifierExpr):
            return node.last_type
        if isinstance(node.last_type, FunctionCall):
            return node.last_type.callee
        if str.__contains__(node.last_type, "int"):
            return IntType()
        if str.__contains__(node.last_type, "str"):
            return StringType()
        if str.__contains__(node.last_type, "char"):
            return CharType()
        if str.__contains__(node.last_type, "bool"):
            return BoolType()
        # self.error(node, "type path expression instead of primitive types")

    def visit_BoolLiteral(self, node):
        return BoolType()

    def visit_IntLiteral(self, node):
        return IntType()

    def visit_StrLiteral(self, node):
        return StringType()

    def visit_PrimaryExpression(self, node):
        pass

    def visit_typeWrapper(self, node):
        pass

    def visit_UseDecl(self, node):
        pass

    def visit_CharLiteral(self, node):
        pass

    def visit_StaticVarDecl(self, node):
        node_type = self.visit(node.declarationInfo.type)
        self.env.declare(name=node.declarationInfo.name, typ=node_type, mutable=node.isMutable)
        if node.isMutable and isinstance(node, TopLevel):
            self.error(node, f"global static mutable struct declaration: {node.declarationInfo.name}")