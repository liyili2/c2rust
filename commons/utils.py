from antlr4 import CommonTokenStream, InputStream
from rust.parser.RustLexer import RustLexer
from rust.parser.RustParser import RustParser
from rust.commons.RustASTTransformer import RustASTTransformer


def parse_string_to_ast(rust_string: str):
    lexer = RustLexer(InputStream(rust_string))
    tokens = CommonTokenStream(lexer)
    parser = RustParser(tokens)
    tree = parser.program()
    transformer = RustASTTransformer()
    ast = transformer.visit(tree)

    return ast
