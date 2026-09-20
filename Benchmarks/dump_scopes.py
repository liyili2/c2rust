"""
dump_scopes.py

Walks the whole marked AST and prints, for EVERY modification point, the node
type and the names that RandomCandidateReplacementGenerator would see in scope
there. Nothing is mutated. Run it from the same directory as show_mutation.py.
"""

import sys
import os
import random
from collections import Counter

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from antlr4 import CommonTokenStream, InputStream
from rust.parser.RustLexer import RustLexer
from rust.parser.RustParser import RustParser
from rust.commons.RustASTTransformer import RustASTTransformer
from rust.visitors.MarkingVisitor import MarkingVisitor
from rust.visitors.RandomCandidateReplacementGenerator import RandomCandidateReplacementGenerator
from rust.modification.ScopeEnvironment import ScopeEnvironment


class ScopeDumper(RandomCandidateReplacementGenerator):
    """Reuses the generator's scope threading, but only records and prints."""

    def __init__(self):
        # Skip the parent's __init__ (it needs a selected node); no mutation happens here.
        self._selected_id = None
        self._rng = random.Random(0)
        self._scope = ScopeEnvironment()
        self.records = []  # (node type name, tuple of scope names)

    def visitMarkedASTNode(self, node):
        kind = type(node.node).__name__
        names = tuple(self._scope.names())
        self.records.append((kind, names))
        print(f"{kind:<24} scope={list(names)}")
        # _selected_id is None, so the parent falls through to the default rebuild.
        return super().visitMarkedASTNode(node)


file_path = "./avl/avl.rs"

with open(file_path, "r", encoding="utf-8") as f:
    rust_code = f.read()

lexer = RustLexer(InputStream(rust_code))
tokens = CommonTokenStream(lexer)
parser = RustParser(tokens)
tree = parser.program()
ast = RustASTTransformer().visit(tree)
marked_ast = ast.accept(MarkingVisitor())

dumper = ScopeDumper()
marked_ast.accept(dumper)

print()
print("=" * 70)
print(f"{len(dumper.records)} modification points; distinct scopes seen:")
print("=" * 70)
for names, count in Counter(names for _, names in dumper.records).most_common():
    print(f"{count:>4} x {list(names)}")
