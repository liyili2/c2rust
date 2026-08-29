"""
Tests for rust.constraints.Constraints and rust.edits.UnsafeFunctionShuffleEditor.

Run with pytest:
    pytest tests/test_unsafe_function_shuffle.py -v

Or standalone (no pytest required):
    python tests/test_unsafe_function_shuffle.py
"""

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from rust.nodes.Program import Program
from rust.nodes.TopLevel import FunctionDefinition
from rust.nodes.Statement import Block, LetStmt
from rust.nodes.Expression import VarDef, IdentifierExpression
from rust.nodes.MarkedASTNode import MarkedASTNode
from rust.modification.Constraint import ConstraintChecker
from rust.modification.Unsafefunctionshuffleeditor import UnsafeFunctionShuffleEditor
from rust.visitors.ASTEditor import ASTEditor
from rust.visitors.NodeCollector import NodeCollector


def test_constraint_checker_matches_unsafe_function():
    """An unsafe FunctionDefinition satisfies the default (is_unsafe == True) constraint."""
    unsafe_fn = FunctionDefinition(
        identifier="do_it",
        params=[],
        return_type=None,
        body=Block([], is_unsafe=True),
        is_unsafe=True,
    )

    checker = ConstraintChecker()

    assert checker.satisfies_any(unsafe_fn) is True


def test_constraint_checker_rejects_safe_function():
    """A safe FunctionDefinition should NOT satisfy the default constraint - sanity check
    alongside the positive case above, so the assertion isn't trivially always-true."""
    safe_fn = FunctionDefinition(
        identifier="do_it_safely",
        params=[],
        return_type=None,
        body=Block([], is_unsafe=False),
        is_unsafe=False,
    )

    checker = ConstraintChecker()

    assert checker.satisfies_any(safe_fn) is False


def _build_tiny_unsafe_ast_with_three_marked_let_stmts():
    """
    Builds a minimal Program containing exactly one unsafe FunctionDefinition,
    whose body is three LetStmts, each assigning a MarkedASTNode-wrapped
    identifier expression:

        unsafe fn target() {
            let x0 = <marked: val_a>;
            let x1 = <marked: val_b>;
            let x2 = <marked: val_c>;
        }

    Returns (program, ordered_original_names) where ordered_original_names is
    the sequence of identifier names as they appear in the marked positions,
    in traversal order, before any edit.
    """
    names = ["val_a", "val_b", "val_c"]

    let_stmts = [
        LetStmt(VarDef(f"x{i}"), MarkedASTNode(IdentifierExpression(name)))
        for i, name in enumerate(names)
    ]

    body = Block(let_stmts, is_unsafe=True)
    unsafe_fn = FunctionDefinition(
        identifier="target",
        params=[],
        return_type=None,
        body=body,
        is_unsafe=True,
    )
    program = Program([unsafe_fn])

    return program, names


def _collect_marked_names_in_order(node):
    """Traversal-order list of the identifier names currently sitting inside
    every MarkedASTNode reachable from `node`."""
    marked_nodes = NodeCollector(MarkedASTNode).collect(node)
    return [marked.node.name() for marked in marked_nodes]


def test_shuffle_editor_changes_marked_node_order():
    """
    Building a tiny AST with a single unsafe function whose body is three
    LetStmts, each holding a MarkedASTNode, and running the shuffle editor
    over it should change the order the marked values appear in - while
    still being the same three values, just rearranged.
    """
    program, original_order = _build_tiny_unsafe_ast_with_three_marked_let_stmts()

    assert _collect_marked_names_in_order(program) == original_order  # sanity: order is stable before editing

    editor = UnsafeFunctionShuffleEditor()
    editor.edit(program)

    new_order = _collect_marked_names_in_order(program)

    assert new_order != original_order  # the arrangement changed
    assert sorted(new_order) == sorted(original_order)  # but it's still the same three values, just permuted


def test_ast_editor_returns_new_shuffled_ast_and_leaves_original_untouched():
    """
    ASTEditor is a RustASTGenerator: ast.accept(editor) must return a
    distinct AST object with the eligible function's marked positions
    shuffled, while the original `ast` passed in is left completely
    unmodified.
    """
    program, original_order = _build_tiny_unsafe_ast_with_three_marked_let_stmts()

    editor = ASTEditor()
    new_program = program.accept(editor)

    assert new_program is not program  # a genuinely new AST, not a mutated one

    new_order = _collect_marked_names_in_order(new_program)
    original_still_in_order = _collect_marked_names_in_order(program)

    assert original_still_in_order == original_order  # original AST untouched
    assert new_order != original_order  # new AST is shuffled
    assert sorted(new_order) == sorted(original_order)  # same values, just permuted


def test_ast_editor_leaves_ineligible_functions_unshuffled():
    """A safe (non-matching) function's marked positions should come through
    the generated copy in their original order."""
    from rust.nodes.Program import Program
    from rust.nodes.TopLevel import FunctionDefinition
    from rust.nodes.Statement import Block, LetStmt
    from rust.nodes.Expression import VarDef, IdentifierExpression

    names = ["x", "y", "z"]
    let_stmts = [
        LetStmt(VarDef(f"v{i}"), MarkedASTNode(IdentifierExpression(name)))
        for i, name in enumerate(names)
    ]
    safe_fn = FunctionDefinition(
        identifier="safe_target",
        params=[],
        return_type=None,
        body=Block(let_stmts, is_unsafe=False),
        is_unsafe=False,
    )
    program = Program([safe_fn])

    new_program = program.accept(ASTEditor())
    new_order = _collect_marked_names_in_order(new_program)

    assert new_order == names


if __name__ == "__main__":
    tests = [
        test_constraint_checker_matches_unsafe_function,
        test_constraint_checker_rejects_safe_function,
        test_shuffle_editor_changes_marked_node_order,
        test_ast_editor_returns_new_shuffled_ast_and_leaves_original_untouched,
        test_ast_editor_leaves_ineligible_functions_unshuffled,
    ]

    failures = 0
    for test in tests:
        try:
            test()
            print(f"PASSED: {test.__name__}")
        except AssertionError as e:
            failures += 1
            print(f"FAILED: {test.__name__}: {e}")

    print(f"\n{len(tests) - failures}/{len(tests)} passed")
    sys.exit(1 if failures else 0)