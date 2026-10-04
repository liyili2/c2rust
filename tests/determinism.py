import os
import random
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
"""
trace_determinism.py — logs every RNG draw made during RustReplacementOperator.create(),
for two independent parses with the same seed, and reports exactly where they diverge.

Usage: python trace_determinism.py [path/to/avl.rs]
"""

from antlr4 import CommonTokenStream, InputStream
from rust.parser.RustLexer import RustLexer
from rust.parser.RustParser import RustParser
from rust.commons.RustASTTransformer import RustASTTransformer
from rust.visitors.MarkingVisitor import MarkingVisitor
from rust.modification.ModificationPointSelector import ModificationPointSelector
from rust.visitors.RandomCandidateReplacementGenerator import RandomCandidateReplacementGenerator
from rust.visitors.ast_compare import ast_equal

FILE_PATH = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "Benchmarks", "avl", "avl.rs"
)
SEED = 42


def parse(path):
    with open(path, "r", encoding="utf-8") as f:
        src = f.read()
    lexer = RustLexer(InputStream(src))
    parser = RustParser(CommonTokenStream(lexer))
    return RustASTTransformer().visit(parser.program())


def describe(node):
    """Identify a node WITHOUT using the printer (which has open bugs)."""
    t = type(node).__name__
    if hasattr(node, "name"):
        try:
            return f"{t}(name={node.name()!r})"
        except Exception:
            pass
    if hasattr(node, "op"):
        try:
            return f"{t}(op={node.op()!r})"
        except Exception:
            pass
    return t


class TracingRNG:
    """Wraps a random.Random, logging every call that consumes randomness."""
    def __init__(self, seed, label, log):
        self._rng = random.Random(seed)
        self._label = label
        self._log = log

    def choice(self, seq):
        result = self._rng.choice(seq)
        self._log.append((self._label, "choice", len(seq), describe(result) if hasattr(result, "accept") else repr(result)))
        return result

    def sample(self, population, k):
        result = self._rng.sample(population, k)
        self._log.append((self._label, "sample", len(population), k))
        return result

    def random(self):
        result = self._rng.random()
        self._log.append((self._label, "random", None, round(result, 6)))
        return result

    def randrange(self, *args):
        result = self._rng.randrange(*args)
        self._log.append((self._label, "randrange", args, result))
        return result


def run(label, log):
    root = parse(FILE_PATH)
    rng = TracingRNG(SEED, label, log)

    marked_root = root.accept(MarkingVisitor())
    selector = ModificationPointSelector(rng=rng)
    point = selector.select(marked_root)
    log.append((label, "SELECTED", None, describe(point.node)))

    generator = RandomCandidateReplacementGenerator(point, rng=rng)
    marked_root.accept(generator)
    candidate = generator.replacement()
    log.append((label, "CANDIDATE", None, describe(candidate)))

    return root, candidate, point.node


def dump(node, indent=0, seen=None):
    """Full recursive field dump of a node, excluding uid, for direct comparison."""
    if seen is None:
        seen = set()
    pad = "  " * indent
    if node is None or isinstance(node, (str, int, float, bool)):
        return f"{pad}{node!r}\n"
    if isinstance(node, list):
        out = f"{pad}[list len={len(node)}]\n"
        for item in node:
            out += dump(item, indent + 1, seen)
        return out
    if id(node) in seen:
        return f"{pad}<cycle {type(node).__name__}>\n"
    if hasattr(node, "__dict__"):
        seen = seen | {id(node)}
        out = f"{pad}{type(node).__name__}\n"
        for k, v in sorted(node.__dict__.items()):
            if k == "uid":
                continue
            out += f"{pad}  .{k} =\n"
            out += dump(v, indent + 2, seen)
        return out
    return f"{pad}{node!r}\n"


log = []
root_a, candidate_a, selected_a = run("run1", log)
root_b, candidate_b, selected_b = run("run2", log)

log_a = [entry for entry in log if entry[0] == "run1"]
log_b = [entry for entry in log if entry[0] == "run2"]

print(f"run1: {len(log_a)} logged operations")
print(f"run2: {len(log_b)} logged operations\n")

diverged = False
for i, (a, b) in enumerate(zip(log_a, log_b)):
    _, kind_a, arg_a, val_a = a
    _, kind_b, arg_b, val_b = b
    match = (kind_a == kind_b and arg_a == arg_b and val_a == val_b)
    marker = "" if match else "  <<< DIVERGES HERE"
    print(f"[{i}] run1: {kind_a} arg={arg_a} -> {val_a}")
    print(f"    run2: {kind_b} arg={arg_b} -> {val_b}{marker}")
    if not match:
        diverged = True
        break

if not diverged and len(log_a) != len(log_b):
    print(f"\n>>> Logs matched up to the shorter length, but counts differ "
          f"({len(log_a)} vs {len(log_b)}) - one run retried more times than the other.")
elif not diverged:
    print("\n>>> Every logged RNG operation matched. Checking final candidates directly...")
    same = ast_equal(candidate_a, candidate_b)
    print(f">>> Final candidates structurally equal: {same}")
    if not same:
        print(">>> RNG draws matched exactly but the RESULT differs - the two selected/generated")
        print(">>> nodes must carry different field VALUES despite matching draw sequence.")
        print(f">>> run1 selected: {describe(selected_a)}   run1 candidate: {describe(candidate_a)}")
        print(f">>> run2 selected: {describe(selected_b)}   run2 candidate: {describe(candidate_b)}")
        print("\n=== run1 candidate, full field dump ===")
        print(dump(candidate_a))
        print("=== run2 candidate, full field dump ===")
        print(dump(candidate_b))
