from RustParser.AST_Scripts.ast.ASTNode import ASTNode

class Statement(ASTNode):
    pass

class InitBlock(ASTNode):
    def __init__(self, attrList, returnExpr):
        self.attrList = attrList
        self.returnExpr = returnExpr

    def accept(self, visitor):
        return visitor.visitInitBlock(self)
