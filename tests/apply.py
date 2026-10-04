"""
test_apply.py — simple end-to-end check: load avl.rs through PyGGI, create one
replacement edit, call apply(), and show that the mutation actually happened.
"""
import os
import sys
import random
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from repair.pyggi.tree.tree import TreeProgram
from repair.pyggi.tree.rust_operators import RustReplacementOperator
from rust.visitors.Printers import RustASTPrinter
from rust.visitors.ast_compare import ast_equal

PROJECT_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "Benchmarks", "avl"
)
config = {"test_command": "true", "target_files": ["avl.rs"]}

# --- load the file through the real PyGGI plug (TreeProgram -> RustEngine) ---
program = TreeProgram(PROJECT_PATH, config=config)

# --- create() : mark, select, generate a candidate, store the edit ---
edit = RustReplacementOperator.create(program, target_file="avl.rs", rng=random.Random(1))
assert edit.modification_point_id is not None, "no non-trivial edit found"

# --- apply() : re-mark, find the point, swap it in ---
new_contents = dict(program.contents)
success = edit.apply(program, new_contents, program.modification_points)
assert success, "apply() failed"

# --- proof it actually changed something ---
changed = not ast_equal(program.contents["avl.rs"], new_contents["avl.rs"])
print(f"Mutation applied: {changed}")

# --- readable before/after (Printers.py has known open bugs - for eyeballing only) ---
printer = RustASTPrinter()
print("\n=== BEFORE ===")
print(program.contents["avl.rs"].accept(printer))
print("\n=== AFTER ===")
print(new_contents["avl.rs"].accept(printer))
