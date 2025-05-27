from ast import Expression
import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from AST_Scripts.ast.TypeChecker import TypeChecker
from AST_Scripts.ast.Statement import AssignStmt, IfStmt, LetStmt, ReturnStmt
from AST_Scripts.ast.Expression import BoolLiteral, BorrowExpr, FunctionCallExpr, IdentifierExpr, LiteralExpr
from AST_Scripts.ast.Type import IntType, RefType
from AST_Scripts.ast.TopLevel import FunctionDef
from AST_Scripts.ast.VarDef import VarDef

class TestTypeChecker(unittest.TestCase):
    def test_valid_let_stmt_with_int(self):
        checker = TypeChecker()
        stmt = LetStmt(
            var_def=VarDef(name="x", var_type=IntType()),
            value=LiteralExpr(42)
        )

        checker.visit(stmt)
        self.assertIn("x", checker.env.scopes[-1])
        self.assertIsInstance(checker.env.scopes[-1]["x"]["type"], IntType)

    def test_let_stmt_type_mismatch(self):
        checker = TypeChecker()
        stmt = LetStmt(
            var_def=VarDef(name="x", var_type=IntType()),
            value=LiteralExpr("hello!")  # Not an int!
        )

        checker.visit(stmt)
        assert(checker.error_count == 1)

    def test_valid_if_stmt(self):
        checker = TypeChecker()
        let_a = LetStmt(
            var_def=VarDef(name="a", var_type=IntType()),
            value=LiteralExpr(42)
        )
        stmt = IfStmt(
            condition=BoolLiteral(True),
            then_branch=[AssignStmt("a", LiteralExpr(1))],
            else_branch=[AssignStmt("a", LiteralExpr(2))]
        )

        checker.visit(let_a)
        checker.visit(stmt)
        assert(checker.error_count == 0)

    def test_if_stmt_with_non_bool_condition(self):
        checker = TypeChecker()
        checker.env.declare("a", IntType(), mutable=False)

        stmt = IfStmt(
            condition=LiteralExpr(42),
            then_branch=[AssignStmt("a", LiteralExpr(1))],
            else_branch=[AssignStmt("a", LiteralExpr(2))]
        )

        checker.visit(stmt)
        assert checker.error_count == 1

    def test_use_after_move_raises_error(self):
        checker = TypeChecker()
        let_x = LetStmt(
            var_def=VarDef(name="x", var_type=IntType()),
            value=LiteralExpr(42)
        )
        let_y = LetStmt(
            var_def=VarDef(name="y", var_type=IntType()),
            value=IdentifierExpr("x")
        )
        reassign_x = AssignStmt(
            target="x",
            value=LiteralExpr(5)
        )

        checker.visit(let_x)
        checker.visit(let_y)
        checker.visit(reassign_x)
        assert(checker.error_count == 2)

    def test_pass_moved_value_to_function(self):
        checker = TypeChecker()
        checker.env.declare_function("foo", [IntType()], None)
        let_x = LetStmt(
            var_def=VarDef(name="x", var_type=IntType()),
            value=LiteralExpr(42))
        let_y = LetStmt(
            var_def=VarDef(name="y", var_type=IntType()),
            value=IdentifierExpr("x"))
        call_foo_with_x = FunctionCallExpr(
            func="foo",
            args=[IdentifierExpr("x")])

        checker.visit(let_x)
        checker.visit(let_y)        
        checker.visit(call_foo_with_x)        
        assert checker.error_count > 0

    def test_use_after_move_to_function(self):
        checker = TypeChecker()
        let_x = LetStmt(
            var_def=VarDef(name="x", var_type=IntType()),
            value=LiteralExpr(42)
        )
        call_foo = FunctionCallExpr(
            func="foo",
            args=[IdentifierExpr("x")]
        )
        assign_y = LetStmt(
            var_def=VarDef(name="y", var_type=IntType()),
            value=IdentifierExpr("x")
        )
        checker.env.declare_function(
            name="foo",
            param_types=[IntType()],
            return_type=None
        )

        assert(checker.visit(let_x))
        checker.visit(call_foo)
        assert(checker.visit(assign_y))

    def test_borrow_expr_marks_as_borrowed_and_returns_ref_type(self):
        checker = TypeChecker()

        let_stmt = LetStmt(
            var_def=VarDef(name="x", var_type=IntType()),
            value=LiteralExpr(42)
        )
        checker.visit(let_stmt)

        borrow_expr = BorrowExpr(name="x")
        typ = checker.visit(borrow_expr)

        self.assertIsInstance(typ, RefType)
        self.assertIsInstance(typ.inner, IntType)
        self.assertTrue(checker.env.lookup("x")["borrowed"])

    def test_assignment_while_borrowed_should_fail(self):
        checker = TypeChecker()
        let_stmt = LetStmt(
            var_def=VarDef(name="x", var_type=IntType()),
            value=LiteralExpr(42)
        )
        checker.visit(let_stmt)

        borrow_expr = BorrowExpr(name="x")
        checker.visit(borrow_expr)

        assign_stmt = AssignStmt(
            target="x",
            value=LiteralExpr(100)
        )
        checker.visit(assign_stmt)
        assert checker.error_count > 0

    def test_move_borrowed_variable_should_fail(self):
        checker = TypeChecker()

        let_x = LetStmt(
            var_def=VarDef(name="x", var_type=IntType()),
            value=LiteralExpr(5)
        )
        borrow_x = LetStmt(
            var_def=VarDef(name="y", var_type=RefType(IntType())),
            value=BorrowExpr("x")
        )
        move_x = LetStmt(
            var_def=VarDef(name="z", var_type=IntType()),
            value=IdentifierExpr("x")
        )

        checker.visit(let_x)
        checker.visit(borrow_x)
        checker.visit(move_x)
        assert checker.error_count > 0

    def test_borrowed_variable_is_reset_after_function_call(self):
        checker = TypeChecker()

        let_x = LetStmt(
            var_def=VarDef(name="x", var_type=IntType()),
            value=LiteralExpr(5)
        )
        checker.env.declare_function("foo", RefType(IntType()), IntType())
        func_call = FunctionCallExpr(
            func="foo",
            args=[IdentifierExpr("x")]
        )
        checker.visit(let_x)
        checker.visit(func_call)

        info = checker.env.lookup("x")
        self.assertFalse(info["borrowed"])

    def test_reborrow_while_already_borrowed(self):
        checker = TypeChecker()
        let_x = LetStmt(
            var_def=VarDef(name="x", var_type=IntType(), mutable=False),
            value=LiteralExpr(1)
        )
        borrow1 = LetStmt(
            var_def=VarDef(name="ref1", var_type=IntType(), mutable=False),
            value=IdentifierExpr("x")
        )
        borrow2 = LetStmt(
            var_def=VarDef(name="ref2", var_type=IntType(), mutable=False),
            value=IdentifierExpr("x")
        )

        checker.visit(let_x)
        checker.visit(borrow1)
        checker.visit(borrow2)
        assert checker.error_count > 0

    def test_mutable_borrow_of_immutable_variable(self):
        checker = TypeChecker()
        let_stmt = LetStmt(
            var_def=VarDef(name="x", var_type=IntType(), mutable=False),
            value=LiteralExpr(5)
        )

        borrow_stmt = LetStmt(
            var_def=VarDef(name="y", var_type=None, mutable=False),
            value=BorrowExpr(name="x", mutable=True)
        )

        checker.visit(let_stmt)
        checker.visit(borrow_stmt)
        assert checker.error_count > 0

    def test_mutable_borrow_while_immutable_exists(self):
        checker = TypeChecker()
        let_x = LetStmt(
            var_def=VarDef(name="x", var_type=IntType()),
            value=LiteralExpr(10)
        )
        borrow_y = LetStmt(
            var_def=VarDef(name="y", var_type=IntType()),
            value=BorrowExpr(name="x", mutable=False)
        )
        borrow_z = LetStmt(
            var_def=VarDef(name="z", var_type=IntType()),
            value=BorrowExpr(name="x", mutable=True)
        )
        checker.visit(let_x)
        checker.visit(borrow_y)
        checker.visit(borrow_z)
        assert checker.error_count > 0

if __name__ == "__main__":
    unittest.main()
