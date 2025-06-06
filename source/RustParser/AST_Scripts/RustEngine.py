from antlr4 import CommonTokenStream, InputStream
import os, sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from pyggi.tree.abstract_engine import AbstractTreeEngine
from RustParser.AST_Scripts.antlr.RustLexer import RustLexer
from RustParser.AST_Scripts.antlr.RustParser import RustParser
from pyggi.tree.tree import TreeProgram

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
        return pretty_print_ast(tree)
    
    @classmethod
    def get_contents(cls, file_path):
        pass

    @classmethod
    def get_modification_points(cls, contents_of_file):
        pass

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

class MyRustProgram(TreeProgram):
    def __init__(self, path, config):
        super().__init__(path, config)
        self.files = "./"
        self.engine_classes = {
            '.rs': RustEngine
        }

    @classmethod
    def get_engine(cls, file_name):
        if file_name.endswith(".rs"):
            return RustEngine
        print("detecting engine!")
        extension = get_file_extension(file_name)
        print("ext is ", extension)
        if extension in ['.rs']:
            return RustEngine
        else:
            raise Exception('{} file is not supporteddddd'.format(extension))
