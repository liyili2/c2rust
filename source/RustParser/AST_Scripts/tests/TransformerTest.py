import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from antlr4 import CommonTokenStream, InputStream
from RustParser.AST_Scripts.antlr.RustLexer import RustLexer
from RustParser.AST_Scripts.antlr.RustParser import RustParser
from RustParser.AST_Scripts.ast.Transformer import Transformer
from RustParser.AST_Scripts.ast.TypeChecker import TypeChecker

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

#TODO: test the assignment of negative numbers to integers
lexer = RustLexer(InputStream("fn main(){let a : i32 = 1; a=12;let b = true;if b{a=2;}else{a=1;}let nums: [i32; 3] = [1,2,3];}"))
tokens = CommonTokenStream(lexer)
parser = RustParser(tokens)
tree = parser.program()
print(pretty_print_ast(tree))
builder = Transformer()
custom_ast = builder.visit_Program(tree)
checker = TypeChecker()
# checker.visit(custom_ast)
print("Pretty AST:")
print(pretty_print_ast(custom_ast))
