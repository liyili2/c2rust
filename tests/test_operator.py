"""test_rust_replacement.py — verifies the AST replacement operator end to end."""
import random

from repair.pyggi.tree.tree import TreeProgram
from repair.pyggi.tree.rust_operators import RustReplacementOperator

PROJECT_PATH = "../Benchmarks/avl"  # directory containing avl.rs

config = {
    "test_command": "true",   # unused here, but AbstractProgram.load_config needs a key
    "target_files": ["avl.rs"],
}

program = TreeProgram(PROJECT_PATH, config=config)

seed = 42
edit = RustReplacementOperator.create(program, target_file="avl.rs", rng=random.Random(seed))

assert edit.modification_point_id is not None, "no eligible modification point found"

new_contents = dict(program.contents)  # shallow copy: only avl.rs's root will be replaced
success = edit.apply(program, new_contents, program.modification_points)
assert success, "edit failed to apply"

before = program.dump(program.contents, "avl.rs")
after = program.dump(new_contents, "avl.rs")

print("=== BEFORE ===")
print(before)
print("\n=== AFTER ===")
print(after)

assert before != after, "mutated source is identical to the original"

# Determinism: same seed -> same candidate -> same result, from a fresh parse.
program2 = TreeProgram(PROJECT_PATH, config=config)
edit2 = RustReplacementOperator.create(program2, target_file="avl.rs", rng=random.Random(seed))
new_contents2 = dict(program2.contents)
edit2.apply(program2, new_contents2, program2.modification_points)
after2 = program2.dump(new_contents2, "avl.rs")

assert after == after2, "same seed produced different mutations across runs"
print("\nOK: mutation applied, is non-trivial, and is reproducible under a fixed seed.")

