import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

"""test_operator.py — verifies the AST replacement operator end to end,
without depending on RustASTPrinter's correctness. Printed BEFORE/AFTER
source is shown for human inspection only and never gates pass/fail."""
import copy
import random

from repair.pyggi.tree.tree import TreeProgram
from repair.pyggi.tree.rust_operators import RustReplacementOperator
from rust.visitors.ast_compare import ast_equal
from rust.visitors.Printers import RustASTPrinter

PROJECT_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "Benchmarks", "avl"
)
config = {"test_command": "true", "target_files": ["avl.rs"]}
printer = RustASTPrinter()


def try_dump(label, root):
    try:
        print(f"=== {label} ===")
        print(root.accept(printer))
    except Exception as e:
        print(f"=== {label} === (could not print: {e})")


program = TreeProgram(PROJECT_PATH, config=config)

seed = 42
edit = RustReplacementOperator.create(program, target_file="avl.rs", rng=random.Random(seed))
assert edit.modification_point_id is not None, "no non-trivial edit found (all points were no-ops)"

new_contents = dict(program.contents)
success = edit.apply(program, new_contents, program.modification_points)
assert success, "edit failed to apply"

try_dump("BEFORE", program.contents["avl.rs"])
try_dump("AFTER", new_contents["avl.rs"])

assert not ast_equal(program.contents["avl.rs"], new_contents["avl.rs"]), \
    "mutated tree is structurally identical to the original"

# Determinism: same seed -> same candidate -> same result, from a fresh parse.
program2 = TreeProgram(PROJECT_PATH, config=config)
edit2 = RustReplacementOperator.create(program2, target_file="avl.rs", rng=random.Random(seed))
new_contents2 = dict(program2.contents)
edit2.apply(program2, new_contents2, program2.modification_points)

assert ast_equal(new_contents["avl.rs"], new_contents2["avl.rs"]), \
    "same seed produced structurally different mutations across runs"

print("\nOK: mutation applied, is structurally non-trivial, and is reproducible under a fixed seed.")