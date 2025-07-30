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
        # parents = self.utils.get_all_parents(ast_root, target_node)
        # if not isinstance(ast_root, Program):
        #     return None

        # print("inserting!")
        # remaining_tops = []
        # parent_len = len(parents)

        # for top in ast_root.getChildren():
        #     if parent_len < 3:
        #         remaining_tops.append(top)
        #         continue

        #     parent_1, parent_2 = parents[-2], parents[-3]
        #     top_type_matches = isinstance(parent_1, type(top))
        #     if isinstance(top, list):
        #         top_children = top
        #     else:
        #         top_children = top.getChildren()

        #     if not top_type_matches:
        #         remaining_tops.append(top)
        #         continue

        #     if isinstance(parent_2, type(top_children)):
        #         new_stmts = []
        #         if isinstance(top_children, Block):
        #             for stmt in top_children.getChildren():
        #                 if self.utils.statements_eq(stmt, target_node):
        #                     if len(stmt.var_defs) == 1:
        #                         new_let_stmt = LetStmt(var_defs=VarDef(name=stmt.var_defs[0].name,
        #                             mutable= not stmt.var_defs[0].mutable,
        #                             by_ref=stmt.var_defs[0].by_ref,
        #                             var_type=stmt.var_defs[0].type), values=stmt.values[0])
        #                         new_stmts.append(new_let_stmt)
        #                 else:
        #                     new_stmts.append(stmt)
        #             top_children.setBody(new_stmts)
        #             top.setBody(top_children)

        #         elif isinstance(top_children, FunctionDef) and isinstance(top_children.body, Block):
        #             for stmt in top_children.body.getChildren():
        #                 if self.utils.statements_eq(stmt, target_node):
        #                     if len(stmt.var_defs) == 1:
        #                         new_let_stmt = LetStmt(var_defs=VarDef(name=stmt.var_defs[0].name, 
        #                             mutable= not stmt.var_defs[0].mutable,
        #                             by_ref=stmt.var_defs[0].by_ref,
        #                             var_type=stmt.var_defs[0].type), values=stmt.values[0])
        #                         new_stmts.append(new_let_stmt)
        #                 else:
        #                     new_stmts.append(stmt)
        #             top_children.body.setBody(new_stmts)
        #             top.setBody(top_children)
        #         remaining_tops.append(top)
        
        # print("flipped tree:", pretty_print_ast(Program(items=remaining_tops)))
        # return Program(items=remaining_tops)