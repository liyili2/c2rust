from rust.visitors.Base import RustASTGenerator
from rust.nodes.MarkedASTNode import MarkedASTNode

class MarkedNodeTargetUpdater(RustASTGenerator):
    """Rebuilds the tree, swapping the MarkedASTNode with the given id for `target`."""

    def __init__(self, point_id, target):
        super().__init__()
        self._point_id = point_id
        self._target = target

    def visitMarkedASTNode(self, node: MarkedASTNode):
        if node.get_id() == self._point_id:
            return self._target
        return super().visitMarkedASTNode(node)
