import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from antlr4 import CommonTokenStream, InputStream
from rust.parser.RustLexer import RustLexer
from rust.parser.RustParser import RustParser
# from rust.commons import RustASTTransformer


file_path = "C:\\Users\\aqwan\\Documents\\GitHub\\c2rust\\c2safeRust_examples\\aggregate.rs"
with open(file_path, "r", encoding="utf-8") as f:
    rust_code = f.read()
print("Tokenizing:")
lexer = RustLexer(InputStream(rust_code))
tokens = CommonTokenStream(lexer)
print("Parsing:")
print(tokens)
parser = RustParser(tokens)
print(parser)
tree = parser.program()
# transformer = RustASTTransformer()
# ast = transformer.visit(tree)


