from pyggi.base.edit import AbstractEdit
from jmetal.core.problem import Problem
from .cpatch import CPatch
from .cprogram import CProgram
import random

class CProblem(Problem):
    """ Problem C
            What is target description

    """

    def __init__(self, program: CProgram, number_of_variables: int = 1):
        """
        :param number_of_variables: Number of decision variables of the problem.
        :param program: Program object from pyggi
        """
        super(CProblem, self).__init__()
        # Done in super
        #self.reference_front: List[S] = []
        #self.directions: List[int] = []
        #self.labels: List[str] = []

        self.program = program
        self.number_of_variables = 1
        self.number_of_objectives = 1
        self.directions = [self.MINIMIZE]
        self.labels = ['Fitness']

        self.number_of_constraints = 0

    def number_of_variables(self) -> int:
        return self.number_of_variables

    def number_of_objectives(self) -> int:
        return self.number_of_objectives

    def number_of_constraints(self) -> int:
        return self.number_of_constraints

    def evaluate(self, solution: CPatch) -> CPatch:
        '''
        Evaluates a CPatch and returns the fitness
        '''
        result = self.program.evaluate_solution(solution, self.program.test_command)
        # Check if result is valid # TODO #
        solution.objectives[0] = result.fitness

        return solution

    def create_solution(self) -> CPatch:
        '''
        Creates a new solution object with a random edit operator
        '''
        solution = CPatch(self.program, number_of_variables=1, number_of_objectives=1)
        #print(self.program)
        edit_operator: AbstractEdit = random.choice(self.program.operators)
        opr = edit_operator.create(self.program)
        solution.add(opr)
        print("solution obj",solution,"\nsoln diff",solution.diff)
        return solution
    def name(self):
        return 'CProblem'
