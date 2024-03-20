"""
Automated program repair ::
"""
import sys
import random
import argparse

# For pyggi default program + repair
from pyggi.line import LineReplacement, LineInsertion, LineDeletion
from pyggi.tree import XmlEngine
from pyggi.tree import StmtReplacement, StmtInsertion, StmtDeletion
from pyggi.algorithms import LocalSearch
# For modified program + repair
from repairCode.crossover import PyggiCrossover
from repairCode.mutation import NullMutation
from repairCode.patch import PyggiPatch
from repairCode.operators import QGateReplacement, QGateInsertion, QGateDeletion
from repairCode.program import MyLineProgram, MyTreeProgram, MyProgram
from jmetal.algorithm.singleobjective import GeneticAlgorithm
from jmetal.operator import BinaryTournamentSelection
from jmetal.util.termination_criterion import StoppingByQualityIndicator
from jmetal.core.quality_indicator import FitnessValue

class MyFitnessValue(FitnessValue):
    """
    
    """
    is_minimization = True

    def __init__(self, is_minimization: bool = True):
        super().__init__(is_minimization)

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



class MyTabuSearch(LocalSearch):
    """
    
    """
    def setup(self):
        self.tabu = []

    def get_neighbour(self, patch):
        while True:
            temp_patch = patch.clone()
            if len(temp_patch) > 0 and random.random() < 0.5:
                temp_patch.remove(random.randrange(0, len(temp_patch)))
            else:
                edit_operator = random.choice(self.operators)
                temp_patch.add(edit_operator.create(self.program, method="weighted"))
            if not any(item == temp_patch for item in self.tabu):
                self.tabu.append(temp_patch)
                break
        return temp_patch

    def is_better_than_the_best(self, fitness, best_fitness):
        return fitness < best_fitness

    def stopping_criterion(self, iter, fitness):
        return fitness == 0

class MyGA(GeneticAlgorithm):
    """
    Use the default JMetal GA for now
    """
    def stopping_criterion(self, iter, fitness):
        return fitness == 0

if __name__ == "__main__":
    print("Starting")
    parser = argparse.ArgumentParser(description='PYGGI Bug Repair Example')
    parser.add_argument('--project_path', type=str, default='../Benchmark/vqo_small_circuit_ex')
    parser.add_argument('--mode', type=str, default='line')
    parser.add_argument('--epoch', type=int, default=30,
        help='total epoch(default: 30)')
    parser.add_argument('--iter', type=int, default=100,
        help='total iterations per epoch(default: 100)')
    args = parser.parse_args()
    #assert args.mode in ['line', 'tree']

    # Choose which algorithm
    if args.mode == 'ga':
        #program = QProgram(args.project_path)
        #program = MyProgram(args.project_path)
        program = MyProgram(args.project_path)
        ga = MyGA(program, 8, 8, NullMutation(), PyggiCrossover(.5))
        # Uses JMetal defaults if not overwritten
        #ga.mutation_operator = Mutation()
        #ga.crossover_operator = Crossover()
        #ga.selection = BinaryTournamentSelection()

        ga.program.operators = [QGateReplacement]
        
        # Target Fitness, Precision
        ga.termination_criterion = StoppingByQualityIndicator(MyFitnessValue, 0, 1.0)
        result = ga.run()

    elif args.mode == 'line':
        program = MyLineProgram(args.project_path)
        tabu_search = MyTabuSearch(program)
        tabu_search.operators = [LineReplacement, LineInsertion, LineDeletion]
        result = tabu_search.run(warmup_reps=1, epoch=args.epoch, max_iter=args.iter, timeout=10)
    elif args.mode == 'tree':
        program = MyTreeProgram(args.project_path)
        tabu_search = MyTabuSearch(program)
        tabu_search.operators = [StmtReplacement, StmtInsertion, StmtDeletion]
        result = tabu_search.run(warmup_reps=1, epoch=args.epoch, max_iter=args.iter, timeout=10)

    
    print("======================RESULT======================")
    print(result)
    program.remove_tmp_variant()
