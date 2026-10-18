# run it this way: python demo_test.py the_rust_file_path seed_number

import sys
import os
import random
import difflib

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from repair.framework.cprogram import CProgram
from repair.framework.operators import (
    RustOperator, RustReplacementOperator, RustSwapOperator, strip_marks_tree)
from rust.visitors.Printers import RustASTPrinter
from rust.visitors.MarkingVisitor import MarkingVisitor
from rust.nodes.TopLevel import FunctionDefinition
from rust.modification.Constraint import Constraint, ConstraintChecker
from rust.modification.ModificationPointSelector import ModificationPointSelector
from rust.modification.ProgramInventory import ProgramInventory
from rust.visitors.RandomCandidateReplacementGenerator import RandomCandidateReplacementGenerator


if len(sys.argv) < 2:
    sys.exit("Usage: python demo_test.py path/to/file.rs [seed]")
rust_file = os.path.abspath(sys.argv[1])
if not os.path.isfile(rust_file):
    sys.exit(f"File not found: {rust_file}")
seed = int(sys.argv[2]) if len(sys.argv) > 2 else random.randrange(2 ** 32)
print(f"file = {rust_file}")
print(f"seed = {seed}")

# CProgram (config given -> Rust/AST mode) takes the project folder plus the file name
PROJECT_PATH = os.path.dirname(rust_file)
FILE = os.path.basename(rust_file)
program = CProgram(PROJECT_PATH, config={"test_command": "true", "target_files": [FILE]})

printer = RustASTPrinter()
original = program.contents[FILE]
before_text = original.accept(printer)
print("Source (before any marking/editing):")
print(before_text)

# All constraints are set here, BEFORE any operator runs.
# Eligibility: any marked expression, but only inside unsafe functions.
unsafe_functions = ConstraintChecker([
    Constraint(FunctionDefinition, "is_unsafe", True),
])

marked = original.accept(MarkingVisitor())
selector = ModificationPointSelector(scope_checker=unsafe_functions, rng=random.Random(seed))
points = selector.eligible_points(marked)
print(f"\nEligible modification points (inside unsafe functions): {len(points)}")
for p in points:
    print("  ", type(p.node).__name__, strip_marks_tree(p.node).accept(printer))
if not points:
    print("Nothing eligible - nothing to edit.")
    sys.exit(1)

# Target selection now lives on the program (the Rust counterpart of app_target)
print("\n" + "=" * 50)
print("CProgram.swap_target / replace_target")
print("=" * 50)
_, a_id, b_id = program.swap_target(FILE, scope_checker=unsafe_functions, rng=random.Random(seed))
print("swap_target    :", a_id, "<->", b_id)
_, r_id, cand = program.replace_target(FILE, scope_checker=unsafe_functions, rng=random.Random(seed))
print("replace_target :", r_id, "->", None if cand is None else strip_marks_tree(cand).accept(printer))

# The operators' create() call those same program methods.
for operator in (RustReplacementOperator, RustSwapOperator):
    print("\n" + "=" * 50)
    print(operator.__name__)
    print("=" * 50)

    edit = operator.create(program, target_file=FILE,
                           scope_checker=unsafe_functions, rng=random.Random(seed))
    if edit.modification_point_id is None:
        print("No mutation created.")
        continue

    new_contents = dict(program.contents)
    if not edit.apply(program, new_contents, program.modification_points):
        print("apply() returned False.")
        continue
    after_text = strip_marks_tree(new_contents[FILE]).accept(printer)   # drop <marked> wrappers

    print("--- before ---")
    print(before_text)
    print("--- after ---")
    print(after_text)

    print("--- summary ---")
    chosen = RustOperator._find_by_id(marked, edit.modification_point_id).node
    before = strip_marks_tree(chosen).accept(printer)
    if operator is RustSwapOperator:
        other = RustOperator._find_by_id(marked, edit.point_b_id).node
        print("Swapped:", before, " <-> ", strip_marks_tree(other).accept(printer))
    else:
        print("Node   :", type(chosen).__name__)
        print("Before :", before)
        print("After  :", strip_marks_tree(edit.target).accept(printer))
    for line in difflib.unified_diff(before_text.splitlines(), after_text.splitlines(),
                                     "before", "after", lineterm="", n=0):
        print(line)


# ---------------------------------------------------------------------------
# Direct check of the replacement generator (uses ProgramInventory):
# shows the selected node and the candidate chosen for it.
# Independent of RustReplacementOperator, so it works before rust_operators.py passes `inventory=`.
# ---------------------------------------------------------------------------
print("\n" + "=" * 50)
print("RandomCandidateReplacementGenerator (direct)")
print("=" * 50)

inventory = ProgramInventory(original)
print("Program inventory:", inventory.summary())

selected = ModificationPointSelector(scope_checker=unsafe_functions, rng=random.Random(seed)).select(marked)
generator = RandomCandidateReplacementGenerator(selected, rng=random.Random(seed), inventory=inventory)
new_marked = marked.accept(generator)

selected_text = strip_marks_tree(selected.node).accept(printer)
candidate_text = strip_marks_tree(generator.replacement()).accept(printer)

print("Selected node :", type(selected.node).__name__)
print("To replace    :", selected_text)
print("Candidate     :", type(generator.replacement()).__name__)
print("Replacement   :", candidate_text)
if candidate_text == selected_text:
    print("(no visible change: no-op for this node/seed, e.g. a function call or a single-name scope)")

direct_after = strip_marks_tree(new_marked).accept(printer)
for line in difflib.unified_diff(before_text.splitlines(), direct_after.splitlines(),
                                 "before", "after", lineterm="", n=0):
    print(line)
