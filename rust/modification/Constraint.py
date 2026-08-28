"""
Constraints

Declarative constraints over AST nodes, expressed as data rather than code.

A Constraint says: "a node of `node_type` is eligible when `attribute`
equals `expected_value`" - e.g.

    Constraint(FunctionDefinition, "is_unsafe", True)

`attribute` is read via getattr(node, attribute); if what comes back is
callable (a getter method like `is_unsafe`, not a plain field) it's called
with no arguments first, so this works uniformly whether the node exposes
the value as a method or a plain attribute.

Adding a new condition never requires writing a predicate function, a new
visitor, or a new file - it's one more Constraint(...) entry in the list
below. ConstraintChecker then answers a single question - "does this node
satisfy any constraint in its list?" - and that's what gets handed to
NodeCollector/the editor as the eligibility check; neither Constraint nor
ConstraintChecker does any traversal or editing themselves.
"""

from rust.nodes.TopLevel import FunctionDefinition


class Constraint:

    def __init__(self, node_type: type, attribute: str, expected_value):
        self.node_type = node_type
        self.attribute = attribute
        self.expected_value = expected_value

    def matches(self, node) -> bool:
        if not isinstance(node, self.node_type):
            return False
        if not hasattr(node, self.attribute):
            return False

        actual = getattr(node, self.attribute)
        if callable(actual):
            actual = actual()

        return actual == self.expected_value


# Static for now - add a new Constraint(...) here for any future condition,
# on any node type, without touching Constraint or ConstraintChecker.
DEFAULT_CONSTRAINTS = [
    Constraint(FunctionDefinition, "is_unsafe", True),
]


class ConstraintChecker:

    def __init__(self, constraints: list = None):
        self._constraints = constraints if constraints is not None else DEFAULT_CONSTRAINTS

    def satisfies_any(self, node) -> bool:
        """True if `node` matches at least one constraint in this checker's list."""
        return any(constraint.matches(node) for constraint in self._constraints)
