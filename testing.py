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
marker = MarkingVisitor(ast)
marked_ast = marker.run()

all_marked = marked_ast.list_marked_nodes()

marked_with_ids = marked_ast.list_marked_nodes_with_ids()
marked_nodes_count = 0
for uid, node in marked_with_ids:
    print(f"{uid}: {type(node).__name__}")
    marked_nodes_count += 1

print("marked ast has ", marked_nodes_count, " marked nodes")

# node = marked_ast.get_random_marked()
# print("marked node: ", node)
engine = RustEngine()
engine.get_contents(file_path)
# printer = RustASTPrinter()
# reassmbled_source = printer.visit(ast)
