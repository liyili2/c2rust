import sys
import os
import random

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


# Usage:  python testing.py [seed]
# No seed -> a random one (printed, so any run can be reproduced).
seed = int(sys.argv[1]) if len(sys.argv) > 1 else random.randrange(2 ** 32)
print(f"seed = {seed}")

file_path = "./avl/avl.rs"


with open(file_path, "r", encoding="utf-8") as f:
    rust_code = f.read()

print("Tokenizing:")
lexer = RustLexer(InputStream(rust_code))
abc = CommonTokenStream(lexer)
print("Parsing:")
parser = RustParser(abc)
tree = parser.program()
print("Transforming:")
transformer = RustASTTransformer()
ast = transformer.visit(tree)

printer = RustASTPrinter()

print("Reassembled source (before any marking/editing):")
reassmbled_source = ast.accept(printer)
print(reassmbled_source)

# --- Architecture: mark -> select -> generate (one visitor) ---

print("\nMarking modification points:")
marked_ast = ast.accept(MarkingVisitor())

# Eligibility: any marked expression, but only inside unsafe functions.
# Adjust/add Constraint(...) entries here as needed - see rust.modification.Constraint.
unsafe_functions = ConstraintChecker([
    Constraint(FunctionDefinition, "is_unsafe", True),
])

print("Selecting one eligible modification point:")
selector = ModificationPointSelector(scope_checker=unsafe_functions, rng=random.Random(seed))
print(f"Eligible modification points: {len(selector.eligible_points(marked_ast))}")
selected = selector.select(marked_ast)

if selected is None:
    print("No eligible modification points found - nothing to edit.")
else:
    print("Selected point:", selected.node.accept(printer))

    # The single mutation visitor: it walks the marked AST, keeps track of the
    # variables in scope, and rebuilds the AST with the selected node replaced.
    generator = RandomCandidateReplacementGenerator(selected, rng=random.Random(seed))
    new_ast = marked_ast.accept(generator)

    print("\n=== ORIGINAL (marked) ===")
    print(marked_ast.accept(printer))

    print("\n=== MUTATED ===")
    print(new_ast.accept(printer))


# --- Mutation summary (kept at the very end of the output) ---

print("\n=== MUTATION SUMMARY ===")
if selected is None:
    print("No mutation applied (no eligible modification point).")
else:
    chosen = selected.node
    before = chosen.accept(printer)
    after_node = generator.replacement()
    after = after_node.accept(printer) if after_node is not None else None

    print("Chosen node :", type(chosen).__name__)
    print("Before      :", before)
    if after is None:
        print("After       : (the visitor never reached the selected node)")
    else:
        print("After       :", after)
        if after == before:
            print("              (no visible change: the replacement prints the same as the original)")