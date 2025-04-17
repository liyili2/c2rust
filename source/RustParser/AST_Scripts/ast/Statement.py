from ASTNode import ASTNode

class Statement(ASTNode):
    pass

class LetStmt(Statement):
    def __init__(self, name, declared_type, value):
        self.name = name
        self.declared_type = declared_type
        self.value = value

    def accept(self, visitor):
        return visitor.visit_LetStmt(self)

class AssignStmt(Statement):
    def __init__(self, target, value):
        self.target = target
        self.value = value

    def accept(self, visitor):
        return visitor.visit_assign_stmt(self)

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
