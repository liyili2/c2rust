import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from rust.ast.ASTNode import ASTNode, CloneableASTNode
from rust.ast.Expression import Expression
from rust.ast.MarkedASTNode import MarkedASTNode

class MarkingVisitor:
    def __init__(self, program):
        self.program = program

    def mark(self, node: ASTNode) -> ASTNode:
        """Recursively visit and wrap Expression nodes."""
        # First, recurse into children (even if already wrapped)
        self._visit_children(node)
        
        # If this node is an Expression, wrap it
        if isinstance(node, Expression):
            marked = MarkedASTNode(node)
            self.program.add_marked(marked)
            return marked
        return node

    def _visit_children(self, node: ASTNode):
        for attr_name in list(node.__dict__.keys()):
            if attr_name == 'parent':
                continue

            attr = getattr(node, attr_name)
            print(f"  {type(node).__name__}.{attr_name} = {type(attr).__name__}")  # debug

            if isinstance(attr, CloneableASTNode):
                # print(f"    -> CloneableASTNode, marking...")
                setattr(node, attr_name, self.mark(attr))

            elif isinstance(attr, (list, tuple)):
                # print(f"    -> list/tuple, iterating...")
                new_list = []
                for item in attr:
                    if isinstance(item, CloneableASTNode):
                        new_list.append(self.mark(item))
                    else:
                        new_list.append(item)
                setattr(node, attr_name, new_list)

            elif isinstance(attr, dict):
                # print(f"    -> dict, iterating...")
                new_dict = {}
                for k, v in attr.items():
                    if isinstance(v, CloneableASTNode):
                        new_dict[k] = self.mark(v)
                    else:
                        new_dict[k] = v
                setattr(node, attr_name, new_dict)

            # else:
            #     print(f"    -> skipped (not CloneableASTNode, list, or dict)")

    def run(self):
        """Start marking from the program's items."""
        new_items = []
        for item in self.program.items:
            new_items.append(self.mark(item))
        self.program.items = new_items
        return self.program