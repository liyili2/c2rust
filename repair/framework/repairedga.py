"""
Genetic algorithms for the Rust/PyGGI setup (RepairedGeneticAlgorithm family).
They subclass jMetal's GeneticAlgorithm, so jMetal is still the engine underneath; only the
generation loop is customised.

    GeneticAlgorithm                       (jMetal)
      -> RepairedGeneticAlgorithm          selection on copies; crossover -> mutation ("repair via
                                           the edit operators"); lineage labels; pipeline trace
        -> LoggingGeneticAlgorithm         replacement prints the best fitnesses
          -> TopKSelectorGeneticAlgorithm  only the k best of the old population survive

One generation, as a pipeline (every stage can be watched through the `trace` callback):

    selection      parents are picked from a COPY of the population
    crossover      RustSubtreeCrossover exchanges a subtree between two parents
    mutation       RustMutation adds a swap or a replacement edit        <- the "repair"
    evaluation     the offspring get their fitness
    survival       old population + offspring compete, the best survive

`trace(stage, solutions)` is called with stage one of
    "initial", "evaluation", "selection", "crossover", "mutation", "kept", "survival".
Each solution carries attributes["label"] (P<i> for the initial population, G<generation>.<i>
for offspring) and attributes["parents"] (labels of the two parents), so a solution can be
followed from stage to stage.
"""
import copy
import random
from functools import cmp_to_key
from typing import List

from jmetal.algorithm.singleobjective import GeneticAlgorithm
from jmetal.algorithm.singleobjective.genetic_algorithm import S


class RepairedGeneticAlgorithm(GeneticAlgorithm):
    def __init__(self, *args, trace=None, **kwargs):
        super(RepairedGeneticAlgorithm, self).__init__(*args, **kwargs)
        self.trace = trace          # optional callable(stage: str, solutions: list)
        self.generation = 0

    def _emit(self, stage: str, solutions: List[S]):
        if self.trace is not None:
            self.trace(stage, solutions)

    # -- initial population ---------------------------------------------------------------
    def create_initial_solutions(self, *args, **kwargs) -> List[S]:
        solutions = super(RepairedGeneticAlgorithm, self).create_initial_solutions(*args, **kwargs)
        for i, solution in enumerate(solutions):
            solution.attributes["label"] = f"P{i}"
            solution.attributes["parents"] = []
        self._emit("initial", solutions)
        return solutions

    # -- 1. selection ---------------------------------------------------------------------
    def selection(self, population: List[S]):
        self.generation += 1
        # Select from a deep copy: the chosen parents are then independent objects, so
        # crossover / mutation (which edit solutions in place) never touch the population.
        selected = super(RepairedGeneticAlgorithm, self).selection(copy.deepcopy(population))
        self._emit("selection", selected)
        return selected

    # -- 2. crossover and 3. mutation -------------------------------------------------------
    def reproduction(self, mating_population: List[S]) -> List[S]:
        number_of_parents_to_combine = self.crossover_operator.get_number_of_parents()

        if len(mating_population) % number_of_parents_to_combine != 0:
            raise Exception("Wrong number of parents")

        offspring_population = []
        after_crossover = []        # snapshots taken before the mutation, only when tracing
        for i in range(0, self.offspring_population_size, number_of_parents_to_combine):
            parents = [mating_population[i + j] for j in range(number_of_parents_to_combine)]

            for child in self.crossover_operator.execute(parents):
                if len(offspring_population) >= self.offspring_population_size:
                    break
                child.attributes["label"] = f"G{self.generation}.{len(offspring_population)}"
                child.attributes["parents"] = [p.attributes.get("label") for p in parents]
                if self.trace is not None:
                    after_crossover.append(copy.deepcopy(child))
                # "repair via the operators": the mutation adds one swap or replacement edit
                self.mutation_operator.execute(child)
                offspring_population.append(child)

        self._emit("crossover", after_crossover)
        self._emit("mutation", offspring_population)
        return offspring_population

    # -- 4. evaluation --------------------------------------------------------------------
    def evaluate(self, population: List[S]) -> List[S]:
        population = super(RepairedGeneticAlgorithm, self).evaluate(population)
        self._emit("evaluation", population)
        return population

    # -- 5. survival ----------------------------------------------------------------------
    def replacement(self, population: List[S], offspring_population: List[S]) -> List[S]:
        survivors = super(RepairedGeneticAlgorithm, self).replacement(population, offspring_population)
        self._emit("survival", survivors)
        return survivors


class LoggingGeneticAlgorithm(RepairedGeneticAlgorithm):
    def replacement(self, population: List[S], offspring_population: List[S]) -> List[S]:
        population.extend(offspring_population)
        random.shuffle(population)   # random order first, so equal fitnesses are ranked by chance
        population.sort(key=cmp_to_key(self.solution_comparator.compare))
        survivors = population[: self.population_size]
        if self.trace is None:       # with a trace the fitnesses are shown there
            print("HIGHEST FITNESSES", [solution.objectives[0] for solution in survivors])
        self._emit("survival", survivors)
        return survivors


class TopKSelectorGeneticAlgorithm(LoggingGeneticAlgorithm):
    def __init__(self, k: int, *args, **kwargs) -> None:
        super(TopKSelectorGeneticAlgorithm, self).__init__(*args, **kwargs)
        self.k = k

    def replacement(self, population: List[S], offspring_population: List[S]) -> List[S]:
        # Only the k best of the current population survive into the competition. They are
        # ranked here first: before the very first replacement the population is not sorted yet.
        ranked = sorted(population, key=cmp_to_key(self.solution_comparator.compare))
        kept = ranked[: self.k]
        self._emit("kept", kept)
        return super(TopKSelectorGeneticAlgorithm, self).replacement(kept, offspring_population)