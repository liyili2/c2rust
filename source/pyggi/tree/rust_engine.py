import os
from RustParser.AST_Scripts.ast.AstPrinter import AstPrinter
from RustParser.AST_Scripts.ast.Block import Block
from RustParser.AST_Scripts.antlr.RustLexer import RustLexer
from antlr4 import CommonTokenStream, InputStream
from RustParser.AST_Scripts.antlr.RustParser import RustParser
from RustParser.AST_Scripts.ast.Transformer import Transformer
from RustParser.AST_Scripts.ast.Expression import BinaryExpr, CastExpr, Expression, TypePathExpression, UnsafeExpression
from RustParser.AST_Scripts.ast.Statement import IfStmt, LetStmt, Statement
from RustParser.AST_Scripts.ast.TopLevel import Attribute, ExternBlock, ExternFunctionDecl, FunctionDef, InterfaceDef, StructDef, TopLevel, TopLevelVarDef, TypeAliasDecl
from RustParser.AST_Scripts.ast.TypeChecker import TypeChecker
from RustParser.AST_Scripts.ast.Type import PointerType, RefType
from pyggi.tree.rust_unparser import RustUnparser
from pyggi.tree.abstract_engine import AbstractTreeEngine
from typing import List, Tuple

def pretty_print_ast(node, indent=0):
    spacer = '  ' * indent
    if isinstance(node, list):
        return '\n'.join(pretty_print_ast(n, indent) for n in node)

    if hasattr(node, '__dict__'):
        lines = [f"{spacer}{node.__class__.__name__}:"]
        for key, value in vars(node).items():
            lines.append(f"{spacer}  {key}:")
            lines.append(pretty_print_ast(value, indent + 2))
        return '\n'.join(lines)
    else:
        return f"{spacer}{repr(node)}"

class RustEngine(AbstractTreeEngine):
    def __init__(self):
        self.currentAst = None

    def parse(self, src_code):
        lexer = RustLexer(InputStream(src_code))
        tokens = CommonTokenStream(lexer)
        parser = RustParser(tokens)
        tree = parser.program()
        return tree  # Use your AST node visitor if needed

    @classmethod
    def to_source_code(self, tree):
        print("✍️ Serializing AST back to Rust source...")
        printer = AstPrinter()
        return printer.visit(tree)

    @classmethod
    def get_contents(cls, file_path):
        with open(file_path, 'r') as target_file:
            source_code = target_file.read()
        lexer = RustLexer(InputStream(source_code))
        token_stream = CommonTokenStream(lexer)
        parser = RustParser(token_stream)
        tree = parser.program()
        builder = Transformer()
        ast = builder.visit(tree)
        cls.ast = ast
        return ast

    @classmethod
    def process_tree(cls, tree):
        pass

    @classmethod
    def get_modification_points(cls, ast_root):
        points = cls._collect_nodes(ast_root)
        print("points are ", len(points))
        file_name = "bst.rs"
        return [(file_name, p) for p in points]

    @classmethod
    def _collect_nodes(cls, node):
        results = []

        # if isinstance(node, (Statement, Expression)):
        #     print(f"✅ Found node: {type(node).__name__}")
        #     results.append(node)
        if isinstance(node, Statement):
            # print("=========", node.__class__)
            results.append(node)

        if isinstance(node, list):
            for child in node:
                results.extend(cls._collect_nodes(child))
        elif hasattr(node, "__dict__"):
            for val in vars(node).values():
                results.extend(cls._collect_nodes(val))

        return results

    @classmethod
    def do_replace(cls, program, op, new_contents, modification_points):
        print("do_replace")
        file_name, target_node = op.target
        # Replace the node in AST
        cls._replace_node(target_node, new_contents)
        return

    @classmethod
    def do_insert(cls, program, op, new_contents, modification_points):
        print("do_insert")
        file_name, target_node = op.target
        # You need to decide: insert *before*, *after*, or *into*
        # Let's say we insert after the current node
        parent = getattr(target_node, 'parent', None)
        if parent and hasattr(parent, 'body') and isinstance(parent.body, list):
            idx = parent.body.index(target_node)
            parent.body.insert(idx + 1, new_contents)
        return

    @classmethod
    def do_delete(cls, program, op, new_contents, modification_points):
        print("do_delete")
        file_name, target_node = op.target
        parent = getattr(target_node, 'parent', None)
        if parent and hasattr(parent, 'body') and isinstance(parent.body, list):
            parent.body.remove(target_node)
        return

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
        program_ctx = contents_of_file  # or tree.root or similar depending on your parser wrapper
        unparser = RustUnparser()
        return unparser.visitProgram(program_ctx)

def collect_expressions(node, path="./", index_map=None) -> List[Tuple[str, object]]:

    if index_map is None:
        index_map = {}
    results = []

    # print("collect_expressions", node.__class__)
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

        # elif isinstance(node, IfStmt):
        #     if isinstance(node.condition, BinaryExpr):
        #         if is_problematic(node.condition.left) or is_problematic(node.condition.type):

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

def is_problematic(node):
    return isinstance(node, PointerType) or isinstance(node, RefType) or isinstance(node, TypePathExpression) or isinstance(node, CastExpr) 

def get_file_extension(file_path):
    """
    :param file_path: The path of file
    :type file_path: str
    :return: file extension
    :rtype: str
    """
    _, file_extension = os.path.splitext(file_path)
    return file_extension
