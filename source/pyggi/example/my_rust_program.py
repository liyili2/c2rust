from copy import deepcopy
import os
from types import SimpleNamespace as Result
from pyggi.tree.rust_engine import RustEngine
from pyggi.base.patch import Patch
from pyggi.tree.tree import TreeProgram
from RustParser.AST_Scripts.ast.TypeChecker import TypeChecker
import builtins
import pytest

class ResultCapture:
    def __init__(self):
        self.failed = 0
        self.passed = 0

    def pytest_sessionfinish(self, session):
        self.failed = session.testsfailed
        self.passed = session.testscollected - session.testsfailed

class MyRustProgram(TreeProgram):
    def __init__(self, path, config):
        self.config = config
        super().__init__(path, config)
        self.main_file = config["target_files"][0]
        self.trees = {}
        for file_name in self.target_files:
            file_path = os.path.join(self.path, file_name)
            self.trees[file_name] = self.engines[file_name].get_contents(file_path)

    @classmethod
    def get_engine(cls, file_name):
        if file_name.endswith(".rs"):
            return RustEngine
        raise Exception(f"No engine for {file_name}")

    def apply_patch(self, patch):
        variant = MyRustProgram(path=self.path, config=self.config)
        variant.trees = deepcopy(self.trees)
        variant.modification_points = deepcopy(self.modification_points)
        new_variant = variant.apply(patch)
        return new_variant

    def evaluate_patch(self, patch: Patch, timeout=15):
        """
        1. Apply `patch` to a temp copy of the project
        2. Run the Rust type‑checker on the main file
        3. Return a Result with .status and .fitness  (lower is better)
        """
        print("evaluate_patch")
        variant = self.apply_patch(patch)

        mutated_ast = variant[self.main_file]
        # print("eval tree", self.main_file, pretty_print_ast(mutated_ast))

        # diff = DeepDiff(original, variant, ignore_order=True)
        # print("🔍 Mutation diff:")
        # print(diff)

        res = Result()
        res.status = None
        res.fitness = None
        if mutated_ast:
            if len(mutated_ast.items) == 0:
                fitness = None
                status = "CRASH"
                print("✖︎ Invalid AST Generated")
                status = "CRASH"
                print("✖︎ Invalid AST Generated")

            else:
                # Evaluate directly
                try:
                    checker = TypeChecker()
                    checker.visit(mutated_ast)
                    print("eval ", checker.error_count, len(mutated_ast.items))
                    fitness = checker.error_count
                    status = "SUCCESS"
                    res.status = status
                    res.fitness = fitness

                except Exception as e:
                    fitness = None
                    status = "CRASH"
                    print("✖︎", e)

                # run functional tests and assertions with the ast
                # try:
                #     functional_test_report = ResultCapture()
                #     builtins.ast = mutated_ast
                #     exit_code  = pytest.main(["-s", self.config["test_command"]], plugins=[functional_test_report])
                #     res.fitness += functional_test_report.failed
                #     self.compute_fitness(res, exit_code)

                # except Exception as e:
                #     pass

        # res['BestFitness'] = best_fitness
        # res['diff'] = self.program.diff(best_patch)
        return res
