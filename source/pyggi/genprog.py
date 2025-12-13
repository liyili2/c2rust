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
        self.population_size = 300
        self.max_iteration_num = 500
        self.mutation_const = 1
        self.crossover_const = 0.1
        self.max_fitness = 0
        self.best_fitness = sys.float_info.max
        self.original_ast = copy.deepcopy(original_ast)
        self.best_gene = Gene(fitness=self.best_fitness, gene=original_ast)
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
        best_genes = sorted(population, key=lambda g: g.fitness, reverse=True)
        best_genes.reverse()
        cutoff = int(len(best_genes) * 4 / 5)
        best_genes = best_genes[:cutoff]
        self.best_gene = Gene(fitness=self.best_fitness, gene=best_genes[0].gene)
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
        builtins.ast = variant
        exit_code  = pytest.main(["-s", "pyggi/sample/nfa_rust/nfa_test.py"], plugins=[functional_test_report])
        fitness += functional_test_report.failed
        return fitness

    def run_iterations(self):
        i = 0
        elite_population = self.population
        while i < self.max_iteration_num and self.best_fitness != self.max_fitness:
            i += 1
            elite_population = self.select_best_genes(elite_population)
            for idx, elite in enumerate(elite_population):
                self.mutation_const = random.random()
                mutated_gene = self.apply_mutation(elite.gene)
                new_fitness = self.calculate_fitness(variant=mutated_gene)
                if new_fitness < elite.fitness:
                    elite.fitness = new_fitness
                    elite.gene = mutated_gene
                print(f"fitness#{idx+1}: {elite.fitness}")

            self.best_fitness = min(e.fitness for e in elite_population)
            print("Best Fitness So Far: ", self.best_fitness)

        elite_population.sort(key=lambda e: e.fitness, reverse=True)
        return elite_population[0]