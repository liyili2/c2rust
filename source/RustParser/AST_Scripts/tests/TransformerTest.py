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

TEST_DIR = os.path.join(os.path.dirname(__file__), "test_inputs")
def main():
    test_files = ["bst.rs", "aggregate.rs"]
    for filename in test_files:
        try:
            print(f"Testing {filename}")
            file_path = os.path.join(os.path.dirname(__file__), filename)
            with open(file_path, "r", encoding="utf-8") as f:
                rust_code = f.read()

            lexer = RustLexer(InputStream(rust_code))
            tokens = CommonTokenStream(lexer)
            parser = RustParser(tokens)
            tree = parser.program()
            print(pretty_print_ast(tree))

            builder = Transformer()
            custom_ast = builder.visit_Program(tree)
            print(pretty_print_ast(custom_ast))

        except Exception as e:
            print(f"❌ Error processing {filename}: {e}")
            raise

if __name__ == "__main__":
    main()
