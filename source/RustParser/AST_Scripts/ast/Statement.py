from RustParser.AST_Scripts.ast.ASTNode import ASTNode

class Statement(ASTNode):
    pass

class LetStmt(Statement):
    def __init__(self, var_def, value):
        self.value = value
        self.declared_type = var_def.type
        self.name = var_def.name
        self.mutable = var_def.mutable

    def accept(self, visitor):
        return visitor.visit_LetStmt(self)

class ForStmt:
    def __init__(self, var, iterable, body):
        self.var = var
        self.iterable = iterable
        self.body = body

    def accept(self, visitor):
        return visitor.visit_ForStmt(self)

class IfStmt:
    def __init__(self, condition, then_branch, else_branch=None):
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch
    def accept(self, visitor):
        return visitor.visit_IfStmt(self)

class AssignStmt(Statement):
    def __init__(self, target, value):
        self.target = target
        self.value = value

    def __str__(self):
        return f"{self.target} = {self.value}"

    def accept(self, visitor):
        return visitor.visit_Assignment(self)

class ReturnStmt(Statement):
    def __init__(self, value):
        self.value = value

    def accept(self, visitor):
        return visitor.visit_return_stmt(self)

class Block(Statement):
    def __init__(self, statements):
        self.statements = statements

    def accept(self, visitor):
        return visitor.visit_block(self)

class ExternStaticVarDecl(Statement):
    def __init__(self, name, var_type, mutable, initial_value, visibility=None):
        self.name = name                  # str
        self.var_type = var_type          # Type or str
        self.mutable = mutable            # bool
        self.initial_value = initial_value  # Expr
        self.visibility = visibility      # Optional[str]

    def __repr__(self):
        return f"ExternStaticVarDecl(name={self.name}, type={self.var_type}, mutable={self.mutable}, visibility={self.visibility}, init={self.initial_value})"
