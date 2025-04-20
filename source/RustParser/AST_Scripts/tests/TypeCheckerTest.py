import unittest
from TypeChecker import TypeChecker
from Statement import LetStmt
from Expression import LiteralExpr
from Type import IntType

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

    def test_type_mismatch(self):
        checker = TypeChecker()
        stmt = LetStmt(
            name="x",
            declared_type=IntType(),
            value=LiteralExpr("hello!")  # Not an int!
        )

        with self.assertRaises(Exception) as context:
            checker.visit(stmt)

        self.assertIn("Type mismatch", str(context.exception))

if __name__ == "__main__":
    unittest.main()
