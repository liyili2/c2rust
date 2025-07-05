"""
Automated Chemical Reaction Network repair tool::
"""
from datetime import datetime
import random, time, os, sys, re
from argparse import ArgumentParser
from pyggi.base import AbstractProgram, Patch
from pyggi.tree import XmlEngine, StmtReplacement, StmtDeletion, NewReaction, StmtInsertion
from pyggi import INF
from copy import deepcopy
# jmetal
from jmetal.algorithm.multiobjective.nsgaii import NSGAII
from jmetal.crnrepair import CrnRepair
from jmetal.operator.crossover import CRNCrossover
from jmetal.algorithm.singleobjective.genetic_algorithm import GeneticAlgorithm
from jmetal.algorithm.singleobjective.simulated_annealing import SimulatedAnnealing
from jmetal.algorithm.multiobjective.random_search import RandomSearch
from jmetal.util.termination_criterion import StoppingByEvaluationsOrFitness
from jmetal.operator.mutation import CRNMutation
from jmetal.operator import BinaryTournamentSelection,  RandomSolutionSelection
from jmetal.util.solution import save_results, save_results_so


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


class MyTreeProgram(AbstractProgram):
    """
    Subclass for TreeProgram
    """

    def __init__(self, arguments):
        super().__init__(arguments)

    def setup(self):
        """
        When xml file is not provided, PyGGI uses srcml to prepare AST 
        from the target file. CRNRepair uses Matlab to prepare this. 
        For now, we are ignoring, if sbml is not provided
        """
        fname = os.path.join(self.tmp_path, self.target_files[0])
        if not os.path.exists(fname):
            print("please provide a valid sbml file: " + fname)
            sys.exit()
            pass

    @classmethod
    def get_engine(cls, file_name=""):
        """
        From PyGGI: returns the engine class
        CRNRepair tool uses only XmlEngine
        """
        return MyXmlEngine

    def compute_fitness(self, result, stdout="", first=False ):
        """
          :param self:
          :param result:
          :param return_code:
          :param stdout:
          :param stderr:
          :param elapsed_time:
        """
        #print(stdout)
        try:  # "Fitness: 600; Probabilities: reaction_1:0.70711; reaction_2:0.70711; mutant-new:0.70711; \n"
            pos1 = stdout.find("Fitness:")
            pos2 = stdout.find(";", pos1)
            result.fitness = float(stdout[pos1+8: pos2])
            if self.args.debug:
                print("ComputeFitness Location: ", result.fitness)
            if result.fitness < 0:
                self.err_cnt += 1
                result.fitness = INF

            # Calculate weigths if using localization
            self.initialize_weights(stdout, first)
        except:
            result.status = 'PARSE_ERROR'

def load_run_patch(prg, fname: str):
    """
      :param prg:
      :param fname:
    """
    # [NewReaction, StmtInsertion, StmtReplacement, StmtDeletion]
    mutations = read_file(fname)
    patch = Patch(prg)
    i = 0
    for mutation in mutations:
        m_arr = re.split("['(, )]", mutation)
        opr = str(m_arr[0])
        if opr == 'NewReaction':
            edit_opr = prg.operators[0]
            t_file, t_pos = str(m_arr[3]), int(m_arr[6])
            lm = len(m_arr)
            reactants = []
            k = 9
            for k in range(9, lm):
                if m_arr[k] == '->': break
                if m_arr[k] != '':
                    reactants.append(str(m_arr[k]))
            products = []
            for j in range(k + 1, lm):
                if not (m_arr[j] in ['', '\n']):
                    products.append(str(m_arr[j]))
            patch.add(edit_opr.create2(prg, t_file, t_pos, reactants, products))

        else:
            t_file, t_pos = str(m_arr[6]), int(m_arr[9])
            if opr == 'StmtDeletion':
                edit_opr = prg.operators[3]
                patch.add(edit_opr.create2(t_file, t_pos))
            elif opr == 'StmtReplacement':
                edit_opr = prg.operators[2]
                i_pos = int(m_arr[20])
                patch.add(edit_opr.create2(t_file, t_pos, i_pos))
            else:  # There are only 4 operators
                edit_opr = prg.operators[1]
                i_pos = int(m_arr[20])
                patch.add(edit_opr.create2(t_file, t_pos, i_pos))

        res = prg.evaluate_patch(patch, timeout=prg.args.timeout, partial=0)
        patch.fitness = res.fitness
        i += 1
        print("\nAdded mutation {}: {}".format(str(i), str(patch)))
        prg.copy_best(i, str(patch))

    print()


def run_main(args):
    """
      :param args:
    """
    program = MyTreeProgram(args)
    random.seed(program.timestamp)
    crn_subject = program.config['modelName'] + '-' + program.config['modelID']
    program.operators = [StmtInsertion, StmtReplacement, StmtDeletion]
    if args.new_reaction == 1:
        program.operators.append(NewReaction)
    if args.load_mutations == 'True':
        load_run_patch(program, "mutations.txt")
        program.remove_tmp_variant()
        sys.exit()

    print("Working on {} and the current job ID is {}.".format(crn_subject, program.timestamp))
    print("==============================================================")
    print("Given arguments: {}".format(str(program.args)))
    success_rate = 0
    elapsed_time = 0
    problem = CrnRepair(program, number_of_variables=args.pop)
    for epoch in range(1, args.epochs + 1):
        start_time = time.time()
        problem.initialize()
        problem.prg.initial_fitness = problem.prg.get_initial_fitness()
        print(f"Initial Fitness is: {problem.prg.initial_fitness:.1f}, elapsed time: {time.time() - start_time:.1f}")
        print("Epoch {} started at: {}".format(epoch, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        # Simulated Annealing
        if program.args.algo == 'SA':
            algorithm = SimulatedAnnealing(
                problem=problem,
                mutation=CRNMutation(probability=1, prg=program),
                termination_criterion=StoppingByEvaluationsOrFitness(args.iter, args.target, program.args.debug)
            )
        # Genetic Algorithm
        elif program.args.algo == 'GA':
            algorithm = GeneticAlgorithm(
                problem=problem,
                population_size=args.pop,
                offspring_population_size=args.pop,
                mutation=CRNMutation(probability=args.mutation, prg=program),
                crossover=CRNCrossover(probability=args.crossover),
                selection=BinaryTournamentSelection(),
                termination_criterion=StoppingByEvaluationsOrFitness(args.iter, args.target, program.args.debug)
            )
        # NSGAII
        elif program.args.algo == 'NSGAII':
            algorithm = NSGAII(
                problem=problem,
                population_size=args.pop,
                offspring_population_size=args.pop,
                mutation=CRNMutation(probability=args.mutation, prg=program),
                crossover=CRNCrossover(probability=args.crossover),
                termination_criterion=StoppingByEvaluationsOrFitness(args.iter, args.target, program.args.debug)
            )
        # Random Search
        else:
            algorithm = RandomSearch(
                problem=problem,
                termination_criterion=StoppingByEvaluationsOrFitness(args.iter, args.target)
            )

        algorithm.run()
        front = algorithm.get_result()
        elapsed_time += algorithm.total_computing_time
        p_name = "{}-{}_{}".format(algorithm.get_name(), crn_subject, program.timestamp)
        # print(f"There are  {program.err_cnt} failed evaluations")
        ret = False
        if args.somo == "SO":
            print("SingleObjective - Final Save to file")
            ret = save_results_so(front, algorithm, problem, program, p_name, epoch)
        elif args.somo == "MMO":
            print("MultiObjective - Final Save to file")
            ret = save_results(front, algorithm, problem, program, p_name, epoch)
        if ret:
            success_rate += 1
        for trg in program.target_files:
            src = program.path + "/" + trg + " "
            dst = program.tmp_path + "/" + trg
            os.system("cp " + src + dst)

    print("\n============================================================")
    print("Success rate of {:.1f}%; Elapsed time: {:.1f}"
          .format(success_rate / args.epochs * 100, elapsed_time))
    program.remove_tmp_variant()


if __name__ == "__main__":
    """ 
    Default tags to keep in AST, 
    Because the program is expected to provide sbml output, this tools keeps all the tags
    """
    algorithms = ['GA', 'SA', 'RS', 'NSGAII']
    default_tags = "listOfReactants reaction reactants species rate products listOfParameters "
    default_tags += "annotation SimBiology Version model listOfCompartments compartment "
    default_tags += "speciesReference listOfProducts kineticLaw math apply ci times parameter"
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
    parser.add_argument('--project_path', type=str, default='sample/crn-framework')
    parser.add_argument('--matlab1', type=str, default='matlab')
    parser.add_argument('--algo', type=str, default=algo)
    parser.add_argument('--subject', type=str, default="H1")
    parser.add_argument('--model', type=str, default="101")
    parser.add_argument('--somo', type=str, default="SO")
    parser.add_argument('--tags', type=str, default=default_tags)
    parser.add_argument('--mmo_wgh', type=float, default=1, help='MMO weight')
    parser.add_argument('--target', type=float, default=0, help='Target Fitness')
    parser.add_argument('--probs', type=int, default=0,
                        help='1: Use localization probabilities; 0: Random')
    parser.add_argument('--new_reaction', type=int, default=1,
                        help="1: Use new reaction operator")
    parser.add_argument('--pop', type=int, default=pop, help='Population for GA')
    parser.add_argument('--jobid', type=str, default='0')
    parser.add_argument('--load_mutations', type=str, default='False')
    parser.add_argument('--operationTags', type=str, default="speciesReference reaction")  #
    parser.add_argument('--engine', type=bool, default=True)
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
    parser.add_argument('--debug', type=int, default=0,
                        help='In debug mode (1) or or not (0)')

    arg_prs = parser.parse_args()
    arg_prs.somo = "MMO"
    if arg_prs.algo in ["GA", "SA", "RS"]:
        arg_prs.somo = "SO"

    run_main(arg_prs)