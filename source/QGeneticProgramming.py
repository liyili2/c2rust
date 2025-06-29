from RustCode.AST_Scripts.XMLVisitor import XMLVisitor
from RustCode.simulator import Simulator, Coq_nval, CalInt
from repairCode.crossover import QCrossover
from repairCode.mutation import QMutation
from repairCode.cpatch import QPatch
from Source.repairCode.program import QProblem

from pyggi.base import AbstractProgram

import unittest
#from antlr4 import *
from RustCode.AST_Scripts.ExpListener import ExpListener
from RustCode.AST_Scripts.ExpLexer import ExpLexer
from RustCode.AST_Scripts.ExpParser import ExpParser
from RustCode.AST_Scripts.XMLVisitor import XMLVisitor

from argparse import ArgumentParser
import pytest
import random
import xml.etree.ElementTree as ET

class XMLEngine:
    def __init__(self, xml_content):
        self.xml_content = xml_content
        self.tags = self.extract_tags()

    def extract_tags(self):
        tags = set()
        root = ET.fromstring(self.xml_content)

        for statement in root.findall(".//statement"):
            # Extracting tags within each statement
            tags.update(tag.tag for tag in statement)

        return list(tags)

    def get_tags(self):
        return self.tags     

# Fixture to provide input_states to tests
@pytest.fixture
def input_states_fixture():
    return input_states

# Fixture to provide true_states to tests
@pytest.fixture
def true_states_fixture():
    return true_states

class QProgram(AbstractProgram):
    '''
    Subclass for Program
    '''
    def __init__(self, arguments):
        super().__init__(arguments)

    
    def evaluate_solution(self, solution, build_command):
        """
        Evaluate the fitness of a solution.

        Parameters:
        - solution: QPatch
            The solution to evaluate.
        - build_command: str?

        Returns:
        - float
            The fitness score.
        """

        # Number of qubits
        x = 128

        # Initialize Simulator
        simulator = Simulator()

        correct_predictions = 0

        for _ in range(x):
            # Randomly generate a boolean value
            b = random.choice([True, False])

            # Create an instance of Coq_nval
            v1 = Coq_nval(b, r=0)

            # Pass the instance to the Simulator
            v2 = simulator.simulate(v1, x)
            # Hard Code Test
            # Call pyTest HERE 
            if CalInt(v2, x) == x + pow(2, 10) % pow(2, x):
                correct_predictions += 1

        fitness = correct_predictions / x

        return fitness

def main(args):
    # File path to the quantum program
    # quantum_program_path = 'path/quantum_program.py'

    # with open(quantum_program_path, 'r') as file:
    #     source_code = quantum_program_path.read()

    # Generate solutions
    i_stream = InputStream("X (x,0) ; CU (x,0) (CU (x,1) (X (y,1)))")
    lexer = ExpLexer(i_stream)
    t_stream = CommonTokenStream(lexer)
    parser = ExpParser(t_stream)
    tree = parser.program()
    xml = XMLVisitor()
    problem_instance = tree.accept(xml)

    # Define genetic operators
    mutation = QMutation(problem_instance)
    crossover = QCrossover(problem_instance)

    # Define the genetic algorithm
    algorithm = GA(problem_instance, mutation=mutation, crossover=crossover)
    # Add if conditionals for other algorithims

    #
    logging = Logging(problem_instance)

    # Run the genetic improvement process
    algorithm.run(logging=logging)

    best_solution = algorithm.best

    # Retrieve the best quantum program
    best_program = best_solution.to_real()
    print(best_program)


if __name__ == "__main__":
    """
    Initialize default values 
    """
    algorithms = ['GA', 'SA', 'RS', 'NSGAII']
    algo = algorithms[0]
    epochs = 2
    iter = 100
    pop = 10
    """ 
    Below are the list of command-line (Program) parameters that can be 
        received during a run.
    If a command-line parameter is not provided, the default 
        value given below will be used.
    """
    parser = ArgumentParser(description='PyGGI CRN Repair Example')
    # Subject
    parser.add_argument('--project_path', type=str, default='XXX')
    parser.add_argument('--algo', type=str, default=algo)
    parser.add_argument('--subject', type=str, default="H1")
    parser.add_argument('--model', type=str, default="101")
    parser.add_argument('--somo', type=str, default="SO")    
    parser.add_argument('--target', type=float, default=0, help='Target Fitness')
    parser.add_argument('--jobid', type=str, default='0')
    # Parameters
    parser.add_argument('--probs', type=int, default=0, help='1: Use localization probabilities; 0: Random')
    parser.add_argument('--pop', type=int, default=pop, help='Population for GA')
    parser.add_argument('--mmo_wgh', type=float, default=1, help='MMO weight')
    parser.add_argument('--mutation', type=float, default=0.9)
    parser.add_argument('--crossover', type=float, default=0.9)
    parser.add_argument('--nspec', type=int, default=2,
                        help='Number of ingredients')
    parser.add_argument('--timeout', type=float, default=8,
                        help='time to force-terminate programs if they don\'t end regularly')
    parser.add_argument('--epochs', type=int, default=epochs,
                        help='total epoch(default: 10)')
    parser.add_argument('--iter', type=int, default=iter,
                        help='Generations or iterations per epoch')
    ############
    parser.add_argument('--debug', type=int, default=0,
                        help='In debug mode (1) or or not (0)')
    arg_prs = parser.parse_args()
    arg_prs.somo = "MMO"
    if arg_prs.algo in ["GA", "SA", "RS"]:
        arg_prs.somo = "SO"
    # Call Program
    main(arg_prs)
