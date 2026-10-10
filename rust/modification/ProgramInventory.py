"""
ProgramInventory

Not a visitor itself: it composes NodeCollector to answer "which binary operators
and which integer constants does this PROGRAM actually use?". It is the
program-wide counterpart of ScopeEnvironment (which is per-point), and mirrors
QGen's `ops` / `num_range` constructor arguments, except that the values come
from the program instead of a hardcoded config.

Computed once, before selection/generation; it does not change as a generator
descends. Works on the plain or the marked AST: RustASTVisitor.visitMarkedASTNode
just visits the wrapped node.

Place this file in rust/modification/.
"""

from rust.visitors.NodeCollector import NodeCollector
from rust.nodes.Expression import BinaryExpression, Literal, IntLiteral, FieldAccessExpr, IdentifierExpression

def _as_int(value):
    """Integer value of a literal's raw payload, or None if it isn't one (bools excluded)."""
    if isinstance(value, bool):
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


class ProgramInventory:

    def __init__(self, ast):
        self._ops = sorted({node.op() for node in NodeCollector(BinaryExpression).collect(ast)})

        # IntLiteral.accept() dispatches to visitLiteral, so NodeCollector has to be
        # pointed at Literal and the subtype filtered afterwards.
        literals = NodeCollector(Literal, lambda n: isinstance(n, IntLiteral)).collect(ast)
        values = (_as_int(n.value()) for n in literals)
        self._nums = sorted({v for v in values if v is not None})
        self._field_accesses = []
        for fa in NodeCollector(FieldAccessExpr).collect(ast):
            names = {i.name() for i in NodeCollector(IdentifierExpression).collect(fa)}
            self._field_accesses.append((fa, names))

    def operators(self) -> list:
        return list(self._ops)

    def operators_in_group(self, group: list) -> list:
        """The members of `group` that the program really uses, in `group` order."""
        return [op for op in group if op in self._ops]

    def numbers(self) -> list:
        return list(self._nums)

    def number_range(self):
        """(min, max) of the integer constants in the program, or None if it has none."""
        return (min(self._nums), max(self._nums)) if self._nums else None

    def summary(self) -> str:
        return f"operators={self._ops} numbers={self._nums} number_range={self.number_range()}"

    def field_accesses_in_scope(self, scope, exclude_key=None, key=str):
        """Field accesses from the program whose every identifier is visible in `scope`,
        deduplicated, and excluding the one being replaced."""
        result, seen = [], set()
        for fa, names in self._field_accesses:
            if not all(scope.has(n) for n in names):
                continue
            k = key(fa)
            if k == exclude_key or k in seen:
                continue
            seen.add(k)
            result.append(fa)
        return result