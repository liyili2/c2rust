from RustParser.AST_Scripts.ast.ASTNode import ASTNode

class Statement(ASTNode):
    pass

class LetStmt(Statement):
    def __init__(self, var_defs, values):
        super().__init__()
        # print("llllll", values, var_defs)
        self.var_defs = var_defs if isinstance(var_defs, list) else [var_defs]
        self.values = values if isinstance(values, list) else [values]

    def is_destructuring(self):
        return len(self.var_defs) > 1

    def __repr__(self):
        if self.is_destructuring():
            vars_str = ", ".join(v.name for v in self.var_defs)
            vals_str = ", ".join(str(v) for v in self.values)
            return f"LetStmt(({vars_str}) = ({vals_str}))"
        else:
            var = self.var_defs[0]
            val = self.values[0]
            return f"LetStmt({var.name} = {val})"

    def accept(self, visitor):
        return visitor.visit_LetStmt(self)

class ForStmt(Statement):
    def __init__(self, var, iterable, body):
        super().__init__()
        self.var = var
        self.iterable = iterable
        self.body = body

    def accept(self, visitor):
        return visitor.visit_ForStmt(self)

class IfStmt(Statement):
    def __init__(self, condition, then_branch, else_branch=None):
        super().__init__()
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch
    def accept(self, visitor):
        return visitor.visit_IfStmt(self)

class AssignStmt(Statement):
    def __init__(self, target, value):
        super().__init__()
        self.target = target
        self.value = value

    def __str__(self):
        return f"{self.target} = {self.value}"

    def accept(self, visitor):
        return visitor.visit_Assignment(self)

class ReturnStmt(Statement):
    def __init__(self, value):
        super().__init__()
        self.value = value

    def accept(self, visitor):
        return visitor.visit_return_stmt(self)

class ExternStaticVarDecl(Statement):
    def __init__(self, name, var_type, mutable, initial_value, visibility=None):
        super().__init__()
        self.name = name
        self.var_type = var_type
        self.mutable = mutable
        self.initial_value = initial_value
        self.visibility = visibility

    def __repr__(self):
        return f"ExternStaticVarDecl(name={self.name}, type={self.var_type}, mutable={self.mutable}, visibility={self.visibility}, init={self.initial_value})"

    def accept(self, visitor):
        pass

class WhileStmt(Statement):
    def __init__(self, condition, body, line=None, column=None):
        super().__init__()
        self.condition = condition
        self.body = body
        # self.line = line
        # self.column = column

    def accept(self, visitor):
        return visitor.visit_WhileStmt(self)

class MatchStmt(Statement):
    def __init__(self, expr, arms, line, column):
        super().__init__()
        self.expr = expr
        self.arms = arms
        # self.line = line
        # self.column = column

    def accept(self, visitor):
        return visitor.visit_MatchStmt(self)

class MatchArm(Statement):
    def __init__(self, patterns, body):
        super().__init__()
        self.patterns = patterns
        self.body = body

    def accept(self, visitor):
        return super().accept(visitor)

class MatchPattern(Statement):
    def __init__(self, value):
        super().__init__()
        self.value = value

    def accept(self, visitor):
        return visitor.visit_MatchPattern()

class CompoundAssignment(Statement):
    def __init__(self, target, op, value, line, column):
        super().__init__()
        self.target = target
        self.op = op
        self.value = value
        # self.line = line
        # self.column = column

    def accept(self, visitor):
        return visitor.visit_CompoundAssignment(self)

class ExpressionStmt(Statement):
    def __init__(self, expr, line=None, column=None):
        super().__init__()
        self.expr = expr
        # self.line = line
        # self.column = column

    def accept(self, visitor):
        return visitor.visit_ExpressionStmt(self)

class ReturnStmt(Statement):
    def __init__(self, value=None):
        super().__init__()
        self.value = value

    def accept(self, visitor):
        return visitor.visit_ReturnStmt(self)
    
    def __repr__(self):
        return f"ReturnStmt(value={self.value})"

class LoopStmt(Statement):
    def __init__(self, body):
        super().__init__()
        self.body = body

    def accept(self, visitor):
        return visitor.visit_LoopStmt(self)

    def __repr__(self):
        return f"LoopStmt(body={repr(self.body)})"
    
class BreakStmt(Statement):
    def __init__(self):
        super().__init__()

    def accept(self, visitor):
        return self

class ContinueStmt(Statement):
    def __init__(self):
        super().__init__()
    def accept(self, visitor):
        return self

class StructDef(Statement):
    def __init__(self, type_name: str, fields: list):
        super().__init__()
        self.type_name = type_name
        self.fields = fields

    def accept(self, visitor):
        return visitor.visit_Struct(self)

    def __repr__(self):
        return f"StructDef(type_name={self.type_name}, fields={self.fields})"

class FunctionCall(Statement):
    def __init__(self, callee, args, caller=None):
        super().__init__()
        self.callee = callee
        self.args = args
        self.caller = caller

    def accept(self, visitor):
        return visitor.visit_FunctionCall(self)

class UnsafeBlock(Statement):
    def __init__(self, stmts):
        super().__init__()
        self.stmts = stmts

    def accept(self, visitor):
        return visitor.visit_UnsafeBlock(self)
    
    def getChildren(self):
        return self.stmts

class TypeWrapper(Statement):
    def __init__(self, expr):
        super().__init__()
        self.expr = expr

    def accept(self, visitor):
        return visitor.visit_typeWrapper(self)

class ConditionalAssignmentStmt(Statement):
    def __init__(self, cond, assignment):
        super().__init__()
        self.assignment = assignment
        self.condition = cond

    def accept(self, visitor):
        return super().accept(visitor)
