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
from c2rust.source.pyggi.mutation.deletion import DeletionOperator
from c2rust.source.pyggi.mutation.replacement import ReplacementOperator
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
    # def __init__(self):
    # currentAst = None

    def parse(self, src_code):
        lexer = RustLexer(InputStream(src_code))
        tokens = CommonTokenStream(lexer)
        parser = RustParser(tokens)
        tree = parser.program()
        return tree

    @classmethod
    def to_source_code(self, tree):
        pass

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
            results.append(node)

        if isinstance(node, FunctionParamList):
            results.append(node)

        if isinstance(node, Statement):
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
        replacementOperator = ReplacementOperator()
        replacementOperator.apply()
        # TODO
        # new_ast1 = move_ast_node(new_ast, target_node)
        # new_ast2 = make_global_static_pointers_unmutable(new_ast, target_node)
        # new_ast3 = safe_wrap_raw_pointers(new_ast2, target_node)
        # new_ast4 = safe_wrap_raw_pointer_argumetns(new_ast, target_node)
        # trees[file_name] = new_ast4
        # program.trees[file_name] = new_ast4
        # return trees

    @classmethod
    def do_insert(cls, program, op, trees, modification_points):
        #TODO
        pass

    @classmethod
    def do_delete(cls, program, op, trees, modification_points):
        file_name, target_node = op.target
        if isinstance(target_node, tuple):
            _, target_node = target_node

        deletionOperator = DeletionOperator()
        # TODO
        # trees[file_name] = new_ast1
        # program.trees[file_name] = new_ast1
        # return trees

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
