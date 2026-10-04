"""
test_swap_operator.py - structural checks for RustSwapOperator (no printer involved).

Per seed it checks that the edit
  1. was created (a valid pair was found) and applies,
  2. changes the tree compared to the rebuilt, unmutated baseline,
  3. leaves no MarkedASTNode wrappers behind,
  4. is an involution: applying the same swap again restores the baseline,
  5. is deterministic for a fixed seed.

Usage: python test_swap_operator.py [path/to/avl.rs] [--seeds N]
"""
import argparse
import copy
import os
import random
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from antlr4 import CommonTokenStream, InputStream
from rust.parser.RustLexer import RustLexer
from rust.parser.RustParser import RustParser
from rust.commons.RustASTTransformer import RustASTTransformer
from rust.nodes.ASTNode import CloneableASTNode
from rust.nodes.MarkedASTNode import MarkedASTNode
from rust.visitors.MarkingVisitor import MarkingVisitor
from repair.pyggi.tree.rust_operators import RustOperator, RustSwapOperator, strip_marks_tree

DEFAULT_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "Benchmarks", "avl", "avl.rs")
ap = argparse.ArgumentParser()
ap.add_argument("file", nargs="?", default=DEFAULT_FILE)
ap.add_argument("--seeds", type=int, default=30)
args = ap.parse_args()


def parse(path):
    with open(path, "r", encoding="utf-8") as f:
        src = f.read()
    return RustASTTransformer().visit(RustParser(CommonTokenStream(RustLexer(InputStream(src)))).program())


class FakeProgram:
    def __init__(self, root):
        self.contents = {"avl.rs": root}

    def random_file(self):
        return "avl.rs"


def diffs(a, b, path="root", out=None, seen=None):
    """Minimal differing sites between two UNWRAPPED trees (uid ignored)."""
    out = [] if out is None else out
    seen = set() if seen is None else seen
    if a is b:
        return out
    if type(a) is not type(b):
        out.append((path, type(a).__name__, type(b).__name__))
        return out
    if isinstance(a, (list, tuple)):
        if len(a) != len(b):
            out.append((path, f"len {len(a)}", f"len {len(b)}"))
            return out
        for i, (x, y) in enumerate(zip(a, b)):
            diffs(x, y, f"{path}[{i}]", out, seen)
        return out
    if isinstance(a, CloneableASTNode):
        key = (id(a), id(b))
        if key in seen:
            return out
        seen.add(key)
        for k in sorted((set(vars(a)) | set(vars(b))) - {"uid"}):
            diffs(vars(a).get(k), vars(b).get(k), f"{path}.{k}", out, seen)
        return out
    if a != b:
        out.append((path, repr(a)[:50], repr(b)[:50]))
    return out


def count_marks(x, seen=None):
    seen = set() if seen is None else seen
    if isinstance(x, MarkedASTNode):
        return 1 + count_marks(x.node, seen)
    if isinstance(x, (list, tuple)):
        return sum(count_marks(i, seen) for i in x)
    if isinstance(x, CloneableASTNode):
        if id(x) in seen:
            return 0
        seen.add(id(x))
        return sum(count_marks(v, seen) for v in vars(x).values())
    return 0


failures = 0


def check(cond, msg):
    global failures
    print(("  PASS  " if cond else "  FAIL  ") + msg)
    if not cond:
        failures += 1


orig = parse(args.file)
baseline = strip_marks_tree(orig.accept(MarkingVisitor()))   # rebuilt, unmutated reference


def run_swap(seed):
    o = parse(args.file)
    edit = RustSwapOperator.create(FakeProgram(o), target_file="avl.rs", rng=random.Random(seed))
    nc = {"avl.rs": copy.deepcopy(o)}
    ok = edit.apply(FakeProgram(o), nc, {})
    return edit, ok, nc, o


print(f"swap operator over {args.seeds} seeds")
no_pair = apply_failed = unchanged = marks = not_involution = 0
for seed in range(args.seeds):
    edit, ok, nc, o = run_swap(seed)
    if edit.modification_point_id is None:
        no_pair += 1
        continue
    if not ok:
        apply_failed += 1
        print(f"   seed {seed}: apply() returned False for {edit}")
        continue
    after = nc["avl.rs"]
    d = diffs(baseline, after)
    if not d:
        unchanged += 1
        print(f"   seed {seed}: swap left the tree equal to the baseline: {edit}")
    marks += count_marks(after)
    # involution: swap the same two ids again
    nc2 = {"avl.rs": after}
    ok2 = edit.apply(None, nc2, {})
    if not ok2 or diffs(baseline, nc2["avl.rs"]):
        not_involution += 1
        print(f"   seed {seed}: applying the same swap twice did not restore the tree ({edit})")
    if seed < 5 and d:
        marked_o = o.accept(MarkingVisitor())   # ids are per-parse: look up in the tree the edit was created from
        a = RustOperator._find_by_id(marked_o, edit.point_a_id)
        b = RustOperator._find_by_id(marked_o, edit.point_b_id)
        print(f"   seed {seed}: swapped {type(a.node).__name__} <-> {type(b.node).__name__}; {len(d)} changed site(s), first {d[0][0]}")

check(no_pair < args.seeds, f"valid pairs found ({args.seeds - no_pair}/{args.seeds} seeds)")
check(apply_failed == 0, f"apply() never returned False ({apply_failed} failures)")
check(unchanged == 0, f"every swap changed the tree ({unchanged} no-ops)")
check(marks == 0, f"no MarkedASTNode wrappers left after apply ({marks} found)")
check(not_involution == 0, f"swapping twice restores the baseline ({not_involution} failures)")

e1, _, n1, _ = run_swap(7)
e2, _, n2, _ = run_swap(7)
check(not diffs(n1["avl.rs"], n2["avl.rs"]), "same seed -> structurally identical mutant from a fresh parse")

print("\n" + ("ALL CHECKS PASSED" if failures == 0 else f"{failures} CHECK(S) FAILED"))
sys.exit(1 if failures else 0)
