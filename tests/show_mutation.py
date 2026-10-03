"""
show_mutation.py - print what a RustReplacementOperator mutation actually did,
without RustASTPrinter.

Usage: python show_mutation.py [path/to/avl.rs] [--seed N] [--seeds N]
  --seed N   show one seed in detail
  --seeds N  one-line summary for seeds 0..N-1
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
from repair.pyggi.tree.rust_operators import RustOperator, RustReplacementOperator

DEFAULT_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "..", "Benchmarks", "avl", "avl.rs")
ap = argparse.ArgumentParser()
ap.add_argument("file", nargs="?", default=DEFAULT_FILE)
ap.add_argument("--seed", type=int, default=0)
ap.add_argument("--seeds", type=int, default=0)
args = ap.parse_args()

IGNORED_KEYS = {"uid"}
PRIMS = (str, int, float, bool, type(None))


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


def short(x):
    x = unwrap(x)
    return repr(x)[:60] if isinstance(x, PRIMS) else type(x).__name__


def diffs(a, b, path="root", out=None, seen=None):
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


def dump(x, depth=0):
    """Compact one-line dump with all field values (None fields and uid omitted)."""
    x = unwrap(x)
    if depth > 12:
        return "..."
    if isinstance(x, PRIMS):
        return repr(x)
    if isinstance(x, (list, tuple)):
        return "[" + ", ".join(dump(i, depth + 1) for i in x) + "]"
    if isinstance(x, CloneableASTNode):
        parts = []
        for k, v in vars(x).items():
            if k in IGNORED_KEYS or v is None:
                continue
            name = k.lstrip("_")
            parts.append(f"{name}={type(unwrap(v)).__name__ if k == '_dtype' else dump(v, depth + 1)}")
        return f"{type(x).__name__}({', '.join(parts)})"
    return type(x).__name__ + ":" + repr(x)[:40]


def run(seed):
    """Returns (edit, point_node_before, baseline, after_stripped)."""
    o = parse(args.file)
    baseline = strip_marks(o.accept(MarkingVisitor()))
    edit = RustReplacementOperator.create(FakeProgram(o), target_file="avl.rs", rng=random.Random(seed))
    if edit.modification_point_id is None:
        return edit, None, baseline, None
    point = RustOperator._find_by_id(o.accept(MarkingVisitor()), edit.modification_point_id)
    nc = {"avl.rs": copy.deepcopy(o)}
    ok = edit.apply(FakeProgram(o), nc, {})
    after = strip_marks(nc["avl.rs"]) if ok else None
    return edit, (point.node if point else None), baseline, after


if args.seeds:
    for s in range(args.seeds):
        edit, before, baseline, after = run(s)
        if before is None or after is None:
            print(f"seed {s:3d}: no edit / apply failed")
            continue
        print(f"seed {s:3d}: {type(unwrap(before)).__name__:22s} -> {type(unwrap(edit.target)).__name__:22s} "
              f"| {dump(before)[:60]}  ->  {dump(edit.target)[:60]}")
else:
    edit, before, baseline, after = run(args.seed)
    print(f"seed {args.seed}: modification_point_id = {edit.modification_point_id}")
    if before is None or after is None:
        print("no edit was created or apply failed")
        sys.exit(1)
    print("\nORIGINAL node :", dump(before))
    print("REPLACEMENT   :", dump(edit.target))
    print("\nchanged sites vs. unmutated (rebuilt) baseline:")
    for p, x, y in diffs(baseline, after):
        print(f"  {p}\n      {x}  ->  {y}")
