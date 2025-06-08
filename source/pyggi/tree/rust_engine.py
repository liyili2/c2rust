
import os
from RustParser.AST_Scripts.antlr.RustLexer import RustLexer
from antlr4 import CommonTokenStream, InputStream
from RustParser.AST_Scripts.antlr.RustParser import RustParser
from RustParser.AST_Scripts.ast.Transformer import Transformer
from pyggi.tree.abstract_engine import AbstractTreeEngine

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
    def parse(self, src_code):
        lexer = RustLexer(InputStream(src_code))
        tokens = CommonTokenStream(lexer)
        parser = RustParser(tokens)
        tree = parser.program()
        return tree  # Use your AST node visitor if needed

    def to_source_code(self, tree):
        print("reached pretty-printed ast!!")

    @classmethod
    def get_contents(cls, file_path):
        print("in rust engine get contents")
        with open(file_path, 'r') as target_file:
            source_code = target_file.read()
        lexer = RustLexer(InputStream(source_code))
        token_stream = CommonTokenStream(lexer)
        parser = RustParser(token_stream)
        tree = parser.program()
        builder = Transformer()
        ast = builder.visit_Program(tree)
        # cls.process_tree(tree)
        # print("****************", pretty_print_ast(ast))
        return ast

    @classmethod
    def process_tree(cls, tree):
        # No processing needed for now
        pass

    @classmethod
    def get_modification_points(cls, contents_of_file):
        print("happy happy!!")
        def aux(accu, prefix, node):
            type_counter = dict()

            for child in getattr(node, 'children', []):
                tag = child.__class__.__name__
                type_counter[tag] = type_counter.get(tag, 0) + 1
                s = '{}/{}[{}]'.format(prefix, tag, type_counter[tag])
                accu.append(s)
                aux(accu, s, child)
            return accu
        return aux([], '.', contents_of_file)

    @classmethod
    def get_source(cls, program, file_name, index):
        pass

    @classmethod
    def write_to_tmp_dir(cls, contents_of_file, tmp_path):
        pass

    @classmethod
    def dump(cls, contents_of_file):
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
