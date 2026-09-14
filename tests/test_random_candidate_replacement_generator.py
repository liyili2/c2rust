import sys
import os
import random

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from rust.nodes.Program import Program
from rust.nodes.TopLevel import FunctionDefinition
from rust.nodes.Func import Param
from rust.nodes.Statement import Block, LetStmt, ReturnStmt
from rust.nodes.Expression import (
    VarDef, IdentifierExpression, BinaryExpression, FunctionCallExpression,
    BorrowExpression, ArrayLiteral, IntLiteral, CastExpression, UnaryExpr,
    DereferenceExpr, ParenExpr, RangeExpression, QualifiedExpression,
)
from rust.nodes.Type import SignedIntType
from rust.nodes.MarkedASTNode import MarkedASTNode
from rust.visitors.NodeCollector import NodeCollector
from rust.visitors.RandomCandidateReplacementGenerator import RandomCandidateReplacementGenerator


def _wrap_in_function(body_stmts, params=None):
    """unsafe fn f(<params>) { <body_stmts> } wrapped in a Program."""
    params = params or []
    body = Block(body_stmts, is_unsafe=True)
    func = FunctionDefinition("f", params, None, body, is_unsafe=True)
    return Program([func])


def _run(program, marked_node):
    generator = RandomCandidateReplacementGenerator(marked_node, rng=random.Random(0))
    return program.accept(generator)


def _single_marked(node_to_mark, params=None):
    """Builds a one-statement function with the given expression marked,
    returns (program, marked_node)."""
    marked = MarkedASTNode(node_to_mark)
    stmt = LetStmt(VarDef("result"), marked)
    program = _wrap_in_function([stmt], params=params)
    return program, marked


def test_identifier_candidate_is_another_visible_name():
    x_param = Param("x", SignedIntType("i32"), False)
    y_param = Param("y", SignedIntType("i32"), False)
    program, marked = _single_marked(IdentifierExpression("x"), params=[x_param, y_param])

    new_program = program.accept(RandomCandidateReplacementGenerator(marked, rng=random.Random(1)))
    result = new_program.exp(0).body().statements()[0].values()[0]

    assert isinstance(result, IdentifierExpression)
    assert result.name() == "y"  # only other visible, type-compatible name


def test_binary_expression_candidate_is_structurally_valid():
    x_param = Param("x", SignedIntType("i32"), False)
    original = BinaryExpression(IdentifierExpression("x"), "+", IntLiteral(1))
    program, marked = _single_marked(original, params=[x_param])

    new_program = _run(program, marked)
    result = new_program.exp(0).body().statements()[0].values()[0]

    assert isinstance(result, BinaryExpression)
    assert result.op() in RandomCandidateReplacementGenerator._ARITHMETIC_OPS


def test_function_call_candidate_remains_valid_call():
    x_param = Param("x", SignedIntType("i32"), False)
    y_param = Param("y", SignedIntType("i32"), False)
    original = FunctionCallExpression(IdentifierExpression("foo"), [IdentifierExpression("x")])
    program, marked = _single_marked(original, params=[x_param, y_param])

    new_program = _run(program, marked)
    result = new_program.exp(0).body().statements()[0].values()[0]

    assert isinstance(result, FunctionCallExpression)
    assert len(result.args()) == 1
    assert isinstance(result.args()[0], IdentifierExpression)


def test_borrow_candidate_toggles_mutability():
    original = BorrowExpression(IdentifierExpression("x"), is_mutable=False)
    program, marked = _single_marked(original)

    new_program = _run(program, marked)
    result = new_program.exp(0).body().statements()[0].values()[0]

    assert isinstance(result, BorrowExpression)
    assert result.is_mutable() is True
    assert isinstance(result.expression(), IdentifierExpression)
    assert result.expression().name() == "x"


def test_array_literal_candidate_remains_valid_array():
    original = ArrayLiteral([IntLiteral(1), IntLiteral(2)])
    program, marked = _single_marked(original)

    new_program = _run(program, marked)
    result = new_program.exp(0).body().statements()[0].values()[0]

    assert isinstance(result, ArrayLiteral)
    assert len(result.value()) == 2


def test_unary_candidate_remains_valid():
    x_param = Param("x", SignedIntType("i32"), False)
    original = UnaryExpr("-", IdentifierExpression("x"))
    program, marked = _single_marked(original, params=[x_param])

    new_program = _run(program, marked)
    result = new_program.exp(0).body().statements()[0].values()[0]

    assert isinstance(result, UnaryExpr)
    assert result.op() == "-"


def test_cast_candidate_remains_structurally_valid():
    x_param = Param("x", SignedIntType("i32"), False)
    original = CastExpression(IdentifierExpression("x"), [SignedIntType("i64")])
    program, marked = _single_marked(original, params=[x_param])

    new_program = _run(program, marked)
    result = new_program.exp(0).body().statements()[0].values()[0]

    assert isinstance(result, CastExpression)
    assert result.type() == [SignedIntType("i64")] or isinstance(result.type(), list)


def test_dereference_candidate_remains_structurally_valid():
    x_param = Param("x", SignedIntType("i32"), False)
    original = DereferenceExpr(IdentifierExpression("x"))
    program, marked = _single_marked(original, params=[x_param])

    new_program = _run(program, marked)
    result = new_program.exp(0).body().statements()[0].values()[0]

    assert isinstance(result, DereferenceExpr)
    assert isinstance(result.expression(), IdentifierExpression)


def test_paren_candidate_mutates_inner_expression_preserving_parens():
    x_param = Param("x", SignedIntType("i32"), False)
    original = ParenExpr(IdentifierExpression("x"))
    program, marked = _single_marked(original, params=[x_param])

    new_program = _run(program, marked)
    result = new_program.exp(0).body().statements()[0].values()[0]

    assert isinstance(result, ParenExpr)  # parens preserved
    assert isinstance(result.expression(), IdentifierExpression)


def test_range_candidate_respects_range_shape():
    x_param = Param("x", SignedIntType("i32"), False)
    original = RangeExpression(IntLiteral(0), IntLiteral(10))
    program, marked = _single_marked(original, params=[x_param])

    new_program = _run(program, marked)
    result = new_program.exp(0).body().statements()[0].values()[0]

    assert isinstance(result, RangeExpression)


def test_unmarked_nodes_are_preserved_and_only_selected_node_changes():
    """Two marked identifiers exist; only the SELECTED one should change."""
    x_param = Param("x", SignedIntType("i32"), False)
    y_param = Param("y", SignedIntType("i32"), False)

    marked_x = MarkedASTNode(IdentifierExpression("x"))
    marked_y = MarkedASTNode(IdentifierExpression("y"))

    stmt1 = LetStmt(VarDef("a"), marked_x)
    stmt2 = LetStmt(VarDef("b"), marked_y)
    program = _wrap_in_function([stmt1, stmt2], params=[x_param, y_param])

    new_program = program.accept(RandomCandidateReplacementGenerator(marked_x, rng=random.Random(2)))
    statements = new_program.exp(0).body().statements()

    changed = statements[0].values()[0]
    untouched = statements[1].values()[0]

    assert isinstance(untouched, MarkedASTNode)  # still marked, unchanged
    assert untouched.node.name() == "y"
    assert isinstance(changed, IdentifierExpression)  # selected node replaced, unwrapped
    assert changed.name() == "y"  # only other visible name


def test_original_ast_is_never_mutated():
    x_param = Param("x", SignedIntType("i32"), False)
    y_param = Param("y", SignedIntType("i32"), False)
    program, marked = _single_marked(IdentifierExpression("x"), params=[x_param, y_param])

    before = NodeCollector(MarkedASTNode).collect(program)
    assert len(before) == 1
    assert before[0].node.name() == "x"

    _run(program, marked)

    after = NodeCollector(MarkedASTNode).collect(program)
    assert len(after) == 1
    assert after[0].node.name() == "x"  # original untouched


if __name__ == "__main__":
    tests = [v for k, v in list(globals().items()) if k.startswith("test_")]
    failures = 0
    for test in tests:
        try:
            test()
            print(f"PASSED: {test.__name__}")
        except AssertionError as e:
            failures += 1
            print(f"FAILED: {test.__name__}: {e}")
        except Exception as e:
            failures += 1
            print(f"ERROR: {test.__name__}: {type(e).__name__}: {e}")

    print(f"\n{len(tests) - failures}/{len(tests)} passed")
    sys.exit(1 if failures else 0)
