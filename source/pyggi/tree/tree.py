import os
import ast
import astor
import random
from abc import abstractmethod
from pyggi.tree.rust_engine import RustEngine
from . import AbstractTreeEngine, AstorEngine, XmlEngine
from ..base import AbstractProgram, AbstractEdit
from ..utils import get_file_extension

class TreeProgram(AbstractProgram):
    @classmethod
    def get_engine(cls, file_name):
        print("detecting engine!")
        extension = get_file_extension(file_name)
        print("ext is ", extension)
        if extension in ['.py']:
            return AstorEngine
        elif extension in ['.xml']:
            return XmlEngine
        elif extension in ['.rs']:
            return RustEngine
        else:
            raise Exception('{} file is not supporteddddd'.format(extension))

"""
Possible Edit Operators
"""
class TreeEdit(AbstractEdit):
    @property
    def domain(self):
        return TreeProgram

class StmtReplacement(TreeEdit):
    def __init__(self, target, ingredient):
        self.target = target
        self.ingredient = ingredient

    def apply(self, program, new_contents, modification_points):
        print("StmtReplacement called")
        engine = program.engines[self.target[0]]
        return engine.do_replace(program, self, new_contents, modification_points)

    @classmethod
    def create(cls, program, target_file=None, ingr_file=None, method='random'):
        # print("c1")
        if target_file is None:
            target_file = program.target_files[0]
        if ingr_file is None:
            ingr_file = program.target_files[0]
        # print("c2", target_file, program.engines[ingr_file], program.engines[target_file])
        assert program.engines[target_file] == program.engines[ingr_file]
        return cls(program.random_target(target_file, method),
                program.random_target(ingr_file, 'random'))

class StmtInsertion(TreeEdit):
    def __init__(self, target, ingredient, direction='before'):
        assert direction in ['before', 'after']
        self.target = target
        self.ingredient = ingredient
        self.direction = direction

    def apply(self, program, new_contents, modification_points):
        print("StmtInsertion called")
        engine = program.engines[self.target[0]]
        return engine.do_insert(program, self, new_contents, modification_points)

    @classmethod
    def create(cls, program, target_file=None, ingr_file=None, direction=None, method='random'):
        if target_file is None:
            target_file = program.target_files[0]
        if ingr_file is None:
            ingr_file = program.target_files[0]
        assert program.engines[target_file] == program.engines[ingr_file]
        if direction is None:
            direction = random.choice(['before', 'after'])
        return cls(program.random_target(target_file, method),
                   program.random_target(ingr_file, 'random'), direction)

class StmtDeletion(TreeEdit):
    def __init__(self, target):
        self.target = target

    def apply(self, program, new_contents, modification_points):
        engine = program.engines[self.target[0]]
        print("StmtDeletion called", engine, new_contents.__class__, new_contents, program.__class__, program)
        return engine.do_delete(program, self, new_contents, modification_points)

    @classmethod
    def create(cls, program, target_file=None, method='random'):
        if target_file is None:
            target_file = program.target_files[0]
        return cls(program.random_target(target_file, method))

class StmtMoving(TreeEdit):
    def __init__(self, target, ingredient, direction='before'):
        assert direction in ['before', 'after']
        self.target = target
        self.ingredient = ingredient
        self.direction = direction

    def apply(self, program, new_contents, modification_points):
        engine = program.engines[self.target[0]]
        engine.do_insert(program, self, new_contents, modification_points)
        self.target, self.ingredient = self.ingredient, self.target
        return_code = engine.do_delete(program, self, new_contents, modification_points)
        self.target, self.ingredient = self.ingredient, self.target
        return return_code

    @classmethod
    def create(cls, program, target_file=None, ingr_file=None, direction=None, method='random'):
        if target_file is None:
            target_file = program.random_file(AbstractTreeEngine)
        if ingr_file is None:
            ingr_file = program.random_file(engine=program.engines[target_file])
        assert program.engines[target_file] == program.engines[ingr_file]
        if direction is None:
            direction = random.choice(['before', 'after'])
        return cls(program.random_target(target_file, method),
                   program.random_target(ingr_file, 'random'),
                   direction)
