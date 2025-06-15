import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from RustParser.AST_Scripts.ast.RustTreeProgram import RustASTProgram
from antlr4 import FileStream, CommonTokenStream, InputStream
from RustParser.AST_Scripts.antlr.RustLexer import RustLexer
from RustParser.AST_Scripts.antlr.RustParser import RustParser
from RustParser.AST_Scripts.ast.Transformer import Transformer
from RustParser.AST_Scripts.ast.TypeChecker import TypeChecker

def parse_rust_code():
    file_path = os.path.join(os.path.dirname(__file__), "bst.rs")
    with open(file_path, "r", encoding="utf-8") as f:
        rust_code = f.read()
    lexer = RustLexer(InputStream(rust_code))
    token_stream = CommonTokenStream(lexer)
    parser = RustParser(token_stream)
    tree = parser.program()
    return tree

def transform(tree):
    transformer = Transformer()
    ast = transformer.visit(tree)
    return ast

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

def test_pipeline():
    tree = parse_rust_code()
    ast = transform(tree)
    program = RustASTProgram(ast)
    print("tree is ", program.__class__)
    # mutation = ReplaceExpr()

    # algo = FirstImprovement(
    #     operators=None,
    #     max_iterations=20
    # )

    # algo.run(program)
    print(f"Best fitness: {program.fitness}")

if __name__ == "__main__":
    test_pipeline()
