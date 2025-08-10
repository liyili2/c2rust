import random
from pyggi.mutation.utils import MutationUtils
from RustParser.AST_Scripts.ast.Program import Program

class InsertionOperator:
    def __init__(self, ast, node):
        self.utils = MutationUtils()
        self.operators = [
            self.insert_return_stmt,
        ]
        self.new_ast = self.apply_random_mutations(ast, node, 1)

    def apply_random_mutations(self, ast, node, num_ops):
        selected_ops = random.sample(self.operators, k=num_ops)
        for op in selected_ops:
            ast = op(ast, node)
        return ast

    def get_new_ast(self):
        return self.new_ast
    
    def insert_return_stmt(self, ast_root, target_node):
        pass
