import os
from RustParser.AST_Scripts.ast.Block import Block
from RustParser.AST_Scripts.antlr.RustLexer import RustLexer
from antlr4 import CommonTokenStream, InputStream
from RustParser.AST_Scripts.antlr.RustParser import RustParser
from RustParser.AST_Scripts.ast.Transformer import Transformer
from RustParser.AST_Scripts.ast.Expression import Expression, UnsafeExpression
from RustParser.AST_Scripts.ast.Statement import LetStmt, Statement
from RustParser.AST_Scripts.ast.TopLevel import Attribute, ExternBlock, ExternFunctionDecl, FunctionDef, InterfaceDef, StructDef, TopLevel, TopLevelVarDef, TypeAliasDecl
from RustParser.AST_Scripts.ast.TypeChecker import TypeChecker
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
        ast = builder.visit(tree)
        cls.ast = ast
        return ast

    @classmethod
    def process_tree(cls, tree):
        pass

    @classmethod
    def get_modification_points(cls, ast_root):
        print("in get_modification_points", ast_root.__class__)
        modification_points = []

        for item in ast_root.items:
            if isinstance(item, list):
                for subitem in item:
                    modification_points.extend(cls._extract_points_from_top_level(subitem))
            else:
                modification_points.extend(cls._extract_points_from_top_level(item))

        print("modification points' number is ", len(modification_points))
        return modification_points

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

    print("collect_expressions", node.__class__)
    if isinstance(node, FunctionDef):
        if node.unsafe:
            results.append(node)
        collect_expressions(node.body, "./", index_map)

    if isinstance(node, Block):
        if node.isUnsafe:
            print("unsafe block ", node)
            results.append(node)
        for stmt in node.stmts:
            collect_expressions(stmt)

    if isinstance(node, Expression):
        results.append((path.rstrip("/"), node))

    if not hasattr(node, "__dict__"):
        return results

    node_type = type(node).__name__
    index_map.setdefault(node_type, 0)
    current_index = index_map[node_type]
    index_map[node_type] += 1

    for field_name, field_value in vars(node).items():
        full_path = f"{path}{node_type}[{current_index}]/{field_name}"
        # print("full path is ", full_path)
        if isinstance(node, Expression):
            if isinstance(node, UnsafeExpression):
                print("0000")
                results.append((full_path, field_value))

        if isinstance(node, Statement):
            results.append((full_path, field_value))

        elif isinstance(node, list):
            print("2222")
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
