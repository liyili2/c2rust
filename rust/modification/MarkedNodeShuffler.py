"""
MarkedNodeShuffler

Single responsibility: perform the actual edit - randomly permute the inner
nodes wrapped by an already-collected list of MarkedASTNode positions.

This is deliberately not a visitor: it does no AST traversal and no
eligibility/constraint checking. It operates purely on the flat list of
modification points handed to it by MarkedNodeCollector, which keeps the
edit itself decoupled from how those positions were found.
"""

import random


class MarkedNodeShuffler:

    def __init__(self, rng: random.Random = None):
        self._rng = rng or random.Random()

    def shuffle(self, marked_nodes: list) -> None:
        """Randomly permutes the wrapped inner nodes across `marked_nodes`, in place."""
        if len(marked_nodes) < 2:
            return

        inner_nodes = [m.node for m in marked_nodes]
        shuffled = inner_nodes[:]
        while shuffled == inner_nodes:
            self._rng.shuffle(shuffled)

        for marked, new_inner in zip(marked_nodes, shuffled):
            marked.node = new_inner
