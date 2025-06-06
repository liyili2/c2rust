import os
from RustParser.AST_Scripts.ast.ASTNode import ASTNode
from pyggi.base.program import AbstractProgram
from RustParser.AST_Scripts.antlr.RustLexer import RustLexer
from antlr4 import CommonTokenStream, InputStream
from RustParser.AST_Scripts.antlr.RustParser import RustParser

class RustEngine():
    def parse(self, src_code):
        lexer = RustLexer(InputStream(src_code))
        tokens = CommonTokenStream(lexer)
        parser = RustParser(tokens)
        tree = parser.program()
        return tree  # Use your AST node visitor if needed

    def to_source_code(self, tree):
        print("reached pretty-printed ast!!")

class Program(AbstractProgram):
    def __init__(self, items, path):
        super().__init__(path=path)
        self.items = items  # A list of FunctionDef, StructDef, etc.
        self.path = path

    def accept(self, visitor):
        return visitor.visit_Program(self)

    def get_file_extension(file_path):
        """
        :param file_path: The path of file
        :type file_path: str
        :return: file extension
        :rtype: str
        """
        _, file_extension = os.path.splitext(file_path)
        return file_extension

    @classmethod
    def get_engine(cls, file_name):
        _, extension = os.path.splitext(file_name)
        if extension == '.rs':
            return RustEngine
        raise Exception(f'Unsupported file extension: {extension}')
