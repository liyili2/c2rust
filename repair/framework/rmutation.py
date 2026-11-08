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
    Adds ONE new edit to a solution, using one operator chosen among `operators`
    (default: RustSwapOperator and RustReplacementOperator).

    How the operator is picked, step by step
    ----------------------------------------
    1. With probability `probability` the mutation happens at all; otherwise the solution
       is returned unchanged.
    2. One operator is DRAWN at random. Each candidate's chance is its
       get_weight_initial() divided by the sum of the candidates' weights
       (swap 0.5 and replacement 0.5  ->  50% each).
    3. The drawn operator creates an edit against the solution's current AST and the edit is
       added with RPatch.add (which applies it to the AST and records it in the edit list).
    4. FALLBACK: if that operator has nothing eligible, or its edit cannot be applied,
       it is removed from the candidates and step 2 is repeated with the rest.
       So the operator that ends up used is the drawn one unless it could not act.

    After execute(), you can see what happened:
      last_operator  the operator class that produced the edit (None: no edit was added)
      last_edit      the edit that was added (None: no edit was added)
      last_trace     the steps above, e.g.
                     ['drew RustSwapOperator (50%)', 'not applicable',
                      'fell back to RustReplacementOperator', 'applied']
    """

    def __init__(self, probability: float, operators=None, scope_checker=None,
                 pair_checker=None, max_attempts: int = 10, rng: random.Random = None):
        super(RustMutation, self).__init__(probability=probability)
        self.operators = list(operators) if operators else [RustSwapOperator,
                                                            RustReplacementOperator]
        self.scope_checker = scope_checker  # e.g. only inside unsafe functions
        self.pair_checker = pair_checker    # only passed to operators whose create() accepts it
        self.max_attempts = max_attempts
        self.rng = rng or random.Random()
        self.last_operator = None
        self.last_edit = None
        self.last_trace = []

    @staticmethod
    def _weight(operator) -> float:
        getter = getattr(operator, 'get_weight_initial', None)
        return float(getter()) if getter is not None else 1.0

    def _draw(self, candidates):
        """Draw one operator from `candidates`; returns (operator, its chance in percent)."""
        weights = [self._weight(op) for op in candidates]
        if sum(weights) <= 0:
            weights = [1.0] * len(candidates)
        chosen = self.rng.choices(candidates, weights=weights, k=1)[0]
        percent = 100.0 * weights[candidates.index(chosen)] / sum(weights)
        return chosen, percent

    def _create_edit(self, operator, solution: RPatch):
        kwargs = dict(scope_checker=self.scope_checker,
                      rng=self.rng, max_attempts=self.max_attempts,
                      updated_contents=solution.ast)
        if self.pair_checker is not None and \
                'pair_checker' in inspect.signature(operator.create).parameters:
            kwargs['pair_checker'] = self.pair_checker
        return operator.create(solution.program, **kwargs)

    def execute(self, solution: RPatch, threshold_fitness=None) -> RPatch:
        """threshold_fitness: accepted because TypeConsistentGeneticAlgorithm passes it; unused."""
        Check.that(isinstance(solution, RPatch), "Solution type invalid")

        self.last_operator, self.last_edit, self.last_trace = None, None, []

        # 1. does the mutation happen at all?
        if self.rng.random() > self.probability:
            self.last_trace.append('mutation not triggered')
            return solution

        candidates = list(self.operators)
        while candidates:
            # 2. draw one operator
            operator, percent = self._draw(candidates)
            candidates.remove(operator)
            if len(candidates) + 1 == len(self.operators):      # the first draw
                self.last_trace.append(f'drew {operator.__name__} ({percent:.0f}%)')
            else:                                                # after a fallback
                self.last_trace.append(f'fell back to {operator.__name__}')

            # 3. let it create an edit and add it to the patch
            edit = self._create_edit(operator, solution)
            if solution.add(edit):       # False: nothing eligible, or the edit failed to apply
                self.last_operator, self.last_edit = operator, edit
                self.last_trace.append('applied')
                return solution

            # 4. fallback: continue with the operators not tried yet
            self.last_trace.append('not applicable')

        self.last_trace.append('no operator could produce an edit')
        return solution

    def get_name(self):
        return 'Rust mutation (' + ', '.join(op.__name__ for op in self.operators) + ')'


RustSwapMutation = RustMutation   # old name, kept so existing imports keep working