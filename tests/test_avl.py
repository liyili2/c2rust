"""
Integration test: runs the full mark -> select -> generate pipeline against
the real avl.rs benchmark file, using the actual ANTLR parser/transformer -
not a hand-built synthetic AST like the unit tests in
test_random_candidate_replacement_generator.py.

This is deliberately separate from the unit test file: it depends on
external resources (the generated parser, the .rs file on disk) that may
not exist in every environment, so it skips cleanly instead of failing
when they're missing.
"""

import sys
import os
import random

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest

antlr4 = pytest.importorskip("antlr4", reason="antlr4 runtime not installed")

try:
    from rust.parser.RustLexer import RustLexer
    from rust.parser.RustParser import RustParser
    from rust.commons.RustASTTransformer import RustASTTransformer
    _PARSER_AVAILABLE = True
except ImportError:
    _PARSER_AVAILABLE = False

from rust.visitors.Printers import RustASTPrinter
from rust.visitors.MarkingVisitor import MarkingVisitor
from rust.visitors.NodeCollector import NodeCollector
from rust.visitors.RandomCandidateReplacementGenerator import RandomCandidateReplacementGenerator
from rust.nodes.MarkedASTNode import MarkedASTNode
from rust.nodes.Expression import BinaryExpression
from rust.modification.Constraint import Constraint, ConstraintChecker
from rust.modification.ModificationPointSelector import ModificationPointSelector


AVL_RS_PATH = os.path.abspath(os.path.join(
    os.path.dirname(__file__), '..', 'Benchmarks', 'avl', 'avl.rs'
))


def _parse_avl():
    if not _PARSER_AVAILABLE:
        pytest.skip("Generated Rust parser not available in this environment")

    if not os.path.exists(AVL_RS_PATH):
        pytest.skip(f"avl.rs not found at {AVL_RS_PATH}")

    with open(AVL_RS_PATH, "r", encoding="utf-8") as f:
        rust_code = f.read()

    lexer = RustLexer(antlr4.InputStream(rust_code))
    tokens = antlr4.CommonTokenStream(lexer)
    parser = RustParser(tokens)
    tree = parser.program()
    transformer = RustASTTransformer()
    return transformer.visit(tree)


def test_avl_rs_pipeline_produces_a_valid_mutant():
    ast = _parse_avl()
    printer = RustASTPrinter()

    original_source = printer.visit(ast)
    assert original_source  # sanity: the file actually parses and prints

    marked_ast = ast.accept(MarkingVisitor())

    marked_count = len(NodeCollector(MarkedASTNode).collect(marked_ast))
    assert marked_count > 0  # marking actually produced modification points

    checker = ConstraintChecker([Constraint(BinaryExpression, "op", "+")])
    selector = ModificationPointSelector(checker, rng=random.Random(0))
    selected = selector.select(marked_ast)

    assert selected is not None  # avl.rs has "+" binary expressions (rightRotate/leftRotate/insert)

    generator = RandomCandidateReplacementGenerator(selected, rng=random.Random(0))
    new_ast = marked_ast.accept(generator)

    mutated_source = printer.visit(new_ast)
    assert mutated_source  # the mutant still prints to something

    # Same number of top-level items (functions/structs) - mutation only
    # replaced one expression, it never added or removed declarations.
    i = 0
    while marked_ast.exp(i) is not None:
        i += 1
    original_top_level_count = i

    j = 0
    while new_ast.exp(j) is not None:
        j += 1
    mutated_top_level_count = j

    assert mutated_top_level_count == original_top_level_count


def test_avl_rs_original_ast_is_never_mutated():
    ast = _parse_avl()
    printer = RustASTPrinter()

    marked_ast = ast.accept(MarkingVisitor())
    before_source = printer.visit(marked_ast)

    checker = ConstraintChecker([Constraint(BinaryExpression, "op", "+")])
    selector = ModificationPointSelector(checker, rng=random.Random(1))
    selected = selector.select(marked_ast)
    assert selected is not None

    generator = RandomCandidateReplacementGenerator(selected, rng=random.Random(1))
    marked_ast.accept(generator)  # discard the result on purpose

    after_source = printer.visit(marked_ast)
    assert after_source == before_source  # marked_ast itself was never touched


if __name__ == "__main__":
    tests = [
        test_avl_rs_pipeline_produces_a_valid_mutant,
        test_avl_rs_original_ast_is_never_mutated,
    ]
    failures = 0
    for test in tests:
        try:
            test()
            print(f"PASSED: {test.__name__}")
        except pytest.skip.Exception as e:
            print(f"SKIPPED: {test.__name__}: {e}")
        except AssertionError as e:
            failures += 1
            print(f"FAILED: {test.__name__}: {e}")
        except Exception as e:
            failures += 1
            print(f"ERROR: {test.__name__}: {type(e).__name__}: {e}")

    print(f"\n{len(tests) - failures}/{len(tests)} passed")
    sys.exit(1 if failures else 0)
