import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from antlr4 import CommonTokenStream, InputStream
from RustParser.AST_Scripts.antlr.RustLexer import RustLexer
from RustParser.AST_Scripts.antlr.RustParser import RustParser
from RustParser.AST_Scripts.ast.Transformer import Transformer
from RustParser.AST_Scripts.ast.Simulator import Simulator
from RustParser.AST_Scripts.ast.TypeChecker import TypeChecker
from RustParser.AST_Scripts.ast.TopLevel import *
from RustParser.AST_Scripts.ast.ASTNode import *
from RustParser.AST_Scripts.ast.Program import *

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

def setParents(node, parent=None, top_level_prog=None):
    if not isinstance(node, ASTNode):
        return
    if isinstance(node, Program):
        top_level_prog = node
    if isinstance(node, FunctionDef) and isinstance(parent, InterfaceDef):
        node.parent = parent
    elif isinstance(node, TopLevel) and top_level_prog:
        node.parent = top_level_prog
    elif parent is not None:
        node.parent = parent
    for attr, value in vars(node).items():
        if attr == "parent":
            continue
        if isinstance(value, list):
            for item in value:
                setParents(item, node, top_level_prog)
        elif isinstance(value, ASTNode):
            setParents(value, node, top_level_prog)

file_path = os.path.join(os.path.dirname(__file__), "test11.rs")
with open(file_path, "r", encoding="utf-8") as f:
    rust_code = f.read()
lexer = RustLexer(InputStream(rust_code))
tokens = CommonTokenStream(lexer)
parser = RustParser(tokens)
tree = parser.program()
transformer = Transformer()
ast = transformer.visit(tree)
setParents(ast)
checker = TypeChecker()
checker.visit(ast)
memory = dict()
stack = dict()
builder = Simulator(memory=memory, stack=stack)
sim_result = builder.visit(ast)

print("Type Error Count : ", checker.error_count)
# print("Pretty AST:")
# print(pretty_print_ast(custom_ast))