import builtins
import copy
import random
import sys

import pytest
from pyggi.mutation.visitor import MutationVisitor
from RustParser.AST_Scripts.ast.TypeChecker import TypeChecker
from RustParser.AST_Scripts.ast import Program

class ResultCapture:
    def __init__(self):
        self.failed = 0
        self.passed = 0

    def pytest_sessionfinish(self, session):
        self.failed = session.testsfailed
        self.passed = session.testscollected - session.testsfailed

class Gene:
    def __init__(self, gene: Program, fitness):
        self.gene = gene
        self.fitness = fitness

class GenProg:
    def __init__(self, original_ast):
        self.population_size = 25
        self.max_iteration_num = 200
        self.mutation_const = 0.3
        self.crossover_const = 0.1
        self.max_fitness = 0
        self.best_fitness = sys.float_info.max
        self.original_ast = copy.deepcopy(original_ast)
        self.population = self.generate_initial_population()
        self.final_answer = self.run_iterations().gene

    def generate_initial_population(self):
        initial_population = []
        for i in range(0, self.population_size):
            new_gene = self.apply_mutation(self.original_ast)
            fitness = self.calculate_fitness(new_gene)
            initial_population.append(Gene(gene=new_gene, fitness=fitness))
        return initial_population

    def select_best_genes(self, population):
        sorted_pop = sorted(population, key=lambda g: g.fitness, reverse=True)
        cutoff = int(len(sorted_pop) * 4 / 5)
        # cutoff = int(len(sorted_pop))
        best_genes = sorted_pop[:cutoff]
        best_genes.reverse()
        self.best_fitness = best_genes[0].fitness
        print("Best Fitness So Far: ", best_genes[0].fitness)
        return best_genes

    def apply_mutation(self, variant):
        mutator = MutationVisitor(original_ast=variant, mutation_const=self.mutation_const)
        mutated_variant = mutator.visit(variant)
        return mutated_variant

    def apply_crossover(self, variant):
        pass

    def calculate_fitness(self, variant):
        type_checker = TypeChecker()
        type_checker.visit(variant)
        fitness = type_checker.error_count
        functional_test_report = ResultCapture()
        # builtins.ast = variant
        # exit_code  = pytest.main(["-s", "pyggi/sample/nfa_rust/nfa_test.py"], plugins=[functional_test_report])
        fitness += functional_test_report.failed
        return fitness

    def run_iterations(self):
        i = 0
        while i < self.max_iteration_num and self.best_fitness != self.max_fitness:
            i += 1
            elite_population = self.select_best_genes(self.population)
            j=0
            self.mutation_const = random.random()
            for elite in elite_population:
                j += 1
                elite = self.apply_mutation(elite.gene)
                # crossover_probability = random.random()
                # if crossover_probability > self.crossover_const:
                #     elite.gene = self.apply_crossover(variant=elite.gene)
                elite.fitness = (self.calculate_fitness(variant=elite))
                print("fitness#" , j, ": ", elite.fitness)

        return elite_population[0]
