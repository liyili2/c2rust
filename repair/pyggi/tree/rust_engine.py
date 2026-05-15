import os
from antlr4 import CommonTokenStream, InputStream
from rust.parser.RustLexer import RustLexer
from rust.parser.RustParser import RustParser
from rust.commons.RustASTTransformer import setParents
from rust.commons.RustASTTransformer import RustASTTransformer
from repair.pyggi.mutation.replacement import ReplacementOperator
from repair.pyggi.tree.abstract_engine import AbstractTreeEngine
from typing import List, Tuple
from rust.ast.TopLevel import *
from rust.ast.Statement import *
from rust.ast.Expression import *
from rust.ast.Func import *
from rust.ast.registry import ASTNodeRegistry

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
    # def parse(self, src_code):
    #     lexer = RustLexer(InputStream(src_code))
    #     tokens = CommonTokenStream(lexer)
    #     parser = RustParser(tokens)
    #     tree = parser.program()
    #     return tree

    @classmethod
    def to_source_code(self, tree):
        pass

    @classmethod
    def get_contents(cls, file_path):
        print("get_contents", file_path)
        with open(file_path, 'r') as target_file:
            source_code = target_file.read()
        lexer = RustLexer(InputStream(source_code))
        token_stream = CommonTokenStream(lexer)
        parser = RustParser(token_stream)
        tree = parser.program()
        builder = RustASTTransformer()
        ast=builder.visit(tree)
        setParents(ast)
        cls.ast = ast
        cls.get_modification_points()
        return ast

    @classmethod
    def process_tree(cls, tree):
        pass

    @classmethod
    def get_modification_points(cls):
        p = cls.get_modification_point()
        print("point is ", p)

    @classmethod
    def get_modification_point(cls):
        return ASTNodeRegistry.get_random_marked_node()

    @classmethod
    def do_replace(cls, program, op, trees, modification_points):
        # TODO
        pass

    @classmethod
    def do_delete(cls, program, op, trees, modification_points):
        # TODO
        pass

    @classmethod
    def do_insert(cls, program, op, trees, modification_points):
        # TODO
        pass

    @classmethod
    def get_source(cls, program, file_name, index):
        pass

    @classmethod
    def write_to_tmp_dir(cls, contents_of_file, tmp_path):
        pass

    @classmethod
    def dump(cls, contents_of_file, file_name):
        pass

def get_file_extension(file_path):
    """
    :param file_path: The path of file
    :type file_path: str
    :return: file extension
    :rtype: str
    """
    _, file_extension = os.path.splitext(file_path)
    return file_extension
