import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from antlr4 import CommonTokenStream, InputStream
from rust.parser.RustLexer import RustLexer
from rust.parser.RustParser import RustParser
from rust.commons.RustASTTransformer import RustASTTransformer
from rust.ast.RustASTPrinter import RustASTPrinter
from rust.ast.MarkingVisitor import MarkingVisitor
from repair.pyggi.tree.rust_engine import RustEngine
from rust.ast.MarkingVisitor import MarkingVisitor

def pretty_print_ast(node, indent=0, visited=None):
    if visited is None:
        visited = set()

    lines = []
    prefix = ' ' * indent

    if isinstance(node, (str, int, float, bool, type(None))):
        return f"{prefix}{repr(node)}"

    node_id = id(node)
    if node_id in visited:
        return f"{prefix}<Cycle: {type(node).__name__}>"

    visited.add(node_id)

    if isinstance(node, list):
        for n in node:
            lines.append(pretty_print_ast(n, indent, visited))
    elif hasattr(node, '__dict__'):
        lines.append(f"{prefix}{type(node).__name__}:")
        for attr, value in vars(node).items():
            if attr == "parent":
                continue
            lines.append(f"{prefix}  {attr}:")
            lines.append(pretty_print_ast(value, indent + 4, visited))
    else:
        lines.append(f"{prefix}{repr(node)}")

    return '\n'.join(lines)

file_path = "./c2safeRust_examples/aggregate.rs"
# file_path = "C:\\Users\\aqwan\\Documents\\GitHub\\c2rust\\c2safeRust_examples\\aggregate.rs"
with open(file_path, "r", encoding="utf-8") as f:
    rust_code = f.read()
print("Tokenizing:")
lexer = RustLexer(InputStream(rust_code))
tokens = CommonTokenStream(lexer)
print("Parsing:")
# print(tokens)
parser = RustParser(tokens)
# print(parser)
tree = parser.program()
transformer = RustASTTransformer()
ast = transformer.visit(tree)
# Use transformer, then use rust ast printer afterwards

marker = MarkingVisitor(ast)
marker.visit(ast)

# print("Pretty AST:")

# pretty = pretty_print_ast(ast)
# print(pretty)

# test_printer = RustASTPrinter()
# testing = test_printer.visitProgram(ast)

# marker = MarkingVisitor(ast)
# marked_ast = marker.run()
#
# all_marked = marked_ast.list_marked_nodes()
#
# marked_with_ids = marked_ast.list_marked_nodes_with_ids()
# marked_nodes_count = 0
# for uid, node in marked_with_ids:
#     print(f"{uid}: {type(node).__name__}")
#     marked_nodes_count += 1
#
# print("marked ast has ", marked_nodes_count, " marked nodes")
#
# # node = marked_ast.get_random_marked()
# # print("marked node: ", node)
# engine = RustEngine()
# engine.get_contents(file_path)
# # printer = RustASTPrinter()
# # reassmbled_source = printer.visit(ast)
# node = marked_ast.get_random_marked()
# print("marked node: ", node)
# engine = RustEngine()
# engine.get_contents(file_path)
# printer = RustASTPrinter()
# reassmbled_source = printer.visit(ast)
