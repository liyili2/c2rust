from TypeChecker import TypeChecker
from Expression import LiteralExpr
from Statement import LetStmt
from Type import IntType

checker = TypeChecker()
stmt = LetStmt(
    name="x",
    declared_type=IntType(),
    value=LiteralExpr(42)
)

checker.visit(stmt)