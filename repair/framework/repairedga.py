"""
Genetic algorithms for the Rust/PyGGI setup: the reference RepairedGeneticAlgorithm family,
copied unchanged in logic. They subclass jMetal's GeneticAlgorithm, so jMetal is still the
engine underneath; only the generation loop is customised.

    GeneticAlgorithm                      (jMetal)
      -> RepairedGeneticAlgorithm         selection works on a copy of the population
        -> TypeConsistentGeneticAlgorithm reproduction validates / repairs every child
          -> LoggingGeneticAlgorithm      replacement prints the best fitnesses
            -> TopKSelectorGeneticAlgorithm only the k best survive into replacement

What the program (RProgram) and the mutation must provide:
    program.update_operators(solution, max_depth, max_width) -> contents   (raises if inconsistent)
    program.validate(contents) -> bool
    mutation.execute(solution, threshold_fitness)
"""
import copy
import random
from functools import cmp_to_key
from typing import List

from jmetal.algorithm.singleobjective import GeneticAlgorithm
from jmetal.algorithm.singleobjective.genetic_algorithm import S


class RepairedGeneticAlgorithm(GeneticAlgorithm):
    def selection(self, population: List[S]):
        # Select from a deep copy: the chosen parents are then independent objects, so
        # crossover / mutation (which edit solutions in place) never touch the population.
        return super(RepairedGeneticAlgorithm, self).selection(copy.deepcopy(population))


class TypeConsistentGeneticAlgorithm(RepairedGeneticAlgorithm):
    def __init__(self, initial_threshold_fitness: float = 0.0, threshold_depth: int = 20,
                 threshold_width: int = 20, *args, **kwargs):
        super(TypeConsistentGeneticAlgorithm, self).__init__(*args, **kwargs)
        self.initial_threshold_fitness = initial_threshold_fitness
        self.threshold_depth = threshold_depth
        self.threshold_width = threshold_width

    def reproduction(self, mating_population: List[S]) -> List[S]:
        number_of_parents_to_combine = self.crossover_operator.get_number_of_parents()

        if len(mating_population) % number_of_parents_to_combine != 0:
            raise Exception("Wrong number of parents")

        offspring_population = []
        for i in range(0, self.offspring_population_size, number_of_parents_to_combine):
            parents = []
            for j in range(number_of_parents_to_combine):
                parents.append(mating_population[i + j])

            offspring = self.crossover_operator.execute(parents)

            for idx, solution in enumerate(offspring):
                try:
                    # repair + check the child; any failure sends us to the except branch
                    new_contents = self.problem.program.update_operators(
                        solution, self.threshold_depth, self.threshold_width)
                    if not self.problem.program.validate(new_contents):
                        raise Exception("Invalidated solution")
                except Exception as e:
                    print(f"Failed solution: {str(e)}")
                    solution = parents[idx]      # invalid child: fall back to its parent
                self.mutation_operator.execute(solution, self.initial_threshold_fitness)
                offspring_population.append(solution)
                if len(offspring_population) >= self.offspring_population_size:
                    break

        return offspring_population


class LoggingGeneticAlgorithm(TypeConsistentGeneticAlgorithm):
    def replacement(self, population: List[S], offspring_population: List[S]) -> List[S]:
        population.extend(offspring_population)
        random.shuffle(population)   # random order first, so equal fitnesses are ranked by chance
        population.sort(key=cmp_to_key(self.solution_comparator.compare))
        print("HIGHEST FITNESSES",
              [solution.objectives[0] for solution in population[: self.population_size]])
        return population[: self.population_size]


class TopKSelectorGeneticAlgorithm(LoggingGeneticAlgorithm):
    def __init__(self, k: int, *args, **kwargs) -> None:
        super(TopKSelectorGeneticAlgorithm, self).__init__(*args, **kwargs)
        self.k = k

    def replacement(self, population: List[S], offspring_population: List[S]) -> List[S]:
        # only the first k of the current population (the best, once it is sorted) survive
        return super(TopKSelectorGeneticAlgorithm, self).replacement(
            population[:self.k], offspring_population)