from RustParser.AST_Scripts.ast.ASTNode import ASTNode

class Statement(ASTNode):
    pass

class LetStmt(Statement):
    def __init__(self, var_def, value):
        super().__init__()
        self.value = value
        self.declared_type = var_def.type
        self.name = var_def.name
        self.mutable = var_def.mutable

    def accept(self, visitor):
        return visitor.visit_LetStmt(self)

class StaticVarDecl:
    def __init__(self, name, var_type, mutable, initial_value, visibility=None):
        super().__init__()
        self.name = name                  # str: variable name
        self.var_type = var_type          # str or Type: declared type
        self.mutable = mutable            # bool: true if `mut` is present
        self.initial_value = initial_value  # Expr: value assigned at declaration
        self.visibility = visibility      # str or None: 'pub', 'pub(crate)', etc.

    def __repr__(self):
        return (
            f"StaticVarDecl(name={self.name}, "
            f"type={self.var_type}, "
            f"mutable={self.mutable}, "
            f"visibility={self.visibility}, "
            f"initial_value={self.initial_value})")

class ForStmt:
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

class Block(Statement):
    def __init__(self, statements):
        super().__init__()
        self.statements = statements

    def accept(self, visitor):
        return visitor.visit_block(self)

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

class WhileStmt(Statement):
    def __init__(self, condition, body, line=None, column=None):
        super().__init__()
        self.condition = condition
        self.body = body
        # self.line = line
        # self.column = column

    def accept(self, visitor):
        return visitor.visitWhileStmt(self)

class MatchStmt(Statement):
    def __init__(self, expr, arms, line, column):
        super().__init__()
        self.expr = expr              # the expression being matched
        self.arms = arms              # list of MatchArm
        # self.line = line
        # self.column = column

    def accept(self, visitor):
        return visitor.visit_match_stmt(self)

class MatchArm(Statement):
    def __init__(self, patterns, body):
        super().__init__()
        self.patterns = patterns
        self.body = body

class MatchPattern(Statement):
    def __init__(self, value):
        super().__init__()
        self.value = value

class CompoundAssignment(Statement):
    def __init__(self, target, op, value, line, column):
        super().__init__()
        self.target = target
        self.op = op
        self.value = value
        # self.line = line
        # self.column = column

    def accept(self, visitor):
        return visitor.visitCompoundAssignment(self)

class ExpressionStmt(Statement):
    def __init__(self, expr, line, column):
        super().__init__()
        self.expr = expr
        # self.line = line
        # self.column = column

    def accept(self, visitor):
        return visitor.visitExpressionStmt(self)

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
        return visitor.visitLoopStmt(self)

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

class StructLiteral(Statement):
    def __init__(self, type_name: str, fields: list):
        super().__init__()
        self.type_name = type_name
        self.fields = fields

    def accept(self, visitor):
        return visitor.visit_StructLiteral(self)

    def __repr__(self):
        return f"StructLiteral(type_name={self.type_name}, fields={self.fields})"

class CallStmt(Statement):
    def __init__(self, callee, args):
        super().__init__()
        self.callee = callee  # Could be an IdentifierExpr or a MethodCallExpr
        self.args = args      # List of expressions

    def accept(self, visitor):
        return visitor.visit_CallStmt(self)

class UnsafeBlock(Statement):
    def __init__(self, block):
        super().__init__()
        self.block = block

    def accept(self, visitor):
        return visitor.visit_UnsafeBlock(self)