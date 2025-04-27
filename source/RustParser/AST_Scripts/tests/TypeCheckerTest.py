from ast import Expression
import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from AST_Scripts.ast.TypeChecker import TypeChecker
from AST_Scripts.ast.Statement import AssignStmt, IfStmt, LetStmt
from AST_Scripts.ast.Expression import BoolLiteral, FunctionCallExpr, IdentifierExpr, LiteralExpr
from AST_Scripts.ast.Type import IntType

class TestTypeChecker(unittest.TestCase):
    # def test_valid_let_stmt_with_int(self):
    #     checker = TypeChecker()
    #     stmt = LetStmt(
    #         name="x",
    #         declared_type=IntType(),
    #         value=LiteralExpr(42)
    #     )

    #     assert(checker.visit(stmt))
    #     self.assertIn("x", checker.env.scopes[-1])
    #     self.assertIsInstance(checker.env.scopes[-1]["x"]["type"], IntType)

    # def test_let_stmt_type_mismatch(self):
    #     checker = TypeChecker()
    #     stmt = LetStmt(
    #         name="x",
    #         declared_type=IntType(),
    #         value=LiteralExpr("hello!")  # Not an int!
    #     )

    #     assert(not checker.visit(stmt))

    # def test_valid_if_stmt(self):
    #     checker = TypeChecker()
    #     let_a = LetStmt(
    #         name="a",
    #         declared_type=IntType(),
    #         value=LiteralExpr(42)
    #     )
    #     stmt = IfStmt(
    #         condition=BoolLiteral(True),
    #         then_branch=[AssignStmt("a", LiteralExpr(1))],
    #         else_branch=[AssignStmt("a", LiteralExpr(2))]
    #     )

    #     assert(checker.visit(let_a))
    #     assert(checker.visit(stmt))

    # def test_if_stmt_with_non_bool_condition(self):
    #     checker = TypeChecker()
    #     checker.env.define("a", IntType())

    #     stmt = IfStmt(
    #         condition=LiteralExpr(42),  # Not a BoolLiteral!
    #         then_branch=[AssignStmt("a", LiteralExpr(1))],
    #         else_branch=[AssignStmt("a", LiteralExpr(2))]
    #     )

    #     assert(not checker.visit(stmt))

    # def test_use_after_move_raises_error(self):
    #     checker = TypeChecker()      
    #     let_x = LetStmt(
    #         name="x",
    #         declared_type=IntType(),
    #         value=LiteralExpr(42)
    #     )
    #     let_y = LetStmt(
    #         name="y",
    #         declared_type=IntType(),
    #         value=IdentifierExpr("x")
    #     )
    #     reassign_x = AssignStmt(
    #         target="x",
    #         value=LiteralExpr(5)
    #     )

    #     checker.visit(let_x)
    #     checker.visit(let_y)
    #     assert(not checker.visit(reassign_x))

    # def test_pass_moved_value_to_function(self):
    #     checker = TypeChecker()
    #     checker.env.declare_function("foo", [IntType()], None)
    #     let_x = LetStmt(
    #         name="x",
    #         declared_type=IntType(),
    #         value=LiteralExpr(42)
    #     )
    #     let_y = LetStmt(
    #         name="y",
    #         declared_type=IntType(),
    #         value=IdentifierExpr("x")
    #     )
    #     call_foo_with_x = FunctionCallExpr(
    #         func="foo",
    #         args=[IdentifierExpr("x")]
    #     )

    #     checker.visit(let_x)
    #     checker.visit(let_y)
    #     assert(not checker.visit(call_foo_with_x))

    def test_use_after_move_to_function(self):
        checker = TypeChecker()
        let_x = LetStmt(
            name="x",
            declared_type=IntType(),
            value=LiteralExpr(42)
        )
        call_foo = FunctionCallExpr(
            func="foo",
            args=[IdentifierExpr("x")]
        )
        assign_y = LetStmt(
            name="y",
            declared_type=IntType(),
            value=IdentifierExpr("x")
        )
        checker.env.declare_function(
            name="foo",
            param_types=[IntType()],
            return_type=None
        )

        assert(checker.visit(let_x)) 
        checker.visit(call_foo)
        assert(not checker.visit(assign_y))

if __name__ == "__main__":
    unittest.main()
