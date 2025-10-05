"""
Improving non-functional properties ::
"""
from copy import deepcopy
import os
import sys
import random
import argparse
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from pyggi.example.my_rust_program import MyRustProgram
from pyggi.tree.rust_engine import RustEngine
from pyggi.algorithms.local_search import LocalSearch
from pyggi.base.program import AbstractProgram
from pyggi.line.line import LineDeletion, LineInsertion, LineProgram, LineReplacement
from pyggi.tree.tree import StmtDeletion, StmtInsertion, StmtMoving, StmtReplacement, TreeProgram

weighted_choice = lambda s : random.choice(sum(([v] * wt for v,wt in s),[]))

def get_file_extension(file_path):
    """
    :param file_path: The path of file
    :type file_path: str
    :return: file extension
    :rtype: str
    """
    _, file_extension = os.path.splitext(file_path)
    return file_extension

def get_engine(cls, file_name):
    if file_name.endswith(".rs"):
        return RustEngine
    extension = get_file_extension(file_name)
    if extension in ['.rs']:
        return RustEngine
    else:
        raise Exception('{} file is not supporteddddd'.format(extension))

class MyProgram(AbstractProgram):
    def compute_fitness(self, result, exit_code):
        if exit_code != 0:
            result.status = "Functional Incorrectness"
        else:
            result.status = "SUCCESS"

    @classmethod
    def get_engine(cls, file_name):
        return RustEngine

class MyLineProgram(LineProgram, MyProgram):
    pass

class MyLocalSearch(LocalSearch):
    def get_neighbour(self, patch):
        if len(patch) > 0 and random.random() < 0.5:
            patch.remove(random.randrange(len(patch)))
        else:
            edit_op = random.choice(self.operators)
            patch.add(edit_op.create(self.program))
        return patch

    def stopping_criterion(self, iter_no, fitness):
        return fitness == 0

def pretty_print_ast(node, indent=0):
    spacer = '  ' * indent
    if isinstance(node, list):
        return '\n'.join(pretty_print_ast(n, indent) for n in node)

    if hasattr(node, '__dict__'):
        lines = [f"{spacer}{node.__class__.__name__}:"]
        for key, value in vars(node).items():
            lines.append(f"{spacer}  {key}:")
            lines.append(pretty_print_ast(value, indent + 2))
        return '\n'.join(lines)
    else:
        return f"{spacer}{repr(node)}"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--project_path", type=str, default="../sample/bst_rust")
    parser.add_argument("--mode", choices=["line", "tree"], default="tree")
    parser.add_argument("--epoch", type=int, default=30)
    parser.add_argument("--iter",  type=int, default=100)
    args = parser.parse_args()

    if args.mode == "line":
        cfg = {"target_files": ["bst.rs"], "test_command": "./run.sh"}
        program = MyLineProgram(args.project_path, config=cfg)
        ops     = [LineReplacement, LineInsertion, LineDeletion]
    else:
        cfg = {"target_files": ["bst.rs"], "test_command": "pyggi/sample/bst_rust/bst_test.py"}
        program = MyRustProgram(args.project_path, config=cfg)
        ops     = [StmtReplacement, StmtInsertion, StmtDeletion]

    search = MyLocalSearch(program)
    search.operators = ops
    results = search.run(warmup_reps=5, epoch=args.epoch, max_iter=args.iter, timeout=15)
    print("====================== RESULT ======================")
    for ep, r in enumerate(results, 1):
        print(f"Epoch {ep}:  best fitness {r['BestFitness']}")
        # if r["diff"]:
        #     print(r["diff"])

    program.remove_tmp_variant()

if __name__ == "__main__":
    main()