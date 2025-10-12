from RustParser.AST_Scripts.ast.ASTNode import ASTNode

class Block(ASTNode):
    def __init__(self, stmts, isUnsafe):
        self.stmts = stmts
        self.isUnsafe = isUnsafe

    def setBody(self, stmts):
        self.stmts = stmts

    def accept(self, visitor):
        return visitor.visit_Block(self)

    def getChildren(self):
        return self.stmts
    
    def remove(self, stmt):
        self.stmts.remove(stmt)