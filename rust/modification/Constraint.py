class EditConstraint:
    """Base class for AST editing constraints."""
    def matches(self, node, visitor) -> bool:
        raise NotImplementedError


class IsInUnsafeContext(EditConstraint):
    """Constraint that checks if the visitor is currently inside an unsafe scope."""
    def matches(self, node, visitor) -> bool:
        return visitor.in_unsafe


class IsTargetMarkedType(EditConstraint):
    """Example of an extra constraint: only edit if wrapping a specific inner type."""
    def __init__(self, target_class):
        self.target_class = target_class

    def matches(self, node, visitor) -> bool:
        # e.g., only trigger if the node wrapped inside MarkedASTNode is a BinaryExpression
        return isinstance(getattr(node, 'node', None), self.target_class)