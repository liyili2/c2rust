import sys
import os

from rust.ast.AstPrinter import AstPrinter
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from antlr4 import CommonTokenStream, InputStream
from rust.parser.RustLexer import RustLexer
from rust.parser import RustParser
from rust.ast.Transformer import ParseTreeASTTransformer

file_path = os.path.join(os.path.dirname(__file__), "bst.rs")
with open(file_path, "r", encoding="utf-8") as f:
    rust_code = f.read()
lexer = RustLexer(InputStream(rust_code))
tokens = CommonTokenStream(lexer)
parser = RustParser(tokens)
tree = parser.program()
# print(pretty_print_ast(tree))
builder = ParseTreeASTTransformer()
custom_ast = builder.visit(tree)
printer = AstPrinter()
reassmbled_source = printer.visit(custom_ast)
src_path = os.path.join("./RustParser/AST_Scripts/tests/", "reassembled.rs")
with open(src_path, "w", encoding="utf-8") as f:
    f.write(reassmbled_source)
# checker = TypeChecker()
# checker.visit(custom_ast)
# print("Type Error Count : ", checker.error_count)
# print("Pretty AST:")
# print(pretty_print_ast(custom_ast))