"""
CandidateGenerator

A candidate generator answers exactly one question: given the node
currently sitting at a modification point, what should replace it?

This is deliberately a small, swappable interface: ASTEditor and
ModificationPointSelector don't know or care how a candidate gets built,
only that generate(original_node) returns a new node to substitute in.

ExistingValueCandidateGenerator is the MINIMAL implementation: it reuses
another value already present elsewhere in the AST's modification points,
chosen at random from a pool supplied up front. This is a small step up
from the old shuffle-based approach (exactly one point changes per
generated AST instead of a whole function's worth), but it can still only
ever recombine values that already exist somewhere in the tree.

The full QGen-style synthesis - a generator backed by an actual scope/type
environment, able to build genuinely new expressions (a different in-scope
variable, a new constant, a new operator combination) the way
RandomCandidateReplacementProgramGenerator.get_random_candidate does - is
future work, and would be a second implementation of this same interface;
nothing else in the pipeline (ASTEditor, ModificationPointSelector) would
need to change to support it.
"""

import copy
import random
from abc import ABC, abstractmethod


class CandidateGenerator(ABC):

    @abstractmethod
    def generate(self, original_node):
        """Returns a new node to substitute in place of `original_node`."""
        pass


class ExistingValueCandidateGenerator(CandidateGenerator):

    def __init__(self, pool: list, rng: random.Random = None):
        self._pool = pool
        self._rng = rng or random.Random()

    def generate(self, original_node):
        candidates = [node for node in self._pool if node is not original_node]

        if not candidates:
            return original_node  # nothing else available to swap in

        return copy.deepcopy(self._rng.choice(candidates))
