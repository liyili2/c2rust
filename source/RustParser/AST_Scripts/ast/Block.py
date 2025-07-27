from RustParser.AST_Scripts.ast.ASTNode import ASTNode

class InitBlock(ASTNode):
    def __init__(self, attrList, returnExpr):
        super().__init__()
        self.attrList = attrList
        self.returnExpr = returnExpr

    def accept(self, visitor):
        return visitor.visitInitBlock(self)

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