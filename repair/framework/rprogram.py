import os

from .cprogram import CProgram
from .cresult import CResult
from rust.visitors.ast_compare import ast_equal

from .rpatch import RPatch


class RProgram(CProgram):
    """
    CProgram that evaluates an RPatch straight from its AST.

    PyGGI's apply() replays patch.edit_list on a deep copy of the original contents, which
    would only recompute what the RPatch already holds, so apply() returns patch.ast.
    (patch.diff still replays the edit list; both give the same tree.) Evaluation writes
    that AST to the temporary variant of the project and runs the test command there.
    """

    def __init__(self, *args, **kwargs):
        super(RProgram, self).__init__(*args, **kwargs)
        # extra checks used by validate(): callables contents -> bool,
        # e.g. program.validators.append(my_compile_check)
        self.validators = []

    def update_operators(self, solution: RPatch, max_depth=None, max_width=None):
        """
        Called by TypeConsistentGeneticAlgorithm on every crossover child.
        Checks that the child is consistent - its edit list replays on the original program
        to exactly the AST it holds - and returns its contents. Raises if not, which makes
        the algorithm fall back to the parent. (max_depth / max_width are accepted for the
        algorithm's interface; no size limit is enforced here.)
        """
        replayed = solution.apply_edits()
        for file_name, root in solution.ast.items():
            if not ast_equal(replayed[file_name], root):
                raise Exception(f"the edit list does not rebuild the AST of {file_name}")
        return solution.ast

    def validate(self, contents) -> bool:
        """
        True if every target file can be turned back into source text and every extra
        validator in self.validators accepts the contents. A real type/compile check can be
        plugged in through self.validators.
        """
        try:
            for file_name in self.target_files:
                if not self.dump(contents, file_name):
                    return False
        except Exception:
            return False
        return all(check(contents) for check in self.validators)

    def apply(self, patch: RPatch):
        return patch.ast

    def get_modified_contents(self, patch: RPatch):
        """
        Used by PyGGI's diff(). The stock version replays the edits itself and leaves
        MarkedASTNode wrappers in the tree (the diff then shows <marked> tags).
        RPatch.apply_edits replays the same edits and strips the marks after each one.
        """
        return patch.apply_edits()

    def write_variant(self, ast: dict):
        if not os.path.exists(self.tmp_path):
            self.create_tmp_variant()      # copy of the project, once
        self.write_to_tmp_dir(ast)         # overwrite the target files with the AST's source

    def evaluate_solution(self, patch: RPatch, test_command):
        self.write_variant(patch.ast)
        try:
            rcode, stdout, stderr, elapsed = self.exec_cmd(test_command, timeout=10)
        except FileNotFoundError as error:
            raise RuntimeError(
                f"Could not start the test command {test_command!r} (run inside {self.tmp_path}): "
                f"{error}. Check that the program is on PATH, or give the full path. "
                "Use forward slashes in paths: the command is split with shlex, which removes "
                "backslashes.") from error
        result = CResult('SUCCESS', None)
        if rcode is None:                  # timeout: exec_cmd returns (None, None, None, None)
            result.status = 'TIMEOUT'
            result.fitness = RPatch.WORST_FITNESS
            return result
        self.compute_fitness(result, rcode, stdout, stderr, elapsed)
        return result