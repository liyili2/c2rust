"""
Improving non-functional properties ::
"""
import os
import sys
import random
import argparse
from antlr4 import CommonTokenStream, InputStream
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from pyggi.tree.rust_engine import RustEngine
from pyggi.algorithms.local_search import LocalSearch
from pyggi.base.program import AbstractProgram
from pyggi.line.line import LineDeletion, LineInsertion, LineProgram, LineReplacement
from pyggi.tree.tree import StmtDeletion, StmtInsertion, StmtReplacement, TreeProgram
from pyggi.tree.xml_engine import XmlEngine
from RustParser.AST_Scripts.antlr.RustLexer import RustLexer
from RustParser.AST_Scripts.antlr.RustParser import RustParser
from RustParser.AST_Scripts.ast.Transformer import Transformer
from RustParser.AST_Scripts.ast.TypeChecker import TypeChecker

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

class MyRustProgram(TreeProgram):
    def __init__(self, path, config):
        self.ast = None
        self.file_name = None
        super().__init__(path, config)
        self.files = "./"
        self.engine_classes = {
            '.rs': RustEngine
        }

    @classmethod
    def get_engine(cls, file_name):
        if file_name.endswith(".rs"):
            return RustEngine
        extension = get_file_extension(file_name)
        if extension in ['.rs']:
            return RustEngine
        else:
            raise Exception('{} file is not supporteddddd'.format(extension))

class MyProgram(AbstractProgram):
    def compute_fitness(self, result, return_code, stdout, stderr, elapsed_time):
        try:
            passed = "test result: ok" in stdout
            result.fitness = elapsed_time
            result.status = 'SUCCESS' if passed else 'PARSE_ERROR3'
        except:
            result.status = 'PARSE_ERROR4'

    @classmethod
    def get_engine(cls, file_name):
        return RustEngine

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

if __name__ == "__main__":
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
        #TODO: check the target file
        config = {
            "target_files": ["bst.rs"],
            "test_command": "./run.sh"
        }

        program = MyRustProgram(args.project_path, config=config)

        local_search = MyLocalSearch(program)
        local_search.file_name = program.file_name
        local_search.operators = [StmtReplacement, StmtInsertion, StmtDeletion]
        print("local search program is ", local_search.program.__class__)

    result = local_search.run(warmup_reps=5, epoch=args.epoch, max_iter=args.iter, timeout=15)
    print("======================RESULT======================")
    for epoch in range(len(result)):
        print("Epoch {}".format(epoch))
        print(result[epoch])
        print(result[epoch]['diff'])
    program.remove_tmp_variant()
