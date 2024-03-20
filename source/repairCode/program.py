from jmetal.core.problem import Problem
from jmetal.core.solution import Solution
from .patch import PyggiPatch
from pyggi.line import LineProgram
from pyggi.tree import TreeProgram
from pyggi.base.edit import AbstractEdit
from pyggi.tree import XmlEngine
from typing import Generic, TypeVar, List
import random
import re


class PyggiProblem(Problem):
    """ Problem Q
            What is target description

    """

    def __init__(self, number_of_variables: int = 8):
        """
        :param number_of_variables: Number of decision variables of the problem.
        :param prg: Program object from pyggi
        """
        super(PyggiProblem, self).__init__()
        self.program = program
        self.number_of_variables = 1
        self.number_of_objectives = 1
        self.obj_directions = [self.MINIMIZE]
        self.obj_labels = ['Fitness']
        if program.args.somo == "MO":
            self.number_of_objectives = 2
            self.obj_directions = [self.MINIMIZE, self.MINIMIZE]
            self.obj_labels = ['?', 'Fail rate']

        self.number_of_constraints = 0

    def number_of_variables(self) -> int:
        return self.number_of_variables

    def number_of_objectives(self) -> int:
        return self.number_of_objectives

    def number_of_constraints(self) -> int:
        return self.number_of_constraints

    def evaluate(self, solution: PyggiPatch) -> PyggiPatch:
        fitness = self.prg.evaluate_solution(solution, self.program.build_command)
        solution.fitness = 0
        solution.objectives[0] = solution.fitness

        return solution

    def create_solution(self) -> PyggiPatch:
        solution = PyggiPatch(self.program, number_of_variables=1, number_of_objectives=1)
        edit_operator: AbstractEdit = random.choice(self.program.operators) 
        opr = edit_operator.create(self.program)
        solution.add(opr)

        return solution

    def generate_neighbor(self, solution: PyggiPatch) -> PyggiPatch:
        rnd = random.random()
        lp = len(solution)
        if lp == 0 or rnd < 0.33:
            edit_operator = random.choice(self.prg.operators)
            solution.add(edit_operator.create(self.prg))
        elif lp > 1 and rnd < 0.66:
            solution.remove(random.randrange(0, lp))
        else:
            edit_operator = random.choice(self.program.operators)
            pn = random.randrange(0, lp)
            solution.edit_list[pn] = edit_operator.create(self.prg)

        return solution

    def name(self):
        return 'PyggiProblem'
    
class MyLineProgram(LineProgram):
    pass

class MyTreeProgram(TreeProgram):
    pass

class MyProgram(MyTreeProgram, Problem):
    """
    
    """
    number_of_variables = 1
    number_of_objectives = 1
    number_of_constraints = 0

    def __init__(self, project_path):
        """
        :param number_of_variables: Number of decision variables of the problem.
        :param prg: Program object from pyggi
        """
        super(MyTreeProgram, self).__init__(project_path)
        self.path                  = project_path
        self.number_of_variables   = 1
        self.number_of_objectives  = 1
        self.obj_directions        = [self.MINIMIZE]
        self.obj_labels            = ['Fitness']
        self.number_of_constraints = 0


    def compute_fitness(self, result, return_code=0, stdout=0, stderr=0, elapsed_time=0):
        """
        Given a program, compute the fitness
        """


        '''
        m = re.findall("runtime: ([0-9.]+)", stdout)
        if len(m) > 0:
            runtime = m[0]
            failed = re.findall("([0-9]+) failed", stdout)
            pass_all = len(failed) == 0
            failed = int(failed[0]) if not pass_all else 0
            result.fitness = failed
        else:
            result.status = 'PARSE_ERROR'
        '''

    #def get_engine(cls, file_name=""):
    #   return MyXmlEngine

    # jMetalpy functions        
    def create_solution(self) -> PyggiPatch:
        new_solution = PyggiPatch(self, number_of_variables=1, number_of_objectives=1)
        return new_solution

    def evaluate(self, patch) -> PyggiPatch:
        """
        Evaluates a program, and returns the fitness
        """
        # Run Program and get the RunResult Object
        #result = self.evaluate_patch(patch, timeout=15)
        fitness = 0
        # Save to Solution Object
        patch.objectives[0] = fitness
        
        return patch
    
    def number_of_variables(self) -> int:
        return self.number_of_variables

    
    def number_of_objectives(self) -> int:
        return self.number_of_objectives

    def number_of_constraints(self) -> int:
        return self.number_of_constraints
    
    def name(self) -> str:
        return "MyProgram"