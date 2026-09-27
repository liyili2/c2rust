"""
test_pipeline.py — sanity checks for the Rust AST mutation pipeline.
Usage: python test_pipeline.py [path/to/avl.rs]
"""
import copy
import random
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from antlr4 import CommonTokenStream, InputStream
from rust.parser.RustLexer import RustLexer
from rust.parser.RustParser import RustParser
from rust.commons.RustASTTransformer import RustASTTransformer
from rust.visitors.Printers import RustASTPrinter
from rust.visitors.MarkingVisitor import MarkingVisitor
from rust.modification.ModificationPointSelector import ModificationPointSelector
from rust.nodes.Expression import IdentifierExpression
from repair.pyggi.tree.rust_operators import RustReplacementOperator

FILE_PATH = sys.argv[1] if len(sys.argv) > 1 else "./avl/avl.rs"
printer = RustASTPrinter()


def parse(path):
    with open(path, "r", encoding="utf-8") as f:
        src = f.read()
    lexer = RustLexer(InputStream(src))
    parser = RustParser(CommonTokenStream(lexer))
    return RustASTTransformer().visit(parser.program())


def check_clean(label, src):
    """Fails loudly with context instead of a bare AssertionError."""
    ok = True
    if "<marked>" in src:
        i = src.index("<marked>")
        print(f"[{label}] FOUND '<marked>' near:", repr(src[max(0, i-40):i+60]))
        ok = False
    if ": None" in src:
        i = src.index(": None")
        print(f"[{label}] FOUND ': None' near:", repr(src[max(0, i-40):i+20]))
        ok = False
    assert ok, f"{label}: dumped source is not clean (see above)"


class FakeProgram:
    """Stands in for AbstractProgram - just enough for create()/apply() to run."""
    def __init__(self, root):
        self.contents = {"avl.rs": root}
    def random_file(self):
        return "avl.rs"


# --- 1: parse/print round trip is clean -----------------------------------
root = parse(FILE_PATH)
src = root.accept(printer)
check_clean("1. parse/print", src)
print("1. parse/print round trip: OK")

# --- 2: marking reaches identifiers, not just BinaryExpressions -----------
marked = root.accept(MarkingVisitor())
points = ModificationPointSelector().eligible_points(marked)
assert points, "no modification points found at all"
id_points = [p for p in points if isinstance(p.node, IdentifierExpression)]
assert id_points, "no IdentifierExpression points - transformer fix missing"
print(f"2. marking: {len(points)} points, {len(id_points)} are identifiers: OK")

# --- 3: wrapper ids are stable across two INDEPENDENT marking passes ------
root_once = parse(FILE_PATH)
root_a = root_once
root_b = copy.deepcopy(root_once)   # same lineage, NOT a second parse

ids_a = sorted(p.get_id() for p in ModificationPointSelector().eligible_points(root_a.accept(MarkingVisitor())))
ids_b = sorted(p.get_id() for p in ModificationPointSelector().eligible_points(root_b.accept(MarkingVisitor())))
assert ids_a == ids_b, "wrapper ids differ across passes - MarkingVisitor._mark() fix missing"
print("3. id stability across marking passes: OK")

# --- 4: create() -> apply() actually mutates the tree ----------------------
seed = 7
orig = parse(FILE_PATH)
edit = RustReplacementOperator.create(FakeProgram(orig), target_file="avl.rs", rng=random.Random(seed))
assert edit.modification_point_id is not None

new_contents = {"avl.rs": copy.deepcopy(orig)}
assert edit.apply(FakeProgram(orig), new_contents, {}), "apply() couldn't find its own modification point"

before, after = orig.accept(printer), new_contents["avl.rs"].accept(printer)
assert before != after
check_clean("4. after mutation", after)
print("4. create -> apply round trip: OK (source changed, output is clean)")

# --- 5: same seed -> same mutation, from a totally fresh parse ------------
orig2 = parse(FILE_PATH)
edit2 = RustReplacementOperator.create(FakeProgram(orig2), target_file="avl.rs", rng=random.Random(seed))
new_contents2 = {"avl.rs": copy.deepcopy(orig2)}
edit2.apply(FakeProgram(orig2), new_contents2, {})
assert new_contents2["avl.rs"].accept(printer) == after
print("5. determinism under a fixed seed: OK")

print("\nALL TESTS PASSED")