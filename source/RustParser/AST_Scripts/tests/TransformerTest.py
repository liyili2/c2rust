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

def pretty_print_ast(node, indent=0, show_parent=False):
    if isinstance(node, list):
        return '\n'.join(pretty_print_ast(n, indent, show_parent) for n in node)

    if isinstance(node, ASTNode):
        lines = [f"{' ' * indent}{node.__class__.__name__}:"]        
        if show_parent and hasattr(node, 'parent') and node.parent:
            lines.append(f"{' ' * (indent + 2)}parent: {node.parent.__class__.__name__}")

        for attr, value in vars(node).items():
            if attr == 'parent':
                continue
            lines.append(f"{' ' * (indent + 2)}{attr}:")
            lines.append(pretty_print_ast(value, indent + 4, show_parent))
        return '\n'.join(lines)
    return f"{' ' * indent}{repr(node)}"

file_path = os.path.join(os.path.dirname(__file__), "bst.rs")
with open(file_path, "r", encoding="utf-8") as f:
    rust_code = f.read()
lexer = RustLexer(InputStream(rust_code))
tokens = CommonTokenStream(lexer)
parser = RustParser(tokens)
tree = parser.program()
print(pretty_print_ast(tree))
builder = Transformer()
custom_ast = builder.visit(tree)
set_parents(custom_ast)
checker = TypeChecker()
checker.visit(custom_ast)
print("Type Error Count : ", checker.error_count)
print("Pretty AST:")
print(pretty_print_ast(custom_ast, show_parent=True))