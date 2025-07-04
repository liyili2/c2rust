from RustParser.AST_Scripts.ast.ASTNode import ASTNode

class Program(ASTNode):
    def __init__(self, items):
        super().__init__()
        self.items = items  # A list of FunctionDef, StructDef, etc.

    def accept(self, visitor):
        return visitor.visit_Program(self)
    
    def getChildren(self):
        return self.items
