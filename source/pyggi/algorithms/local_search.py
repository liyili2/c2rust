import random
import time, os
from abc import ABCMeta, abstractmethod

from antlr4 import CommonTokenStream, InputStream
from RustParser.AST_Scripts.antlr.RustLexer import RustLexer
from RustParser.AST_Scripts.antlr.RustParser import RustParser
from RustParser.AST_Scripts.ast.Transformer import Transformer
from RustParser.AST_Scripts.ast.TypeChecker import TypeChecker
from pyggi.tree.tree import StmtDeletion, StmtInsertion, StmtReplacement
from ..base import Patch, Algorithm

def pretty_print_ast(node, indent=0, visited=None):
    if visited is None:
        visited = set()

    lines = []
    prefix = ' ' * indent

    if isinstance(node, (str, int, float, bool, type(None))):
        return f"{prefix}{repr(node)}"

    node_id = id(node)
    if node_id in visited:
        return f"{prefix}<Cycle: {type(node).__name__}>"

    visited.add(node_id)

    if isinstance(node, list):
        for n in node:
            lines.append(pretty_print_ast(n, indent, visited))
    elif hasattr(node, '__dict__'):
        lines.append(f"{prefix}{type(node).__name__}:")
        for attr, value in vars(node).items():
            if attr == "parent":
                continue
            lines.append(f"{prefix}  {attr}:")
            lines.append(pretty_print_ast(value, indent + 4, visited))
    else:
        lines.append(f"{prefix}{repr(node)}")

    return '\n'.join(lines)

class LocalSearch(Algorithm):
    """
    Local Search (Abstact Class)

    All children classes need to override

    * :py:meth:`get_neighbour`

    .. hint::
        Example of LocalSearch class. ::

            class MyLocalSearch(LocalSearch):
                def get_neighbour(self, patch):
                    import random
                    if len(patch) > 0 and random.random() < 0.5:
                        patch.remove(random.randrange(0, len(patch)))
                    else:
                        edit_operator = random.choice([LineDeletion, LineInsertion, LineReplacement])
                        patch.add(edit_operator.create(program, method="random"))
                    return patch

                def stopping_criterion(self, iter, patch):
                    return patch.elapsed_time < 100

            local_search = MyLocalSearch(program)
            results = local_search.run(warmup_reps=5, epoch=3, max_iter=100, timeout=15)
    """
    def is_better_than_the_best(self, fitness, best_fitness):
        print("is_better_than_the_best: ", fitness, best_fitness)
        """
        :param fitness: The fitness value of the current patch
        :param best_fitness: The best fitness value ever in the current epoch
        :return: If the current fitness are better than the best one, return True.
          False otherwise.
        :rtype: bool
        """
        if best_fitness is None:
            return True
        is_better_than_the_best = fitness <= best_fitness
        return is_better_than_the_best

    def stopping_criterion(self, iter, fitness):
        """
        :param int iter: The current iteration number in the epoch
        :param patch: The patch visited in the current iteration
        :type patch: :py:class:`.Patch`
        :return: If the satisfying patch is found or the budget is out of run,
          return True to stop the current epoch. False otherwise.
        :rtype: bool
        """
        return False

    @abstractmethod
    def get_neighbour(self, patch):
        """
        :param patch: The patch that the search is visiting now
        :type patch: :py:class:`.Patch`
        :return: The next(neighbour) patch
        :rtype: :py:class:`.Patch`

        .. hint::
            An example::

                return patch.add(LineDeletion.random(program))
        """
        pass

    def run(self, warmup_reps=1, epoch=5, max_iter=100, timeout=15, verbose=True):
        """
        It starts from a randomly generated candidate solution
        and iteratively moves to its neighbouring solution with
        a better fitness value by making small local changes to
        the candidate solution.

        :param int warmup_reps: The number of warming-up test runs to get
          the base fitness value. For some properties, non-functional
          properties in particular, fitness value cannot be fixed. In that
          case, the base fitness value should be acquired by averaging the
          fitness values of original program.
        :param int epoch: The total epoch
        :param int max_iter: The maximum iterations per epoch
        :param float timeout: The time limit of test run (unit: seconds)
        :return: The result of searching(Time, Success, FitnessEval, InvalidPatch, BestPatch)
        :rtype: dict(int, dict(str, ))
        """
        if verbose:
            self.program.logger.info(self.program.logger.log_file_path)

        warmup = list()
        empty_patch = Patch(self.program)
        for i in range(warmup_reps):
            result = self.program.evaluate_patch(empty_patch, timeout=timeout)
            if result.status == 'SUCCESS':
                warmup.append(result.fitness)
        original_fitness = float(sum(warmup)) / len(warmup) if warmup else None
        original_fitness = None

        if verbose:
            self.program.logger.info(
                "The fitness value of original program: {}".format(original_fitness))

        result = []

        if verbose:
            self.program.logger.info("Epoch\tIter\tStatus\tFitness\tPatch")

        for cur_epoch in range(1, epoch + 1):
            # Reset Search
            self.setup()
            cur_result = {}
            best_patch = empty_patch
            best_fitness = original_fitness

            # Result Initilization
            cur_result['BestPatch'] =None
            cur_result['Success'] = False
            cur_result['FitnessEval'] = 0
            cur_result['InvalidPatch'] = 0
            cur_result['diff'] = None

            start = time.time()
            for cur_iter in range(1, max_iter + 1):
                patch = self.get_neighbour(best_patch.clone())
                run = self.program.evaluate_patch(patch, timeout=timeout)

                if run.fitness is not None:
                    cur_result['FitnessEval'] += run.fitness

                if run.status != 'SUCCESS':
                    cur_result['InvalidPatch'] += 1
                    update_best = False
                else:
                    print("update_best")
                    update_best = self.is_better_than_the_best(run.fitness, best_fitness)

                if update_best:
                    print("best_fitness", best_fitness)
                    best_fitness, best_patch = run.fitness, patch

                if verbose:
                    self.program.logger.info("{}\t{}\t{}\t{}{}\t{}".format(
                        cur_epoch, cur_iter, run.status, '*' if update_best else '',
                        run.fitness, patch))

                if run.fitness is not None and self.stopping_criterion(cur_iter, run.fitness):
                    cur_result['Success'] = True
                    # with open("mutated_ast"+ cur_iter +".txt", "w", encoding="utf-8") as f:
                    #   f.write(pretty_print_ast(run.program))
                    break

                # print("diff: ", patch.diff())

            cur_result['Time'] = time.time() - start

            if best_patch:
                cur_result['BestPatch'] = best_patch
                cur_result['BestFitness'] = best_fitness
                # print("best patch: ", pretty_print_ast(best_patch.program.trees[best_patch.program.main_file]))
                # cur_result['diff'] = self.program.diff(best_patch)
                # cur_result['diff'] = None

            result.append(cur_result)
            print("=== PATCHED CODE ===", self.program.path)

        return result
