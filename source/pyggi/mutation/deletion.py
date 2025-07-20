
from RustParser.AST_Scripts.ast.Program import Program
from RustParser.AST_Scripts.ast.TopLevel import FunctionDef
from RustParser.AST_Scripts.ast.Block import Block
from pyggi.mutation.utils import MutationUtils

class DeletionOperator:
    def __init__(self, ast, node):
        self.ast = ast
        self.node = node
        self.utils = MutationUtils()
        self.new_ast = self.remove_ast_node(self.ast, self.node)

    def get_new_ast(self):
        return self.new_ast

    def remove_ast_node(self, ast_root, target_node):
        parents = self.utils.get_all_parents(ast_root, target_node)
        print("target node is ", target_node, target_node.parent, parents, len(parents))
        new_ast = self.remove_node(ast_root, target_node, parents)
        return new_ast

    def remove_node(self, ast_root, target_node, parents):
        current = ast_root
        i = len(parents) - 1
        other_tops = []
        new_ast = None
        if isinstance(current, Program):
            current_list = current.getChildren()
            for top in current_list:
                if isinstance(parents[i - 1], type(top)):
                    top_children = top.getChildren()
                    if isinstance(parents[i - 2] ,type(top_children)):
                        if isinstance(top_children, Block):
                            top_children_stmts = top_children.getChildren()
                            self.utils.remake_ast_after_removal(target_node, other_tops, top, top_children, top_children_stmts)
                        elif isinstance(top_children, FunctionDef):
                            if isinstance(top_children.body, Block):
                                top_children_stmts = top_children.getChildren()
                                self.utils.remake_ast_after_removal(target_node, other_tops, top, top_children, top_children_stmts)
                else:
                    other_tops.append(top)
                    continue

        new_ast = Program(items=other_tops)
        return new_ast
