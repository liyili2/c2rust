"""
NodeCollector

Single responsibility: walk a subtree and collect every node of a given
type that satisfies a given predicate.

This is the ONE traversal visitor needed for "find nodes matching some
condition", regardless of what kind of node or what the condition is:

    # nodes to edit within an eligible function:
    NodeCollector(MarkedASTNode, lambda n: True).collect(func.body())

    # eligible functions:
    NodeCollector(FunctionDefinition, is_unsafe).collect(ast)

    # some future, unrelated example - eligible if-statements:
    NodeCollector(IfStmt, has_else_branch).collect(ast)

It never needs a new file or subclass when a new condition or a new target
node type shows up - only the (node_type, predicate) arguments change. The
condition itself is supplied by the caller (see
rust.constraints.Constraints) and is never known to this class; this class
only knows how to intercept the one visitor method that handles `node_type`
(looked up via rust.visitors.Base.NODE_VISIT_METHODS) and otherwise behaves
exactly like RustASTVisitor's default traversal.
"""

from rust.visitors.Base import RustASTVisitor, NODE_VISIT_METHODS


class NodeCollector(RustASTVisitor):

    def __init__(self, node_type: type, predicate=lambda node: True):
        if node_type not in NODE_VISIT_METHODS:
            raise ValueError(f"No visitor method registered for node type: {node_type}")

        self._predicate = predicate
        self._collected = []

        method_name = NODE_VISIT_METHODS[node_type]
        default_visit = getattr(RustASTVisitor, method_name)

        def intercepted(node):
            if self._predicate(node):
                self._collected.append(node)
            return default_visit(self, node)

        setattr(self, method_name, intercepted)

    def collect(self, node) -> list:
        """Returns every node of `node_type` reachable from `node` for which predicate(n) is True."""
        self._collected = []
        node.accept(self)
        return self._collected
