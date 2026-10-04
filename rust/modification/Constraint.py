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

`attribute` can also be omitted entirely (left as None), meaning "any node
of `node_type` is eligible" - e.g.

    Constraint(BinaryExpression)

which matches every BinaryExpression regardless of its contents. This is
the shape used for modification-point-level constraints, where the
condition is often just "is this the kind of node we're willing to touch
here" rather than a specific field/value check.

Adding a new condition never requires writing a predicate function, a new
visitor, or a new file - it's one more Constraint(...) entry in the list
below. ConstraintChecker then answers a single question - "does this node
satisfy any constraint in its list?" - and that's what gets handed to
NodeCollector/the editor as the eligibility check; neither Constraint nor
ConstraintChecker does any traversal or editing themselves.
"""

from rust.nodes.Expression import BinaryExpression


class Constraint:

    def __init__(self, node_type: type, attribute: str = None, expected_value=None):
        self.node_type = node_type
        self.attribute = attribute
        self.expected_value = expected_value

    def matches(self, node) -> bool:
        if not isinstance(node, self.node_type):
            return False

        if self.attribute is None:
            return True  # type-only constraint - any node of this type is eligible

        if not hasattr(node, self.attribute):
            return False

        actual = getattr(node, self.attribute)
        if callable(actual):
            actual = actual()

        return actual == self.expected_value


# Static for now - add a new Constraint(...) here for any future condition,
# on any node type, without touching Constraint or ConstraintChecker.
#
# This now describes eligibility of a MODIFICATION POINT's wrapped content
# (e.g. "is this a BinaryExpression"), not an enclosing function - see
# ModificationPointSelector, which is what actually applies this list.
DEFAULT_CONSTRAINTS = [
    Constraint(BinaryExpression),
]


class ConstraintChecker:

    def __init__(self, constraints: list = None):
        self._constraints = constraints if constraints is not None else DEFAULT_CONSTRAINTS

    def satisfies_any(self, node) -> bool:
        """True if `node` matches at least one constraint in this checker's list."""
        return any(constraint.matches(node) for constraint in self._constraints)
