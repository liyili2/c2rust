import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from antlr4 import FileStream, CommonTokenStream, InputStream
from RustParser.AST_Scripts.antlr.RustLexer import RustLexer
from RustParser.AST_Scripts.antlr.RustParser import RustParser
from RustParser.AST_Scripts.ast.Transformer import Transformer
from RustParser.AST_Scripts.ast.TypeChecker import TypeChecker

def parse_rust_code():
    file_path = os.path.join(os.path.dirname(__file__), "bst.rs")
    with open(file_path, "r", encoding="utf-8") as f:
        rust_code = f.read()
    lexer = RustLexer(InputStream(rust_code))
    token_stream = CommonTokenStream(lexer)
    parser = RustParser(token_stream)
    tree = parser.program()
    return tree

def transform(tree):
    transformer = Transformer()
    ast = transformer.visit(tree)
    return ast

def test_pipeline():
    tree = parse_rust_code()
    ast = transform(tree)
    checker = TypeChecker()
    checker.visit(ast)
    print(f"Type Errors: {checker.error_count}")

if __name__ == "__main__":
    test_pipeline()
