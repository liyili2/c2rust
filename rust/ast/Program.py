from rust.ast.ASTNode import ASTNode
from rust.ast.MarkedASTNode import MarkedASTNode

class Program(ASTNode):
    def __init__(self, items):
        super().__init__()
        self.items = items
        self.marked_nodes = []

    def accept(self, visitor):
        return visitor.visitProgram(self)

    def getChildren(self):
        return self.items

    def add_marked(self, node: MarkedASTNode):
        self.marked_nodes.append(node)

    def get_random_marked(self):
        import random
        if not self.marked_nodes:
            return None
        return random.choice(self.marked_nodes)
    
    def list_marked_nodes(self):
        return [marked.node for marked in self.marked_nodes]

    def list_marked_nodes_with_ids(self):
        return [(marked.get_id(), marked.node) for marked in self.marked_nodes]