"""
RPatch: the Rust counterpart of CPatch. Its core is the AST.

* The AST ({target_file: AST root}) is the jMetal decision variable (variables[0]) and
  the authoritative state of the solution.
* To stay a PyGGI Patch (diff, clone, program.apply, ...) it also keeps `program` and
  `edit_list`: the sequence of edits that, replayed on the original program, rebuilds
  exactly that AST. `add` / `remove` keep AST and edit list in sync, so always change a
  patch through them rather than editing `ast` or `edit_list` by hand.
"""
import copy

from jmetal.core.solution import Solution
from repair.pyggi.base import Patch
from repair.pyggi.base.edit import AbstractEdit

from .operators import strip_marks_tree


def strip_marks(ast):
    """Remove MarkedASTNode wrappers from every file's tree (in place on the dict)."""
    for file_name in ast:
        ast[file_name] = strip_marks_tree(ast[file_name])
    return ast


class RPatch(Solution, Patch):
    WORST_FITNESS = 1000000

    def __init__(self, program, number_of_variables: int = 1, number_of_objectives: int = 1):
        super(RPatch, self).__init__(number_of_variables=number_of_variables,
                                     number_of_objectives=number_of_objectives)
        # PyGGI side (Patch.__init__ is deliberately not called, same as CPatch)
        self.program = program
        self.edit_list = []
        # jMetal side: the AST is the decision variable, starting as a copy of the original
        self.variables = [copy.deepcopy(program.contents)]
        self.objectives = [self.WORST_FITNESS] * number_of_objectives   # objective[0] = fitness

    # `variables` is abstract in newer jMetal versions and a plain attribute in older ones;
    # defining it explicitly works with both.
    @property
    def variables(self):
        return self._variables

    @variables.setter
    def variables(self, values):
        self._variables = values

    # ------------------------------------------------------------------
    # the AST (core)
    # ------------------------------------------------------------------
    @property
    def ast(self) -> dict:
        """{target_file: AST root}"""
        return self.variables[0]

    @ast.setter
    def ast(self, value: dict):
        self.variables[0] = value

    def get_ast(self, target_file=None):
        """Root of one file's AST (the first file if not given)."""
        if target_file is None:
            target_file = next(iter(self.ast))
        return self.ast[target_file]

    # ------------------------------------------------------------------
    # fitness <-> objectives[0]
    # ------------------------------------------------------------------
    @property
    def fitness(self):
        return self.objectives[0]

    @fitness.setter
    def fitness(self, value):
        self.objectives[0] = value

    def __lt__(self, other):
        """Sort by fitness, best (lowest) first; unevaluated patches go last."""
        if self.fitness is None:
            return False
        if other.fitness is None:
            return True
        return self.fitness < other.fitness

    def __repr__(self):
        return '\n'.join(map(str, self.edit_list))

    def __len__(self):
        return len(self.edit_list)

    # ------------------------------------------------------------------
    # edits: applied onto the AST *and* recorded in the edit list
    # ------------------------------------------------------------------
    def _apply_to(self, edit, contents) -> bool:
        modification_points = getattr(self.program, 'modification_points', None)
        if not edit.apply(self.program, contents, modification_points):
            return False
        target_file = getattr(edit, 'target_file', None)
        if target_file in contents:   # keep the tree free of marks so point ids stay stable
            contents[target_file] = strip_marks_tree(contents[target_file])
        return True

    def add(self, edit, after: bool = True) -> bool:
        """
        Apply `edit` to the AST and record it in the edit list.
        :param after: True (PyGGI's behaviour) appends; False inserts at the front,
                      which means the AST is rebuilt by replaying the whole edit list.
        :return: False (and the patch is left unchanged) if the edit is a no-op or fails.
        """
        assert isinstance(edit, AbstractEdit)
        # an operator that found no eligible point is created with a None point id: a no-op
        if getattr(edit, 'modification_point_id', 0) is None:
            return False
        if after:
            if not self._apply_to(edit, self.ast):
                return False
            self.edit_list.append(edit)
        else:
            self.edit_list.insert(0, edit)
            self.rebuild()
        return True

    def remove(self, index: int):
        """Remove an edit; the AST is rebuilt without it."""
        del self.edit_list[index]
        self.rebuild()

    def apply_edits(self, edits=None) -> dict:
        """
        Replay `edits` (default: the edit list) on a deep copy of the original contents and
        return the resulting {file: AST}. Failing edits are skipped, as PyGGI does.
        """
        contents = copy.deepcopy(self.program.contents)
        for edit in (self.edit_list if edits is None else edits):
            self._apply_to(edit, contents)
        return contents

    def rebuild(self):
        """Recompute the AST from the original program and the edit list."""
        self.ast = self.apply_edits()

    # ------------------------------------------------------------------
    # copying: share the program, copy the AST and the edits
    # (a plain deepcopy would clone the whole program for every offspring)
    # ------------------------------------------------------------------
    def clone(self):
        new = RPatch(self.program, self.number_of_variables, self.number_of_objectives)
        new.ast = copy.deepcopy(self.ast)
        new.edit_list = [copy.deepcopy(edit) for edit in self.edit_list]
        new.objectives = list(self.objectives)
        new.constraints = list(self.constraints)
        new.attributes = copy.deepcopy(self.attributes)
        return new

    def __copy__(self):
        return self.clone()

    def __deepcopy__(self, memo):
        return self.clone()