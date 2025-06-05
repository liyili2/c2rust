"""
Improving non-functional properties ::
"""
import os
import sys
import random
import argparse

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from RustParser.AST_Scripts.antlr.RustLexer import RustLexer
from antlr4 import CommonTokenStream, InputStream
from RustParser.AST_Scripts.antlr.RustParser import RustParser
from pyggi.algorithms.local_search import LocalSearch
from pyggi.base.program import AbstractProgram
from pyggi.line.line import LineDeletion, LineInsertion, LineProgram, LineReplacement
from pyggi.tree.tree import StmtDeletion, StmtInsertion, StmtReplacement, TreeProgram
from pyggi.tree.xml_engine import XmlEngine

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

class MyTreeProgram(TreeProgram, MyProgram):
    def setup(self):
        # if not os.path.exists(os.path.join(self.tmp_path, "bst.rs.xml")):
        #     self.exec_cmd("srcml Triangle.java -o Triangle.java.xml")
        pass

    # @classmethod
    # def get_engine(cls, file_name):
    #     return MyXmlEngine

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
    
class RustEngine():
    def parse(self, src_code):
        lexer = RustLexer(InputStream(src_code))
        tokens = CommonTokenStream(lexer)
        parser = RustParser(tokens)
        tree = parser.program()
        return tree  # Use your AST node visitor if needed

    def to_source_code(self, tree):
        return pretty_print_ast(tree)

class MyRustProgram(TreeProgram):
    @classmethod
    def get_engine(cls, file_name):
        if file_name.endswith(".rs"):
            return RustEngine
        print("detecting engine!")
        extension = get_file_extension(file_name)
        print("ext is ", extension)
        if extension in ['.xml']:
            return XmlEngine
        elif extension in ['.rs']:
            return RustEngine
        else:
            raise Exception('{} file is not supporteddddd'.format(extension))

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
        print("in tree mode!!")
        #TODO: check the target file
        config = {
            "target_files": ["bst.rs"],
            "test_command": "./run.sh"
        }
        program = MyTreeProgram(args.project_path, config=config)
        local_search = MyLocalSearch(program)
        local_search.operators = [StmtReplacement, StmtInsertion, StmtDeletion]

    result = local_search.run(warmup_reps=5, epoch=args.epoch, max_iter=args.iter, timeout=15)
    print("======================RESULT======================")
    for epoch in range(len(result)):
        print("Epoch {}".format(epoch))
        print(result[epoch])
        print(result[epoch]['diff'])
    program.remove_tmp_variant()
