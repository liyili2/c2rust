import copy
from RustParser.AST_Scripts.ast.Program import Program
from RustParser.AST_Scripts.ast.Expression import *
from RustParser.AST_Scripts.ast.Statement import *
from RustParser.AST_Scripts.ast.Func import *
from RustParser.AST_Scripts.ast.Block import *
from RustParser.AST_Scripts.ast.TopLevel import *
from RustParser.AST_Scripts.ast.TypeChecker import *
from RustParser.AST_Scripts.ast.ASTNode import *
from RustParser.AST_Scripts.ast.Type import *
from RustParser.AST_Scripts.ast.VarDef import *
from RustParser.AST_Scripts.ast.Transformer import setParents
from pyggi.mutation.utils import MutationUtils
import random

class Crossover:
    def __init__(self, offspring_1, offspring_2, target_node):
        self.offspring_1 = offspring_1
        self.offspring_2 = offspring_2
        self.target_node = target_node
        return self.apply()

    def apply(self):
        # self.offspring_1.target = self.offspring_2.target
        return self.offspring_1, self.offspring_2
