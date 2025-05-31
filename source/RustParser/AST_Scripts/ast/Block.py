from RustParser.AST_Scripts.ast.ASTNode import ASTNode

class InitBlock(ASTNode):
    def __init__(self, attrList, returnExpr):
        super().__init__()
        self.attrList = attrList
        self.returnExpr = returnExpr

    def accept(self, visitor):
        return visitor.visitInitBlock(self)
