
from RustParser.AST_Scripts.tests.TransformerTest import pretty_print_ast
from RustParser.AST_Scripts.ast.Program import Program
from RustParser.AST_Scripts.ast.TopLevel import FunctionDef, InterfaceDef, StructDef, StructField, TopLevel, StaticVarDecl
from RustParser.AST_Scripts.ast.Func import FunctionParamList, Param
from RustParser.AST_Scripts.ast.Block import Block
from RustParser.AST_Scripts.ast.Statement import LetStmt, UnsafeBlock
from RustParser.AST_Scripts.ast.VarDef import VarDef
from RustParser.AST_Scripts.ast.Type import PointerType, RefType, SafeNonNullWrapper, VoidType
from pyggi.mutation.utils import MutationUtils
import random

from RustParser.AST_Scripts.ast.Expression import DereferenceExpr, ReferenceExpr, UnsafeExpression

class ReplacementOperator:
    def __init__(self, ast, node):
        self.utils = MutationUtils()
        self.operators = [
            self.safe_wrap_raw_pointers,
            self.safe_wrap_raw_pointer_argumetns,
            self.make_global_static_pointers_unmutable,
            self.move_ast_node,
            self.shrink_unsafe_block_stmts,
            self.flip_mutabilities,
            self.safe_wrap_struct_field,
            self.replace_raw_dereferences_in_unsafe_wrapper,
        ]
        self.new_ast = self.apply_random_mutations(ast, node, 6)

    def apply_random_mutations(self, ast, node, num_ops):
        selected_ops = random.sample(self.operators, k=num_ops)
        for op in selected_ops:
            # print("applied operation: ", selected_ops, selected_ops.__class__)
            ast = op(ast, node)
        return ast

    def get_new_ast(self):
        return self.new_ast

    def transform_let_stmt(self, ast_root, target_node, transform_fn, label="transform"):
        parents = self.utils.get_all_parents(ast_root, target_node)
        if not isinstance(ast_root, Program):
            return None
        if not isinstance(target_node, LetStmt):
            return ast_root

        print(f"{label}!")
        remaining_tops = []
        parent_len = len(parents)

        for top in ast_root.getChildren():
            if parent_len < 3:
                remaining_tops.append(top)
                continue

            parent_1, parent_2 = parents[-2], parents[-3]
            top_type_matches = isinstance(parent_1, type(top))
            if not isinstance(top, FunctionDef) or not isinstance(top, InterfaceDef):
                continue
            top_children = top if isinstance(top, list) else top.getChildren()

            if not top_type_matches:
                remaining_tops.append(top)
                continue

            if isinstance(parent_2, type(top_children)):
                new_stmts = []

                block = top_children.body if isinstance(top_children, FunctionDef) else top_children
                if isinstance(block, Block):
                    for stmt in block.getChildren():
                        if self.utils.statements_eq(stmt, target_node):
                            new_stmt = transform_fn(stmt)
                            new_stmts.append(new_stmt if new_stmt else stmt)
                        else:
                            new_stmts.append(stmt)

                    block.setBody(new_stmts)
                    if isinstance(top_children, FunctionDef):
                        top_children.body = block
                    else:
                        top.setBody(block)

                top.setBody(top_children)
            remaining_tops.append(top)

        print(f"{label} result:", pretty_print_ast(Program(items=remaining_tops)))
        return Program(items=remaining_tops)
    
    def replace_raw_dereferences_in_unsafe_wrapper(self, ast_root, target_node):
        def transform(stmt):
            if isinstance(stmt, LetStmt) and len(stmt.var_defs) == 1:
                val = stmt.values[0]
                if isinstance(val, DereferenceExpr):
                    return LetStmt(
                        var_defs=VarDef(
                            name=stmt.var_defs[0].name,
                            mutable=stmt.var_defs[0].mutable,
                            by_ref=stmt.var_defs[0].by_ref,
                            var_type=RefType("T")
                        ),
                        values=UnsafeExpression(expr=ReferenceExpr(expr=val))
                    )
            return None  # No change
        return self.transform_let_stmt(ast_root, target_node, transform, label="replace_raw_dereferences_in_unsafe_wrapper")

    def flip_mutabilities(self, ast_root, target_node):
        def transform(stmt):
            if isinstance(stmt, LetStmt) and len(stmt.var_defs) == 1:
                return LetStmt(
                    var_defs=VarDef(
                        name=stmt.var_defs[0].name,
                        mutable=not stmt.var_defs[0].mutable,
                        by_ref=stmt.var_defs[0].by_ref,
                        var_type=stmt.var_defs[0].type
                    ),
                    values=stmt.values[0]
                )
            return None
        return self.transform_let_stmt(ast_root, target_node, transform, label="flip_mutabilities")

    def safe_wrap_struct_field(self, ast_root, target_node):
        if not isinstance(ast_root, Program):
            return None
        remaining_tops = []
        for top in ast_root.getChildren():
            new_fields = []
            if isinstance(top, StructDef):
                for field in top.getChildren():
                    if isinstance(field.type, PointerType) and field.type.mutability:
                        new_field = StructField(name=field.name, typeExpr=SafeNonNullWrapper(
                            typeExpr=field.type), visibility=field.visibility)
                        new_fields.append(new_field)
                    else:
                        new_fields.append(field)
                top.setChildren(new_fields)

            elif isinstance(top, FunctionDef) and isinstance(top.body, Block):
                new_Stmts = []
                for stmt in top.body.getChildren():
                    if isinstance(stmt, StructDef):
                        for field in stmt.getChildren():
                            if isinstance(field.type, PointerType) and field.type.mutability:
                                new_field = StructField(name=field.name, typeExpr=SafeNonNullWrapper(
                                    typeExpr=field.type), visibility=field.visibility)
                                new_fields.append(new_field)
                            else:
                                new_fields.append(field)
                        new_struct_def = StructDef(name=stmt.name, fields=new_fields)
                        new_Stmts.append(new_struct_def)
                    else:
                        new_Stmts.append(stmt)
                new_block = Block(stmts=new_Stmts, isUnsafe=top.body.isUnsafe)
                top.setBody(new_block)
            remaining_tops.append(top)

        # print("safe struct:", pretty_print_ast(Program(items=remaining_tops)))
        return Program(items=remaining_tops)

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
        if not isinstance(target_node, Block):
            return ast_root
        return self.utils.transform_ast(ast_root, target_node, self.shuffle_and_update_block)

    def make_global_static_pointers_unmutable(self, ast_root, target_node):
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

    def shrink_unsafe_block_stmts(self, ast_root, target_node):
        if not isinstance(target_node, UnsafeBlock):
            return ast_root

        remaining_tops = []
        for top in ast_root.getChildren():
            if isinstance(top, FunctionDef):
                top_block = top.body
                for stmt in top_block.getChildren():
                    remaining_block_stmts = []
                    if isinstance(stmt, UnsafeBlock):
                        if self.utils.blocks_eq(stmt, target_node):
                            stmts = stmt.getChildren()
                            if len(stmts) == 0:
                                remaining_stmts = []
                                out_stmts = []
                            else:
                                slice_point = random.randint(0, len(stmts) - 1)
                                remaining_stmts = stmts[:slice_point]
                                out_stmts = stmts[slice_point:]
                            unsafe_block = UnsafeBlock(stmts=remaining_stmts)
                            remaining_block_stmts.append(unsafe_block)
                            remaining_block_stmts.append(out_stmts)
                            remaining_tops.append(top)
                    else:
                        remaining_block_stmts.append(stmt)

                parent_block = Block(stmts=remaining_block_stmts, isUnsafe=False)
                top.setBody(parent_block)
            else:
                remaining_tops.append(top)

        return Program(items=remaining_tops)