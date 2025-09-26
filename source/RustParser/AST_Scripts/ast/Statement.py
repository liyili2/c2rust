from RustParser.AST_Scripts.ast.ASTNode import ASTNode

class Statement(ASTNode):
    def __init__(self, body=None):
        super().__init__()
        self.body = body

    def accept(self, visitor):
        method_name = f'visit_{self.__class__.__name__}'
        return getattr(visitor, method_name, visitor.generic_visit)(self)

class LetStmt(Statement):
    def __init__(self, var_defs, values):
        super().__init__()
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
        return visitor.visitLetStmt(self)

class ForStmt(Statement):
    def __init__(self, var, iterable, body):
        super().__init__()
        self.var = var
        self.iterable = iterable
        self.body = body

    def accept(self, visitor):
        return visitor.visitForStmt(self)

class IfStmt(Statement):
    def __init__(self, condition, then_branch, else_branch=None):
        super().__init__()
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch
    def accept(self, visitor):
        return visitor.visitIfStmt(self)

class AssignStmt(Statement):
    def __init__(self, target, value):
        super().__init__()
        self.target = target
        self.value = value

    def __str__(self):
        return f"{self.target} = {self.value}"

    def accept(self, visitor):
        return visitor.visit_Assignment(self)

class ConditionalAssignmentStmt(Statement):
    def __init__(self, cond, body):
        super().__init__()
        self.body = body # assignment stmt
        self.condition = cond

    def accept(self, visitor):
        return super().accept(visitor)

class WhileStmt(Statement):
    def __init__(self, condition, body):
        super().__init__()
        self.condition = condition
        self.body = body

    def accept(self, visitor):
        return visitor.visitWhileStmt(self)

class MatchStmt(Statement):
    def __init__(self, expr, arms):
        super().__init__()
        self.expr = expr
        self.arms = arms

    def accept(self, visitor):
        return visitor.visitMatchStmt(self)

class MatchArm(Statement):
    def __init__(self, patterns, body):
        super().__init__()
        self.patterns = patterns
        self.body = body

    def accept(self, visitor):
        return visitor.visit(self)

class MatchPattern(Statement):
    def __init__(self, value):
        super().__init__()
        self.value = value

    def accept(self, visitor):
        return visitor.visitMatchPattern()

class CompoundAssignment(Statement):
    def __init__(self, target, op, value):
        super().__init__()
        self.target = target
        self.op = op
        self.value = value

    def accept(self, visitor):
        return visitor.visitCompoundAssignment(self)

class ReturnStmt(Statement):
    def __init__(self, value=None):
        super().__init__()
        self.value = value

    def accept(self, visitor):
        return visitor.visitReturnStmt(self)
    
    def __repr__(self):
        return f"ReturnStmt(value={self.value})"

class LoopStmt(Statement):
    def __init__(self, body):
        super().__init__()
        self.body = body

    def accept(self, visitor):
        return visitor.visitLoopStmt(self)

    def __repr__(self):
        return f"LoopStmt(body={repr(self.body)})"

class BreakStmt(Statement):
    def __init__(self):
        super().__init__()

    def accept(self, visitor):
        return visitor.visit(self)

class ContinueStmt(Statement):
    def __init__(self):
        super().__init__()
    def accept(self, visitor):
        return visitor.visit(self)

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

class Block(Statement):
    def __init__(self, stmts, isUnsafe=False):
        super().__init__()
        self.stmts = stmts
        self.isUnsafe = isUnsafe

    def accept(self, visitor):
        return visitor.visit_Block(self)
    
    def getChildren(self):
        return self.stmts

class TypeWrapper(Statement):
    def __init__(self, expr):
        super().__init__()
        self.expr = expr

    def accept(self, visitor):
        return visitor.visit_typeWrapper(self)