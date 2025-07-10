import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from antlr4 import CommonTokenStream, InputStream
from RustParser.AST_Scripts.antlr.RustLexer import RustLexer
from RustParser.AST_Scripts.antlr.RustParser import RustParser
from RustParser.AST_Scripts.ast.Transformer import Transformer
from RustParser.AST_Scripts.ast.TypeChecker import TypeChecker
from RustParser.AST_Scripts.ast.Program import Program
from RustParser.AST_Scripts.ast.TopLevel import TopLevel
from RustParser.AST_Scripts.ast.ASTNode import ASTNode

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

file_path = os.path.join(os.path.dirname(__file__), "aggregate.rs")
with open(file_path, "r", encoding="utf-8") as f:
    rust_code = f.read()
lexer = RustLexer(InputStream(rust_code))
tokens = CommonTokenStream(lexer)
parser = RustParser(tokens)
tree = parser.program()
print(pretty_print_ast(tree))
builder = Transformer()
custom_ast = builder.visit(tree)
# set_parents(custom_ast)
checker = TypeChecker()
checker.visit(custom_ast)
print("Type Error Count : ", checker.error_count)
print("Pretty AST:")
# print(pretty_print_ast(custom_ast))