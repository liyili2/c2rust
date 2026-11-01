import random
from typing import List

from jmetal.operator.crossover import Crossover

from rust.visitors.MarkingVisitor import MarkingVisitor
from rust.visitors.ast_compare import ast_equal
from rust.modification.ModificationPointSelector import ModificationPointSelector

from .operators import RustReplacementOperator, strip_marks_tree
from .rpatch import RPatch

"""
.. module:: rcrossover
   :synopsis: Subtree-exchange crossover on the ASTs of two RPatches.
"""


class RustSubtreeCrossover(Crossover[RPatch, RPatch]):
    """
    Exchange one subtree between the two parents' ASTs.

    A random eligible node is picked in parent A and a random eligible node of the same
    node class in parent B. Child A is a copy of A (AST and edits) plus a
    RustReplacementOperator putting a copy of B's subtree at A's node; child B is the
    mirror image. The replacement goes through RPatch.add, so each child's AST changes
    and the exchange is recorded as an ordinary edit (children stay valid PyGGI patches).
    If no compatible pair is found the children are plain copies of the parents.
    """

    def __init__(self, probability: float, scope_checker=None,
                 pair_checker=None, max_attempts: int = 10, rng: random.Random = None):
        super(RustSubtreeCrossover, self).__init__(probability=probability)
        self.scope_checker = scope_checker
        self.pair_checker = pair_checker    # optional (point_a, point_b) -> bool
        self.max_attempts = max_attempts
        self.rng = rng or random.Random()
        self.last_exchange = None   # what the last execute() exchanged (None: nothing)

    def execute(self, parents: List[RPatch]) -> List[RPatch]:
        if len(parents) != 2:
            raise Exception('The number of parents is not two: {}'.format(len(parents)))

        self.last_exchange = None
        child_a, child_b = parents[0].clone(), parents[1].clone()
        if self.rng.random() > self.probability:
            return [child_a, child_b]

        shared_files = [f for f in child_a.ast if f in child_b.ast]
        if not shared_files:
            return [child_a, child_b]
        target_file = self.rng.choice(shared_files)

        marked_a = strip_marks_tree(child_a.ast[target_file]).accept(MarkingVisitor())
        marked_b = strip_marks_tree(child_b.ast[target_file]).accept(MarkingVisitor())
        selector = ModificationPointSelector(checker=self.checker, scope_checker=self.scope_checker, rng=self.rng)
        points_a = selector.eligible_points(marked_a)
        points_b = selector.eligible_points(marked_b)
        if not points_a or not points_b:
            return [child_a, child_b]

        for _ in range(self.max_attempts):
            pa = self.rng.choice(points_a)
            compatible = [pb for pb in points_b if type(pb.node) is type(pa.node)]
            if not compatible:
                continue
            pb = self.rng.choice(compatible)
            if self.pair_checker is not None and not self.pair_checker(pa, pb):
                continue

            subtree_a = strip_marks_tree(pa.node)
            subtree_b = strip_marks_tree(pb.node)
            if ast_equal(subtree_a, subtree_b):
                continue  # exchanging equal subtrees changes nothing

            # point ids come from marking the very trees the children hold, so they match
            applied_a = child_a.add(RustReplacementOperator(target_file, pa.get_id(), subtree_b))
            applied_b = child_b.add(RustReplacementOperator(target_file, pb.get_id(), subtree_a))
            self.last_exchange = {"target_file": target_file,
                                  "node_type": type(pa.node).__name__,
                                  "node_a": subtree_a,      # was in parent 1, now in child 2
                                  "node_b": subtree_b,      # was in parent 2, now in child 1
                                  "applied": (applied_a, applied_b)}
            break

        return [child_a, child_b]

    def get_number_of_parents(self) -> int:
        return 2

    def get_number_of_children(self) -> int:
        return 2

    def get_name(self):
        return 'Rust subtree crossover'