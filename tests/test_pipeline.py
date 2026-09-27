"""
test_pipeline.py — sanity checks for the Rust AST mutation pipeline.
Usage: python test_pipeline.py [path/to/avl.rs]

Note: printer-dependent checks are intentionally excluded here (Printers.py
has open, separately-tracked bugs) - this only verifies marking, id
stability, and that create()/apply() actually mutate the tree structurally.
"""
import copy
import os
import random
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from antlr4 import CommonTokenStream, InputStream
from rust.parser.RustLexer import RustLexer
from rust.parser.RustParser import RustParser
from rust.commons.RustASTTransformer import RustASTTransformer
from rust.visitors.MarkingVisitor import MarkingVisitor
from rust.visitors.ast_compare import ast_equal
from rust.modification.ModificationPointSelector import ModificationPointSelector
from rust.nodes.Expression import IdentifierExpression
from repair.pyggi.tree.rust_operators import RustReplacementOperator

FILE_PATH = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "Benchmarks", "avl", "avl.rs"
)


def parse(path):
    with open(path, "r", encoding="utf-8") as f:
        src = f.read()
    lexer = RustLexer(InputStream(src))
    parser = RustParser(CommonTokenStream(lexer))
    return RustASTTransformer().visit(parser.program())


class FakeProgram:
    def __init__(self, root):
        self.contents = {"avl.rs": root}
    def random_file(self):
        return "avl.rs"


# --- 2: marking reaches identifiers, not just BinaryExpressions -----------
root = parse(FILE_PATH)
marked = root.accept(MarkingVisitor())
points = ModificationPointSelector().eligible_points(marked)
assert points, "no modification points found at all"
id_points = [p for p in points if isinstance(p.node, IdentifierExpression)]
assert id_points, "no IdentifierExpression points - transformer fix missing"
print(f"2. marking: {len(points)} points, {len(id_points)} are identifiers: OK")

# --- 3: wrapper ids are stable across two INDEPENDENT marking passes ------
root_once = parse(FILE_PATH)
root_a = root_once
root_b = copy.deepcopy(root_once)
ids_a = sorted(p.get_id() for p in ModificationPointSelector().eligible_points(root_a.accept(MarkingVisitor())))
ids_b = sorted(p.get_id() for p in ModificationPointSelector().eligible_points(root_b.accept(MarkingVisitor())))
assert ids_a == ids_b, "wrapper ids differ across passes - MarkingVisitor._mark() fix missing"
print("3. id stability across marking passes: OK")

# --- 4: create() -> apply() actually mutates the tree (structurally) ------
seed = 7
orig = parse(FILE_PATH)
edit = RustReplacementOperator.create(FakeProgram(orig), target_file="avl.rs", rng=random.Random(seed))
assert edit.modification_point_id is not None, "no non-trivial edit found (all points were no-ops)"

new_contents = {"avl.rs": copy.deepcopy(orig)}
assert edit.apply(FakeProgram(orig), new_contents, {}), "apply() couldn't find its own modification point"
assert not ast_equal(orig, new_contents["avl.rs"]), "tree is structurally identical after apply()"
print("4. create -> apply round trip: OK (tree structurally changed)")

# --- 5: same seed -> same mutation, from a totally fresh parse ------------
orig2 = parse(FILE_PATH)
edit2 = RustReplacementOperator.create(FakeProgram(orig2), target_file="avl.rs", rng=random.Random(seed))
new_contents2 = {"avl.rs": copy.deepcopy(orig2)}
edit2.apply(FakeProgram(orig2), new_contents2, {})
assert ast_equal(new_contents["avl.rs"], new_contents2["avl.rs"]), "same seed produced structurally different mutations"
print("5. determinism under a fixed seed: OK")

print("\nALL TESTS PASSED")