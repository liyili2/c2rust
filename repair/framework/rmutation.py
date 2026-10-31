import inspect
import random

from jmetal.core.operator import Mutation
from jmetal.util.ckecking import Check

from .operators import RustSwapOperator, RustReplacementOperator
from .rpatch import RPatch

"""
.. module:: rmutation
   :synopsis: Mutation for RPatch that picks one of the Rust edit operators.
"""


class RustMutation(Mutation[RPatch]):
    """
    With probability `probability`, add ONE new edit to the solution, chosen among
    `operators` (default: RustSwapOperator and RustReplacementOperator).

    The operator is drawn at random, weighted by each operator's get_weight_initial().
    If the drawn operator finds nothing eligible (or its edit cannot be applied), the next
    one is tried, so a mutation only comes back empty when no operator can do anything.

    The edit is chosen against the solution's current AST (updated_contents=solution.ast)
    and added with RPatch.add, which applies it to the AST and records it in the edit list.
    `last_edit` holds the edit added by the last execute() (None if there was none).
    """

    def __init__(self, probability: float, operators=None, checker=None, scope_checker=None,
                 pair_checker=None, max_attempts: int = 10, rng: random.Random = None):
        super(RustMutation, self).__init__(probability=probability)
        self.operators = list(operators) if operators else [RustSwapOperator,
                                                            RustReplacementOperator]
        self.checker = checker
        self.scope_checker = scope_checker  # e.g. only inside unsafe functions
        self.pair_checker = pair_checker    # only passed to operators whose create() accepts it
        self.max_attempts = max_attempts
        self.rng = rng or random.Random()
        self.last_edit = None

    @staticmethod
    def _weight(operator) -> float:
        getter = getattr(operator, 'get_weight_initial', None)
        return float(getter()) if getter is not None else 1.0

    def _operator_order(self):
        """All operators, in a random weighted order: the first one is the pick."""
        remaining, order = list(self.operators), []
        while remaining:
            weights = [self._weight(op) for op in remaining]
            if sum(weights) <= 0:
                weights = [1.0] * len(remaining)
            pick = self.rng.choices(remaining, weights=weights, k=1)[0]
            order.append(pick)
            remaining.remove(pick)
        return order

    def execute(self, solution: RPatch) -> RPatch:
        Check.that(isinstance(solution, RPatch), "Solution type invalid")

        self.last_edit = None
        if self.rng.random() > self.probability:
            return solution

        for operator in self._operator_order():
            kwargs = dict(checker=self.checker, scope_checker=self.scope_checker,
                          rng=self.rng, max_attempts=self.max_attempts,
                          updated_contents=solution.ast)
            if self.pair_checker is not None and \
                    'pair_checker' in inspect.signature(operator.create).parameters:
                kwargs['pair_checker'] = self.pair_checker
            edit = operator.create(solution.program, **kwargs)
            if solution.add(edit):       # False: no-op (nothing eligible) or failed to apply
                self.last_edit = edit
                break
        return solution

    def get_name(self):
        return 'Rust mutation (' + ', '.join(op.__name__ for op in self.operators) + ')'


RustSwapMutation = RustMutation   # old name, kept so existing imports keep working