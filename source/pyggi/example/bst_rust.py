"""
Improving non-functional properties ::
"""
import os
import sys
import random
import argparse

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from RustParser.AST_Scripts.RustEngine import MyRustProgram
from RustParser.AST_Scripts.antlr.RustLexer import RustLexer
from antlr4 import CommonTokenStream, InputStream
from RustParser.AST_Scripts.antlr.RustParser import RustParser
from pyggi.algorithms.local_search import LocalSearch
from pyggi.base.program import AbstractProgram
from pyggi.line.line import LineDeletion, LineInsertion, LineProgram, LineReplacement
from pyggi.tree.tree import StmtDeletion, StmtInsertion, StmtReplacement, TreeProgram
from pyggi.tree.xml_engine import XmlEngine

weighted_choice = lambda s : random.choice(sum(([v] * wt for v,wt in s),[]))

class MyProgram(AbstractProgram):
    def compute_fitness(self, result, return_code, stdout, stderr, elapsed_time):
        try:
            runtime, pass_all = stdout.strip().split(',')
            runtime = float(runtime)
            if not pass_all == 'true':
                result.status = 'PARSE_ERROR'
            else:
                result.fitness = runtime
        except:
            result.status = 'PARSE_ERROR'

class MyLineProgram(LineProgram, MyProgram):
    pass

class MyLocalSearch(LocalSearch):
    def get_neighbour(self, patch):
        if len(patch) > 0 and random.random() < 0.5:
            patch.remove(random.randrange(0, len(patch)))
        else:
            edit_operator = random.choice(self.operators)
            patch.add(edit_operator.create(self.program))
        return patch

    def stopping_criterion(self, iter, fitness):
        return fitness < 100

if __name__ == "__main__":
    print("running pyggi!!!!!!")
    parser = argparse.ArgumentParser(description='PYGGI Improvement Example')
    parser.add_argument('--project_path', type=str, default='../sample/bst_rust')
    parser.add_argument('--mode', type=str, default='line')
    parser.add_argument('--epoch', type=int, default=30,
        help='total epoch(default: 30)')
    parser.add_argument('--iter', type=int, default=100,
        help='total iterations per epoch(default: 100)')
    args = parser.parse_args()
    assert args.mode in ['line', 'tree']

    if args.mode == 'line':
        config = {
            "target_files": ["bst.rs"],
            "test_command": "./run.sh"
        }
        program = MyLineProgram(args.project_path, config=config)
        local_search = MyLocalSearch(program)
        local_search.operators = [LineReplacement, LineInsertion, LineDeletion]
    elif args.mode == 'tree':
        print("in tree mode!!")
        #TODO: check the target file
        config = {
            "target_files": ["bst.rs"],
            "test_command": "./run.sh"
        }
        program = MyRustProgram(args.project_path, config=config)
        print("Registered engines and files:")
        print(program.__class__, program.files)
        local_search = MyLocalSearch(program)
        local_search.operators = [StmtReplacement, StmtInsertion, StmtDeletion]

    
    result = local_search.run(warmup_reps=5, epoch=args.epoch, max_iter=args.iter, timeout=15)
    print("======================RESULT======================")
    for epoch in range(len(result)):
        print("Epoch {}".format(epoch))
        print(result[epoch])
        print(result[epoch]['diff'])
    program.remove_tmp_variant()
