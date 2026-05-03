import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from antlr4 import CommonTokenStream, InputStream
from rust.parser.RustLexer import RustLexer
from rust.parser import RustParser
# from rust.ast.Transformer import ParseTreeASTTransformer


file_path = "C:\\Users\\aqwan\\Documents\\GitHub\\c2rust\\Benchmarks\\avl\\avl.rs"
with open(file_path, "r", encoding="utf-8") as f:
    rust_code = f.read()
print("Tokenizing:")
lexer = RustLexer(InputStream(rust_code))
tokens = CommonTokenStream(lexer)
print("Parsing:")
parser = RustParser(tokens)


