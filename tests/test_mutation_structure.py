"""
test_mutation_structure.py - checks, WITHOUT the printer, whether the operator
pipeline really changes the tree.

Two traps this test avoids:
  1. apply() returns a tree still wrapped in MarkedASTNode, so the naive
     `not ast_equal(orig, after)` is true even when nothing was mutated.
     -> wrappers are stripped from both sides before comparing.
  2. Marking rebuilds the tree through RustASTGenerator, and that rebuild may
     not be faithful (e.g. visitLiteral turning IntLiteral into Literal).
     That noise would show up as "changes" in every mutant.
     -> layer 0 measures the rebuild noise on its own, and layers 1-2 compare
        against a REBUILT BASELINE (strip(mark(orig))), so only the operator's
        change is counted.

Layers:
  0. controls: rebuild fidelity, naive-ast_equal false positive, manual splice
  1. create(): None / no-op / real candidates
  2. apply(): number and location of changed sites vs. the baseline
  3. determinism and no in-place modification of the original

Usage: python test_mutation_structure.py [path/to/avl.rs] [--seeds N]
"""
import argparse
import copy
import os
import random
import sys
from collections import Counter

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from antlr4 import CommonTokenStream, InputStream
from rust.parser.RustLexer import RustLexer
from rust.parser.RustParser import RustParser
from rust.commons.RustASTTransformer import RustASTTransformer
from rust.nodes.ASTNode import CloneableASTNode
from rust.nodes.MarkedASTNode import MarkedASTNode
from rust.visitors.MarkingVisitor import MarkingVisitor
from rust.visitors.ast_compare import ast_equal as naive_ast_equal
from rust.modification.ModificationPointSelector import ModificationPointSelector
from repair.pyggi.tree.rust_operators import RustOperator, RustReplacementOperator
from rust.visitors.MarkedNodeTargetUpdater import MarkedNodeTargetUpdater  # adjust path if needed

DEFAULT_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "..", "Benchmarks", "avl", "avl.rs")
ap = argparse.ArgumentParser()
ap.add_argument("file", nargs="?", default=DEFAULT_FILE)
ap.add_argument("--seeds", type=int, default=30)
args = ap.parse_args()
FILE_PATH, NUM_SEEDS = args.file, args.seeds

IGNORED_KEYS = {"uid"}   # add parent/back-pointer attribute names here if you have any
PRIMS = (str, int, float, bool, type(None))


# ----------------------------------------------------------------- helpers
def parse(path):
    with open(path, "r", encoding="utf-8") as f:
        src = f.read()
    return RustASTTransformer().visit(RustParser(CommonTokenStream(RustLexer(InputStream(src)))).program())


class FakeProgram:
    def __init__(self, root):
        self.contents = {"avl.rs": root}

    def random_file(self):
        return "avl.rs"


def unwrap(x):
    while isinstance(x, MarkedASTNode):
        x = x.node
    return x


def strip_marks(x, memo=None):
    """Deep copy of x with every MarkedASTNode wrapper removed."""
    memo = {} if memo is None else memo
    x = unwrap(x)
    if isinstance(x, list):
        return [strip_marks(i, memo) for i in x]
    if isinstance(x, tuple):
        return tuple(strip_marks(i, memo) for i in x)
    if isinstance(x, CloneableASTNode):
        if id(x) in memo:
            return memo[id(x)]
        new = copy.copy(x)
        memo[id(x)] = new
        for k, v in list(vars(x).items()):
            new.__dict__[k] = strip_marks(v, memo)
        return new
    return x


def count_marks(x, seen=None):
    """Number of MarkedASTNode wrappers left in a tree."""
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


def short(x):
    x = unwrap(x)
    return repr(x)[:60] if isinstance(x, PRIMS) else type(x).__name__


def diffs(a, b, path="root", out=None, seen=None):
    """Minimal differing sites (path, before, after); wrappers and uid ignored."""
    out = [] if out is None else out
    seen = set() if seen is None else seen
    a, b = unwrap(a), unwrap(b)
    if a is b:
        return out
    if type(a) is not type(b):
        out.append((path, short(a), short(b)))
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
        for k in sorted((set(vars(a)) | set(vars(b))) - IGNORED_KEYS):
            diffs(vars(a).get(k), vars(b).get(k), f"{path}.{k}", out, seen)
        return out
    if a != b:
        out.append((path, repr(a)[:60], repr(b)[:60]))
    return out


failures = 0


def check(cond, msg):
    global failures
    print(("  PASS  " if cond else "  FAIL  ") + msg)
    if not cond:
        failures += 1
    return cond


# ------------------------------------------------ layer 0: controls
print("0. controls (validate the checker, the rebuild and the updater)")
orig = parse(FILE_PATH)
orig_snapshot = copy.deepcopy(orig)
marked = orig.accept(MarkingVisitor())
baseline = strip_marks(marked)          # rebuilt, unmutated reference

noise = diffs(orig, baseline)
check(not noise, f"rebuild is faithful: strip(mark(tree)) == tree ({len(noise)} site(s) differ)")
if noise:
    kinds = Counter((b, a) for _, b, a in noise)
    print("        rebuild noise by (before -> after):")
    for (b, a), n in kinds.most_common():
        print(f"          {n:3d} x  {a}  ->  {b}")
    print("        (later layers compare against the rebuilt baseline, so they stay meaningful)")

check(not naive_ast_equal(orig, marked),
      "naive ast_equal(tree, mark(tree)) is False  <- the false positive in the old tests")

pts = ModificationPointSelector().eligible_points(marked)
a_pt = pts[len(pts) // 2]
b_pt = next(p for p in pts if type(unwrap(p.node)) is not type(unwrap(a_pt.node)))
spliced = marked.accept(MarkedNodeTargetUpdater(a_pt.get_id(), copy.deepcopy(b_pt.node)))
d = diffs(baseline, spliced)
check(len(d) == 1, f"manual splice of a different node type is exactly 1 site vs baseline (got {len(d)})")
for p, x, y in d[:3]:
    print(f"        {p}: {x}  ->  {y}")

# ------------------------------------------------ layer 1: create()
print(f"\n1. create() over {NUM_SEEDS} seeds")
stats = Counter()
for seed in range(NUM_SEEDS):
    o = parse(FILE_PATH)
    edit = RustReplacementOperator.create(FakeProgram(o), target_file="avl.rs", rng=random.Random(seed))
    if edit.modification_point_id is None:
        stats["id_none"] += 1
        continue
    if edit.target is None:
        stats["candidate_none"] += 1
        continue
    point = RustOperator._find_by_id(o.accept(MarkingVisitor()), edit.modification_point_id)
    if point is None:
        stats["id_not_found"] += 1
        continue
    stats["noop_candidate" if not diffs(point.node, edit.target) else "real_candidate"] += 1
print("   ", dict(stats))
check(stats["real_candidate"] > 0, "at least one seed produced a structurally different candidate")
bad = stats["id_none"] + stats["candidate_none"] + stats["noop_candidate"] + stats["id_not_found"]
check(bad == 0, f"no seed produced a None / no-op / unfindable candidate ({bad} did)")

# ------------------------------------------------ layer 2: apply()
print(f"\n2. apply() over {NUM_SEEDS} seeds (marks stripped, compared to rebuilt baseline)")
site_counts, first_paths = Counter(), Counter()
n_failed = 0
marks_left = 0
for seed in range(NUM_SEEDS):
    o = parse(FILE_PATH)
    edit = RustReplacementOperator.create(FakeProgram(o), target_file="avl.rs", rng=random.Random(seed))
    if edit.modification_point_id is None:
        continue
    new_contents = {"avl.rs": copy.deepcopy(o)}
    if not edit.apply(FakeProgram(o), new_contents, {}):
        n_failed += 1
        print(f"   seed {seed}: apply() returned False")
        continue
    after = new_contents["avl.rs"]
    marks_left = max(marks_left, count_marks(after))
    d = diffs(baseline, after)
    site_counts[len(d)] += 1
    if d:
        first_paths[d[0][0]] += 1
    if seed < 8:
        if d:
            print(f"   seed {seed}: {len(d)} site(s); first: {d[0][0]}: {d[0][1]}  ->  {d[0][2]}")
        else:
            print(f"   seed {seed}: apply() succeeded but tree equals the baseline (NO-OP)")

print("    sites changed per edit (sites: count):", dict(sorted(site_counts.items())))
print(f"    distinct first-change locations: {len(first_paths)}")
print(f"    MarkedASTNode wrappers still present after apply(): {marks_left}")
check(n_failed == 0, f"apply() never returned False ({n_failed} failures)")
check(site_counts[0] == 0, f"no applied edit left the tree equal to the baseline ({site_counts[0]} no-ops)")
if NUM_SEEDS >= 5:
    check(len(first_paths) > 1, "mutations land in different places across seeds")

# ------------------------------------------------ layer 3: determinism / purity
print("\n3. determinism and purity")


def run(seed):
    o = parse(FILE_PATH)
    e = RustReplacementOperator.create(FakeProgram(o), target_file="avl.rs", rng=random.Random(seed))
    nc = {"avl.rs": copy.deepcopy(o)}
    e.apply(FakeProgram(o), nc, {})
    return nc["avl.rs"]


check(not diffs(run(7), run(7)), "same seed -> structurally identical mutant from a fresh parse")
check(bool(diffs(run(1), run(2))) or True, "different seeds run without error")
check(not diffs(orig_snapshot, orig), "original tree object was not modified in place")

print("\nInterpretation:")
print(" - rebuild noise FAIL      -> a visitX in RustASTGenerator is not faithful (e.g. visitLiteral);")
print("                              fix it, every mutant is currently altered beyond the operator's edit")
print(" - layer 1 no-ops          -> generator / ast_equal filter in create()")
print(" - layer 2 no-ops          -> apply()/updater lose the change")
print(" - layers 1-3 pass         -> the operator mutates; identical dumps came from the printer")
print("\n" + ("ALL CHECKS PASSED" if failures == 0 else f"{failures} CHECK(S) FAILED"))
sys.exit(1 if failures else 0)
