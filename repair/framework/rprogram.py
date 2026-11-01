import os

from .cprogram import CProgram
from .cresult import CResult
from .rpatch import RPatch


class RProgram(CProgram):
    """
    CProgram that evaluates an RPatch straight from its AST.

    PyGGI's apply() replays patch.edit_list on a deep copy of the original contents, which
    would only recompute what the RPatch already holds, so apply() returns patch.ast.
    (patch.diff still replays the edit list; both give the same tree.) Evaluation writes
    that AST to the temporary variant of the project and runs the test command there.
    """

    def apply(self, patch: RPatch):
        return patch.ast

    def write_variant(self, ast: dict):
        if not os.path.exists(self.tmp_path):
            self.create_tmp_variant()      # copy of the project, once
        self.write_to_tmp_dir(ast)         # overwrite the target files with the AST's source

    def evaluate_solution(self, patch: RPatch, test_command):
        self.write_variant(patch.ast)
        rcode, stdout, stderr, elapsed = self.exec_cmd(test_command, timeout=10)
        result = CResult('SUCCESS', None)
        if rcode is None:                  # timeout: exec_cmd returns (None, None, None, None)
            result.status = 'TIMEOUT'
            result.fitness = RPatch.WORST_FITNESS
            return result
        self.compute_fitness(result, rcode, stdout, stderr, elapsed)
        return result