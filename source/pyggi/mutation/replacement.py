
from RustParser.AST_Scripts.ast.Program import Program
from RustParser.AST_Scripts.ast.TopLevel import FunctionDef, TopLevel, StaticVarDecl
from RustParser.AST_Scripts.ast.Func import FunctionParamList, Param
from RustParser.AST_Scripts.ast.Block import Block
from RustParser.AST_Scripts.ast.Statement import LetStmt
from RustParser.AST_Scripts.ast.VarDef import VarDef
from RustParser.AST_Scripts.ast.Type import PointerType, SafeNonNullWrapper
from pyggi.mutation.utils import MutationUtils
import random

class ReplacementOperator:
    def __init__(self, ast, node):
        self.utils = MutationUtils()
        self.new_ast = self.apply_mutation(ast, node)

    def get_new_ast(self):
        return self.new_ast

    def apply_mutation(self, ast, node):
        new_ast = self.safe_wrap_raw_pointers(ast, node)
        new_ast = self.safe_wrap_raw_pointer_argumetns(ast, node)
        new_ast = self.make_global_static_pointers_unmutable(ast, node)
        # new_ast = self.move_ast_node(ast, node)
        return new_ast

    def shuffle_and_update_block(self, node, block):
        random.shuffle(block.getChildren())
        new_block = Block(block.getChildren(), block.isUnsafe)
        node.setBody(new_block)

    def replace_raw_pointer_defs_with_safe_wrappers(eslf, node, block):
        new_stmts = []
        for stmt in block.getChildren():
            if isinstance(stmt, LetStmt):
                if len(stmt.var_defs) == 1:
                    if isinstance(stmt.var_defs[0].type, PointerType) and stmt.var_defs[0].mutable:
                        new_stmt = LetStmt(values=stmt.values[0],
                            var_defs=[
                                VarDef(var_type=SafeNonNullWrapper(typeExpr=stmt.var_defs[0].type), 
                                    name=stmt.var_defs[0].name, mutable=stmt.var_defs[0].mutable)
                            ]
                        )
                        new_stmts.append(new_stmt)
            else:
                new_stmts.append(stmt)

        new_block = Block(new_stmts, block.isUnsafe)
        node.setBody(new_block)

    def safe_wrap_raw_pointers(self, ast_root, target_node):
        return self.utils.transform_ast(ast_root, target_node, self.replace_raw_pointer_defs_with_safe_wrappers)

    def move_ast_node(self, ast_root, target_node):
        return self.utils.transform_ast(ast_root, target_node, self.shuffle_and_update_block)

    def make_global_static_pointers_unmutable(self, ast_root, target_node):
        # print("make_global_static_pointers_unmutable")
        if isinstance(target_node, TopLevel):
            top_items = []
            for top in ast_root.getChildren():
                if isinstance(top, StaticVarDecl):
                    new_top_item = StaticVarDecl(var_type=top.var_type, mutable=False, name= top.name,
                                                initial_value=top.initial_value, visibility=top.visibility)
                    top_items.append(new_top_item)
                else:
                    top_items.append(top)

            return Program(items=top_items)

    # check param list parent
    def safe_wrap_raw_pointer_argumetns(self, ast_root, target_node):
        parents = self.utils.get_all_parents(ast_root, target_node)
        if not isinstance(ast_root, Program):
            return None

        if not isinstance(target_node, FunctionParamList):
            return ast_root

        remaining_tops = []
        new_params = []

        parent_1 = parents[-2]
        for top in ast_root.getChildren():
            if isinstance(parent_1, type(top)) and isinstance(parent_1, FunctionDef):
                if self.utils.function_def_eq(parent_1, top):
                    for param in parent_1.params.params:
                        if isinstance(param.typ, PointerType) and param.mutable:
                            new_param = Param(name=param.name, typ=SafeNonNullWrapper(
                                typeExpr=param.typ
                            ), mutable=param.mutable)

                            new_params.append(new_param)
                        else:
                            new_params.append(param)
                    parent_1.setParamList(new_params)
                    remaining_tops.append(parent_1)
            else:
                remaining_tops.append(top)

        return Program(items=remaining_tops)