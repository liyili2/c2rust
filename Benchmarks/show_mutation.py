"""
show_mutation.py

Parses ./avl/avl.rs, marks its modification points, picks ONE random expression
inside an unsafe function, mutates it, and shows what changed.

Usage (run from the directory that contains this file and ./avl/avl.rs):

    python show_mutation.py            # random seed (printed, so you can reproduce it)
    python show_mutation.py 7          # fixed seed -> same mutation every run
    python show_mutation.py 7 --brief  # only the summary, skip the two full dumps
"""

import sys
import os
import random
import difflib

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from antlr4 import CommonTokenStream, InputStream
from rust.parser.RustLexer import RustLexer
from rust.parser.RustParser import RustParser
from rust.commons.RustASTTransformer import RustASTTransformer
from rust.visitors.Printers import RustASTPrinter
from rust.visitors.MarkingVisitor import MarkingVisitor
from rust.visitors.RandomCandidateReplacementGenerator import RandomCandidateReplacementGenerator
from rust.nodes.TopLevel import FunctionDefinition
from rust.modification.Constraint import Constraint, ConstraintChecker
from rust.modification.ModificationPointSelector import ModificationPointSelector


args = [a for a in sys.argv[1:] if not a.startswith("--")]
brief = "--brief" in sys.argv[1:]

seed = int(args[0]) if args else random.randrange(2 ** 32)
print(f"seed = {seed}")

file_path = "./avl/avl.rs"

with open(file_path, "r", encoding="utf-8") as f:
    rust_code = f.read()

lexer = RustLexer(InputStream(rust_code))
tokens = CommonTokenStream(lexer)
parser = RustParser(tokens)
tree = parser.program()
transformer = RustASTTransformer()
ast = transformer.visit(tree)

printer = RustASTPrinter()
marked_ast = ast.accept(MarkingVisitor())

# Eligibility: ANY marked expression, but only inside unsafe functions.
unsafe_functions = ConstraintChecker([Constraint(FunctionDefinition, "is_unsafe", True)])
selector = ModificationPointSelector(scope_checker=unsafe_functions, rng=random.Random(seed))

print(f"eligible modification points: {len(selector.eligible_points(marked_ast))}")
selected = selector.select(marked_ast)

if selected is None:
    print("No eligible modification points found.")
    sys.exit(0)

print("Selected point (original):")
print("   ", selected.node.accept(printer))
print()

generator = RandomCandidateReplacementGenerator(selected, rng=random.Random(seed))
new_ast = marked_ast.accept(generator)

original_text = marked_ast.accept(printer)
mutated_text = new_ast.accept(printer)

print("=" * 70)
print("CHANGE")
print("=" * 70)
changes = [
    line for line in difflib.unified_diff(
        original_text.splitlines(), mutated_text.splitlines(),
        "original", "mutated", lineterm="", n=0,
    )
    if not line.startswith(("---", "+++", "@@"))
]
if changes:
    print("\n".join(changes))
else:
    print("No visible change: the replacement was identical to the original for this seed.")
    print("Try another seed.")

if not brief:
    print()
    print("=" * 70)
    print("ORIGINAL")
    print("=" * 70)
    print(original_text)

    print("=" * 70)
    print("MUTATED")
    print("=" * 70)
    print(mutated_text)