import unittest
import sys
import os
from AST_Scripts.ast.TypeChecker import TypeChecker
from AST_Scripts.ast.Statement import AssignStmt, IfStmt, LetStmt
from AST_Scripts.ast.Expression import BoolLiteral, LiteralExpr
from AST_Scripts.ast.Type import IntType
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

class TestTypeChecker(unittest.TestCase):
    def test_valid_let_stmt_with_int(self):
        checker = TypeChecker()
        stmt = LetStmt(
            name="x",
            declared_type=IntType(),
            value=LiteralExpr(42)
        )

        checker.visit(stmt)
        self.assertIn("x", checker.env.scopes[-1])
        self.assertIsInstance(checker.env.scopes[-1]["x"], IntType)

    def test_let_stmt_type_mismatch(self):
        checker = TypeChecker()
        stmt = LetStmt(
            name="x",
            declared_type=IntType(),
            value=LiteralExpr("hello!")  # Not an int!
        )

        with self.assertRaises(Exception) as context:
            checker.visit(stmt)

        self.assertIn("Type mismatch", str(context.exception))

    def test_valid_if_stmt(self):
        checker = TypeChecker()
        checker.env.define("a", IntType())

        stmt = IfStmt(
            condition=BoolLiteral(True),
            then_branch=[AssignStmt("a", LiteralExpr(1))],
            else_branch=[AssignStmt("a", LiteralExpr(2))]
        )

        checker.visit(stmt)

    def test_if_stmt_with_non_bool_condition(self):
        checker = TypeChecker()
        checker.env.define("a", IntType())

        stmt = IfStmt(
            condition=LiteralExpr(42),  # Not a BoolLiteral!
            then_branch=[AssignStmt("a", LiteralExpr(1))],
            else_branch=[AssignStmt("a", LiteralExpr(2))]
        )

        with self.assertRaises(Exception) as context:
            checker.visit(stmt)
        self.assertIn("Condition in if-statement must be of type bool", str(context.exception))

if __name__ == "__main__":
    unittest.main()
