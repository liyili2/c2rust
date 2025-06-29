import sys
import os

from RustParser.AST_Scripts.tests.TransformerTest import pretty_print_ast
from RustParser.AST_Scripts.ast.AstPrinter import AstPrinter
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from antlr4 import CommonTokenStream, InputStream
from RustParser.AST_Scripts.antlr.RustLexer import RustLexer
from RustParser.AST_Scripts.antlr.RustParser import RustParser
from RustParser.AST_Scripts.ast.Transformer import Transformer
from RustParser.AST_Scripts.ast.TypeChecker import TypeChecker

file_path = os.path.join(os.path.dirname(__file__), "bst.rs")
with open(file_path, "r", encoding="utf-8") as f:
    rust_code = f.read()
lexer = RustLexer(InputStream(rust_code))
tokens = CommonTokenStream(lexer)
parser = RustParser(tokens)
tree = parser.program()
# print(pretty_print_ast(tree))
builder = Transformer()
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