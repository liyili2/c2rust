import sys
import os


#import rust.parser.RustParser

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from antlr4 import CommonTokenStream, InputStream
from rust.parser.RustLexer import RustLexer
from rust.parser.RustParser import RustParser
# from rust.ast.Transformer import ParseTreeASTTransformer
from rust.commons.RustASTTransformer import RustASTTransformer
from rust.ast.RustASTPrinter import RustASTPrinter


file_path = "/home/liyili2/project/compiler_sem_projects/c2rust/Benchmarks/aggregate/aggregate.rs"
with open(file_path, "r", encoding="utf-8") as f:
    rust_code = f.read()
print("Tokenizing:")
lexer = RustLexer(InputStream(rust_code))
abc = CommonTokenStream(lexer)
print("Parsing:")
parser = RustParser(abc)
tree = parser.program()
transformer = RustASTTransformer()
ast = transformer.visit(tree)
printer = RustASTPrinter()
reassmbled_source = printer.visit(ast)
print(reassmbled_source)
