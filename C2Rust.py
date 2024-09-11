"""
Automated program repair ::
"""
import argparse
import logging
# For pyggi default program + repair
from pyggi.tree import XmlEngine
from pyggi.tree import StmtReplacement, StmtInsertion, StmtDeletion  # Default Python program support
# From jMetalpy
from jmetal.algorithm.singleobjective import GeneticAlgorithm
from jmetal.operator import BinaryTournamentSelection
from jmetal.util.termination_criterion import StoppingByEvaluations
# For modified program + repair
from repairCode.cprogram import CProgram
from repairCode.cproblem import CProblem
from repairCode.mutation import PyGGiMutation
from repairCode.crossover import PyGGiCrossover
# Custom Operators
#from repairCode.operators import CGateReplacement, CGateInsertion, CGateDeletion


class MyXmlEngine(XmlEngine):
    """
    PyGGI uses its own engine. Then, it allows customizing some
    functionalities of engine classes through the use of subclasses.
    Subclass for XmlEngine
    """

    @classmethod
    def process_tree(cls, tree, tags):
        """
        Not used!!
        process_tree is used to customize AST for PyGGI
           select_tags removes all tags which are not in the tags list
        """
        stmt_tags = tags
        cls.select_tags(tree, keep=stmt_tags)
        cls.rotate_newlines(tree)

class StoppingByEvaluationORFitness(StoppingByEvaluations):
    """
    Stopping by Evaluation or Fitness
    Default Target Fitness is 0
    """
    def __init__(self, max_evaluations: int, target_fitness: float = 0):
        super(StoppingByEvaluationORFitness, self).__init__(target_fitness)
        self.target_fitness = target_fitness
        self.max_evaluations = max_evaluations
        self.evaluations = 0
        self.fitness = 1000000

    def update(self, *args, **kwargs):
        self.evaluations = kwargs["EVALUATIONS"]
        self.fitness     = kwargs["SOLUTIONS"].objectives[0]

    @property
    def is_met(self):
        return self.evaluations >= self.max_evaluations or self.fitness <= self.target_fitness



def parser_generator():
    parser = argparse.ArgumentParser(description='PYGGI Bug Repair Example')
    parser.add_argument('--project_path', type=str,   default='Benchmarks/Aggregate')
    #parser.add_argument('--project_path', type=str,   default='Benchmark/vqo_small_circuit_ex')
    parser.add_argument('--algorithm',    type=str,   default='ga')
    parser.add_argument('--epoch',        type=int,   default=1,            help='total epoch(default: 1)')
    parser.add_argument('--iter',         type=int,   default=50,           help='total iterations per epoch(default: 100)')
    parser.add_argument('--pop',          type=int,   default=8,            help='population size(default: 10)')
    parser.add_argument('--mutation',     type=float, default=1,            help='mutation rate(default: 0.1)')
    parser.add_argument('--crossover',    type=float, default=1,            help='crossover rate(default: 0.9)')
    parser.add_argument('--sel',          type=str,   default='tournament', help='selection operator(default: tournament)')
    parser.add_argument('--tags',         type=str,   default='[]',         help='XML tags (default: [])')
    parser.add_argument('--operators',    type=str,   default='[]',         help='Operators (default: [])')
    parser.add_argument('--targetfitness', type=str,   default='0',         help='Target Fitness (default: 0)')
    return parser.parse_args()
1


if __name__ == "__main__":
    args = parser_generator()
    # Make a Program
    program = CProgram(args.project_path)
    program.operators = args.operators  # Need to parse args into a list
    program.operators = [StmtDeletion, StmtInsertion, StmtReplacement]
    #program.operators = [CGateInsertion]
    program.tags = args.tags
    # Make a Problem
    problem = CProblem(program, number_of_variables=1)
    # Fault Localization (Future) / Check for correctness (Future)

    # Choose which algorithm
    if args.algorithm == 'ga':
        # Genetic Algorithm
        algorithm = GeneticAlgorithm(problem,
                                     population_size=args.pop,
                                     offspring_population_size=args.pop,
                                     mutation=PyGGiMutation(args.mutation),
                                     crossover=PyGGiCrossover(args.crossover),
                                     selection=BinaryTournamentSelection(),
                                     termination_criterion=StoppingByEvaluationORFitness(max_evaluations=args.iter, target_fitness=0))
        # TODO StoppingByEvaluationORFitness
    else:
        # Invalid Algorithm
        raise Exception('Invalid Algorithm')
    # Run the algorithm
    algorithm.run()
    solution = algorithm.get_result()
    EditList = algorithm.solutions
    print("EditList\n" , EditList)
    print("======================RESULT======================")
    print(solution)
    print(solution.program)
    #program.remove_tmp_variant()
