import inspect
import random

from .cproblem import CProblem
from .rpatch import RPatch
from .rprogram import RProgram


class RProblem(CProblem):
    """CProblem whose solutions are RPatch. evaluate() is inherited."""

    def __init__(self, program: RProgram, scope_checker=None, pair_checker=None,
                 rng: random.Random = None, max_attempts: int = 10):
        super(RProblem, self).__init__(program)
        self.scope_checker = scope_checker
        self.pair_checker = pair_checker    # only passed to operators whose create() accepts it
        self.max_attempts = max_attempts
        self.rng = rng or random.Random()

    def create_solution(self, rng=None) -> RPatch:
        """
        The original AST with one random operator applied (program.operators must be set).
        `rng` is accepted because newer jMetal versions call create_solution(rng); it is
        ignored, the problem uses its own self.rng (so the seed of testing.py is respected).
        """
        solution = RPatch(self.program, number_of_variables=1, number_of_objectives=1)
        operator = self.rng.choice(self.program.operators)
        kwargs = dict(scope_checker=self.scope_checker, rng=self.rng,
                      max_attempts=self.max_attempts, updated_contents=solution.ast)
        if self.pair_checker is not None and \
                'pair_checker' in inspect.signature(operator.create).parameters:
            kwargs['pair_checker'] = self.pair_checker
        edit = operator.create(self.program, **kwargs)
        solution.add(edit)
        return solution

    def name(self):
        return 'RProblem'