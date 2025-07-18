from RustParser.AST_Scripts.ast.Func import FunctionParamList, Param
from copy import deepcopy
import os
from RustParser.AST_Scripts.ast.AstPrinter import AstPrinter
from RustParser.AST_Scripts.ast.Block import Block
from RustParser.AST_Scripts.antlr.RustLexer import RustLexer
from antlr4 import CommonTokenStream, InputStream
from RustParser.AST_Scripts.antlr.RustParser import RustParser
from RustParser.AST_Scripts.ast.Transformer import Transformer, setParents
from RustParser.AST_Scripts.ast.Program import Program
from RustParser.AST_Scripts.ast.Expression import BinaryExpr, BoolLiteral, CastExpr, Expression, FieldAccessExpr, IdentifierExpr, IntLiteral, MethodCallExpr, StrLiteral, TypePathExpression, UnsafeExpression
from RustParser.AST_Scripts.ast.Statement import AssignStmt, CallStmt, ForStmt, IfStmt, LetStmt, Statement, WhileStmt
from RustParser.AST_Scripts.ast.TopLevel import Attribute, ExternBlock, ExternFunctionDecl, FunctionDef, InterfaceDef, StaticVarDecl, StructDef, TopLevel, TopLevelVarDef, TypeAliasDecl
from RustParser.AST_Scripts.ast.TypeChecker import TypeChecker
from RustParser.AST_Scripts.ast.Type import PointerType, RefType, SafeNonNullWrapper
from RustParser.AST_Scripts.ast.VarDef import VarDef
from pyggi.tree.rust_unparser import RustUnparser
from pyggi.tree.abstract_engine import AbstractTreeEngine
from typing import List, Tuple
import random

def pretty_print_ast(node, indent=0, visited=None):
    if visited is None:
        visited = set()

    lines = []
    prefix = ' ' * indent

    if isinstance(node, (str, int, float, bool, type(None))):
        return f"{prefix}{repr(node)}"

    node_id = id(node)
    if node_id in visited:
        return f"{prefix}<Cycle: {type(node).__name__}>"

    visited.add(node_id)

    if isinstance(node, list):
        for n in node:
            lines.append(pretty_print_ast(n, indent, visited))
    elif hasattr(node, '__dict__'):
        lines.append(f"{prefix}{type(node).__name__}:")
        for attr, value in vars(node).items():
            if attr == "parent":
                continue
            lines.append(f"{prefix}  {attr}:")
            lines.append(pretty_print_ast(value, indent + 4, visited))
    else:
        lines.append(f"{prefix}{repr(node)}")

    return '\n'.join(lines)

class RustEngine(AbstractTreeEngine):
    def __init__(self):
        self.currentAst = None

    def parse(self, src_code):
        lexer = RustLexer(InputStream(src_code))
        tokens = CommonTokenStream(lexer)
        parser = RustParser(tokens)
        tree = parser.program()
        return tree

    @classmethod
    def to_source_code(self, tree):
        pass
        # print("✍️ Serializing AST back to Rust source...")
        # printer = AstPrinter()
        # return printer.visit(tree)

    @classmethod
    def get_contents(cls, file_path):
        with open(file_path, 'r') as target_file:
            source_code = target_file.read()
        lexer = RustLexer(InputStream(source_code))
        token_stream = CommonTokenStream(lexer)
        parser = RustParser(token_stream)
        tree = parser.program()
        builder = Transformer()
        ast=builder.visit(tree)
        setParents(ast)
        cls.ast = ast
        return ast

    @classmethod
    def process_tree(cls, tree):
        pass

    @classmethod
    def get_modification_points(cls, ast_root):
        points = cls._collect_nodes(ast_root)
        return [(p, p) for p in points]

    @classmethod
    def _collect_nodes(cls, node, visited=None):
        if visited is None:
            visited = set()

        results = []
        if id(node) in visited:
            return results
        visited.add(id(node))

        if isinstance(node, StaticVarDecl):
            # print("adding it", node)
            results.append(node)

        if isinstance(node, FunctionParamList):
            # print("[[[]]]", node.parent)
            results.append(node)

        if isinstance(node, Statement):
            # print("[[[]]]", node.__class__)
            results.append(node)

        if isinstance(node, list):
            for child in node:
                results.extend(cls._collect_nodes(child, visited))
        elif hasattr(node, "__dict__"):
            for val in vars(node).values():
                results.extend(cls._collect_nodes(val, visited))

        return results

    @classmethod
    def do_replace(cls, program, op, trees, modification_points):
        file_name, target_node = op.target
        if isinstance(target_node, tuple):
            _, target_node = target_node

        new_ast = trees[file_name]
        # new_ast1 = move_ast_node(new_ast, target_node)
        # new_ast2 = make_global_static_pointers_unmutable(new_ast, target_node)
        # new_ast3 = safe_wrap_raw_pointers(new_ast2, target_node)
        new_ast4 = safe_wrap_raw_pointer_argumetns(new_ast, target_node)
        trees[file_name] = new_ast4
        program.trees[file_name] = new_ast4
        return trees

    @classmethod
    def do_insert(cls, program, op, trees, modification_points):
        #TODO
        pass

    @classmethod
    def do_delete(cls, program, op, trees, modification_points):
        file_name, target_node = op.target
        if isinstance(target_node, tuple):
            _, target_node = target_node

        new_ast1 = remove_ast_node(trees[file_name], target_node)
        trees[file_name] = new_ast1
        program.trees[file_name] = new_ast1
        return trees

    @classmethod
    def _get_root_node(cls, node):
        while hasattr(node, 'parent') and node.parent is not None:
            node = node.parent
        return node

    @staticmethod
    def _replace_node(target_node, new_node):
        parent = getattr(target_node, 'parent', None)
        if not parent:
            return
        for attr, val in vars(parent).items():
            if val == target_node:
                setattr(parent, attr, new_node)
                return
            elif isinstance(val, list):
                for i in range(len(val)):
                    if val[i] == target_node:
                        val[i] = new_node
                        return

    @classmethod
    def _extract_points_from_top_level(cls, item):
        points = []

        print("point class ", item.__class__)
        if isinstance(item, TopLevelVarDef):
            if str.startswith(item.def_kind, "unsafe"):
                print("item1 is ", item)
                points.append(item)
        if isinstance(item, FunctionDef):
            if item.unsafe:
                points.extend(item)
            print("1")
            for stmt in item.body.stmts:
                points.extend(collect_expressions(stmt, path=[item]))

        elif isinstance(item, TopLevelVarDef):
            print("2")
            fields = getattr(item, 'fields', None)
            if isinstance(fields, list):
                for field in fields:
                    points.extend(collect_expressions(field, path=[item]))
            elif fields is not None:
                print(f"⚠️ Warning: 'fields' on {item} is not a list: {type(fields).__name__}")
                # for field in item.fields:
                #     points.extend(collect_expressions(field, path=[item]))
            if hasattr(item, 'type_'):
                points.extend(collect_expressions(item.type_, path=[item]))

        elif isinstance(item, StructDef):
            print("3")
            if hasattr(item, 'fields'):
                for field in item.fields:
                    points.extend(collect_expressions(field, path=[item]))

        elif isinstance(item, ExternBlock):
            for extern_item in item.items:
                points.extend(collect_expressions(extern_item, path=[item]))

        elif isinstance(item, Attribute):
            for arg in item.args:
                points.extend(collect_expressions(arg, path=[item]))

        elif isinstance(item, TypeAliasDecl):
            points.extend(collect_expressions(item.type, path=[item]))

        elif isinstance(item, InterfaceDef):
            print("54")
            for func in item.functions:
                print("function in interfaceDef")
                points.extend(collect_expressions(func, path=[item]))

        elif isinstance(item, ExternFunctionDecl):
            if item.return_type:
                points.extend(collect_expressions(node=item.return_type, path=[item]))
            for param in item.params:
                points.extend(collect_expressions(param, path=[item]))

        # print("points are ", len(points))

        return points

    @classmethod
    def get_source(cls, program, file_name, index):
        pass

    @classmethod
    def write_to_tmp_dir(cls, contents_of_file, tmp_path):
        pass

    @classmethod
    def dump(cls, contents_of_file, file_name):
        program_ctx = contents_of_file
        # unparser = RustUnparser()
        return program_ctx
        # return unparser.visitProgram(program_ctx)

def collect_expressions(node, path="./", index_map=None) -> List[Tuple[str, object]]:

    if index_map is None:
        index_map = {}
    results = []

    if isinstance(node, FunctionDef):
        if node.unsafe:
            results.append(node)
        collect_expressions(node.body, "./", index_map)

    if isinstance(node, Block):
        if node.isUnsafe:
            results.append(node)
        for stmt in node.stmts:
            collect_expressions(stmt)

    if isinstance(node, Expression):
        results.append((path.rstrip("/"), node))

    if isinstance(node, Statement):
        if isinstance(node, LetStmt):
            for var_def, value in zip(node.var_defs, node.values):
                is_cast_expr = isinstance(value, CastExpr)
                has_type_path = False
                if var_def.type is not None:
                    if  isinstance(var_def.type, TypePathExpression):
                        has_type_path = True
                        results.append(node)
                if is_cast_expr or has_type_path or var_def.type==None:
                    results.append(node)

    if not hasattr(node, "__dict__"):
        return results

    node_type = type(node).__name__
    index_map.setdefault(node_type, 0)
    current_index = index_map[node_type]
    index_map[node_type] += 1

    for field_name, field_value in vars(node).items():
        full_path = f"{path}{node_type}[{current_index}]/{field_name}"
        if isinstance(node, Expression):
            if isinstance(node, UnsafeExpression):
                results.append((full_path, field_value))

        if isinstance(node, Statement):
            results.append((full_path, field_value))

        elif isinstance(node, list):
            for i, item in enumerate(field_value):
                if isinstance(item, (Expression, Statement)):
                    results += collect_expressions(item, f"{full_path}[{i}]/", index_map)

        elif hasattr(node, "__dict__"):
            results += collect_expressions(field_value, f"{full_path}/", index_map)

    return results

def get_file_extension(file_path):
    """
    :param file_path: The path of file
    :type file_path: str
    :return: file extension
    :rtype: str
    """
    _, file_extension = os.path.splitext(file_path)
    return file_extension

def get_all_parents(ast_root, target_node, parent=None):
    if parent is None:
        parent = getattr(target_node, 'parent', None)
        if parent is None:
            raise ValueError("Target node has no parent reference")

    if isinstance(parent, Program):
        return [parent]

    return [parent] + get_all_parents(ast_root, parent, parent.parent)

def remove_node(ast_root, target_node, parents):
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
                        remake_ast_after_removal(target_node, other_tops, top, top_children, top_children_stmts)
                    elif isinstance(top_children, FunctionDef):
                        if isinstance(top_children.body, Block):
                            top_children_stmts = top_children.getChildren()
                            remake_ast_after_removal(target_node, other_tops, top, top_children, top_children_stmts)
            else:
                other_tops.append(top)
                continue

    new_ast = Program(items=other_tops)
    return new_ast

def remake_ast_after_removal(target_node, other_tops, top, top_children, top_children_stmts):
    for stmt in top_children_stmts:
        if statements_eq(stmt, target_node):
            print("equal, applying deletion")
            top_children_stmts.remove(stmt)
            newBlock = Block(top_children_stmts, top_children.isUnsafe)
            top.setBody(newBlock)
            other_tops.append(top)
        else:
            continue

def statements_eq(stmt1, stmt2):
    print("statements_eq_", stmt1, stmt2)
    if not isinstance(stmt1, type(stmt2)):
        return False

    if isinstance(stmt1, LetStmt):
        for i in range(len(stmt1.var_defs)):
            if not (str.__eq__(stmt1.var_defs[i].name, stmt2.var_defs[i].name) and isinstance(stmt1.var_defs[i].type, type(stmt2.var_defs[i].type))):
                print(stmt1.var_defs[i].name, stmt2.var_defs[i].name, stmt1.var_defs[i].type, stmt2.var_defs[i].type)
                return False
        return True

    if isinstance(stmt1, IfStmt):
        print("ifstmts: ", stmt1.condition , stmt2.condition, stmt1.then_branch , stmt2.then_branch , stmt1.else_branch , stmt2.else_branch)
        return (expr_eq(stmt1.condition, stmt2.condition) and
                statements_eq(stmt1.then_branch, stmt2.then_branch) and
                (stmt1.else_branch is None and stmt2.else_branch is None or
                 stmt1.else_branch is not None and stmt2.else_branch is not None and
                 statements_eq(stmt1.else_branch, stmt2.else_branch)))

    if isinstance(stmt1, ForStmt):
        print("forstmt eq case")
        return (
            stmt1.var == stmt2.var and
            expr_eq(stmt1.iterable, stmt2.iterable) and
            statements_eq(stmt1.body, stmt2.body))

    if isinstance(stmt1, CallStmt):
        if not expr_eq(stmt1.callee, stmt2.callee):
            return False
        if len(stmt1.args) != len(stmt2.args):
            return False
        for arg1, arg2 in zip(stmt1.args, stmt2.args):
            if not expr_eq(arg1, arg2):
                return False
        return True

    if isinstance(stmt1, AssignStmt):
        print("assignstmt eq case")
        return (
            expr_eq(stmt1.target, stmt2.target) and
            expr_eq(stmt1.value, stmt2.value))
    
    if isinstance(stmt1, WhileStmt):
        print("whilestmt eq case")
        return (
            expr_eq(stmt1.condition, stmt2.condition) and
            statements_eq(stmt1.body, stmt2.body))

    return False

def expr_eq(expr1, expr2):
    if type(expr1) != type(expr2):
        return False
    if isinstance(expr1, IdentifierExpr):
        return expr1.name == expr2.name
    if isinstance(expr1, StrLiteral):
        return expr1.value == expr2.value
    if isinstance(expr1, IntLiteral):
        return expr1.value == expr2.value
    if isinstance(expr1, BoolLiteral):
        return expr1.value == expr2.value
    if isinstance(expr1, BinaryExpr):
        return (expr_eq(expr1.left, expr2.left) and
                expr_eq(expr1.right, expr2.right) and
                expr1.op == expr2.op)
    if isinstance(expr1, MethodCallExpr):
        return (
            expr_eq(expr1.receiver, expr2.receiver) and
            expr1.method_name == expr2.method_name and
            len(expr1.args) == len(expr2.args) and
            all(expr_eq(a1, a2) for a1, a2 in zip(expr1.args, expr2.args)))
    if isinstance(expr1, FieldAccessExpr):
        return (expr_eq(expr1.receiver, expr2.receiver) and expr_eq(expr1.name, expr2.name))
    return False 

def function_def_eq(func1, func2):
    # print("function_def_eq", func1.identifier, func2.identifier, (func1.params.param_len), (func2.params.param_len), len(func1.body.getChildren()))
    return (func1.identifier == func2.identifier and (func1.params.param_len) == (func2.params.param_len) and len(func1.body.getChildren()) == len(func1.body.getChildren()))

def remove_ast_node(ast_root, target_node):
    parents = get_all_parents(ast_root, target_node)
    print("target node is ", target_node, target_node.parent, parents, len(parents))
    new_ast = remove_node(ast_root, target_node, parents)
    return new_ast

def shuffle_and_update_block(node, block):
    random.shuffle(block.getChildren())
    new_block = Block(block.getChildren(), block.isUnsafe)
    node.setBody(new_block)

def replace_raw_pointer_defs_with_safe_wrappers(node, block):
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

def transform_ast(ast_root, target_node, transform_fn):
    parents = get_all_parents(ast_root, target_node)
    if not isinstance(ast_root, Program):
        return None

    remaining_tops = []
    parent_len = len(parents)

    for top in ast_root.getChildren():
        if parent_len < 3:
            remaining_tops.append(top)
            continue

        parent_1, parent_2 = parents[-2], parents[-3]
        top_type_matches = isinstance(parent_1, type(top))
        if isinstance(top, list):
            top_children = top
        else:
            top_children = top.getChildren()

        if not top_type_matches:
            remaining_tops.append(top)
            continue

        if isinstance(parent_2, type(top_children)):
            if isinstance(top_children, Block):
                transform_fn(top, top_children)
            elif isinstance(top_children, FunctionDef) and isinstance(top_children.body, Block):
                transform_fn(top, top_children.body)

            remaining_tops.append(top)

        elif isinstance(top_children, list):
            matched_children = []
            for item in top_children:
                if isinstance(parent_2, type(item)) and isinstance(item.body, Block):
                    transform_fn(item, item.body)
                    matched_children.append(item)
                else:
                    matched_children.append(item)

            top.setFunctions(matched_children)
            remaining_tops.append(top)

    return Program(items=remaining_tops)

def safe_wrap_raw_pointers(ast_root, target_node):
    return transform_ast(ast_root, target_node, replace_raw_pointer_defs_with_safe_wrappers)

def move_ast_node(ast_root, target_node):
    return transform_ast(ast_root, target_node, shuffle_and_update_block)

def make_global_static_pointers_unmutable(ast_root, target_node):
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
def safe_wrap_raw_pointer_argumetns(ast_root, target_node):
    parents = get_all_parents(ast_root, target_node)
    if not isinstance(ast_root, Program):
        return None

    if not isinstance(target_node, FunctionParamList):
        return ast_root

    remaining_tops = []
    new_params = []

    parent_1 = parents[-2]
    for top in ast_root.getChildren():
        if isinstance(parent_1, type(top)) and isinstance(parent_1, FunctionDef):
            if function_def_eq(parent_1, top):
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