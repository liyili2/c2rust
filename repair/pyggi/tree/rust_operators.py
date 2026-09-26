import copy

from repair.pyggi.tree.tree import TreeEdit
from rust.visitors.MarkingVisitor import MarkingVisitor
from rust.visitors.MarkedNodeTargetUpdater import MarkedNodeTargetUpdater
from rust.visitors.NodeCollector import NodeCollector
from rust.nodes.MarkedASTNode import MarkedASTNode
from rust.modification.ModificationPointSelector import ModificationPointSelector
from rust.modification.Constraint import ConstraintChecker


class RustOperator(TreeEdit):
    """Base for AST-level Rust operators. Mirrors QGenOperator's shape,
    but conforms to PyGGI's apply(program, new_contents, modification_points)
    call convention, since AbstractProgram.get_modified_contents calls it
    that way (QGen's own apply(current_root) does not fit that contract)."""

    def __init__(self, otype: str, target_file: str, modification_point_id, target):
        self.otype = otype
        self.target_file = target_file
        # Store the id, not the MarkedASTNode object: the object is only
        # valid against the exact marked tree it came from, and new_contents
        # gets deep-copied / rebuilt by earlier edits before this one runs.
        self.modification_point_id = modification_point_id
        self.target = target
        # AbstractProgram.get_modified_contents filters by `edit._target[0]`
        self._target = (target_file, modification_point_id)

    def apply(self, program, new_contents, modification_points):
        return self.do_apply(new_contents)

    def do_apply(self, new_contents):
        if self.modification_point_id is None:
            return True  # nothing was eligible at create time - no-op edit

        root = new_contents[self.target_file]
        marked_root = root.accept(MarkingVisitor())

        target_node = self._find_by_id(marked_root, self.modification_point_id)
        if target_node is None:
            # the point no longer exists (e.g. an earlier edit in this
            # patch removed/rewrote it) - fail this edit, don't guess
            return False

        updater = MarkedNodeTargetUpdater(self.modification_point_id, copy.deepcopy(self.target))
        new_contents[self.target_file] = marked_root.accept(updater)
        return True

    @staticmethod
    def _find_by_id(marked_root, point_id):
        matches = NodeCollector(MarkedASTNode, lambda n: n.get_id() == point_id).collect(marked_root)
        return matches[0] if matches else None

    def update(self, updated_root):
        pass

    @staticmethod
    def get_weight_initial():
        pass


class RustReplacementOperator(RustOperator):

    TYPE = "RustReplacement"

    def __init__(self, target_file: str, modification_point_id, target):
        super().__init__(self.TYPE, target_file, modification_point_id, target)

    @classmethod
    def create(cls, program, target_file=None,
               checker: ConstraintChecker = None,
               scope_checker: ConstraintChecker = None,
               rng=None):
        if target_file is None:
            target_file = program.random_file()

        root = program.contents[target_file]
        marked_root = root.accept(MarkingVisitor())

        selector = ModificationPointSelector(checker=checker, scope_checker=scope_checker, rng=rng)
        point = selector.select(marked_root)
        if point is None:
            return cls(target_file, None, None)

        # Import here to avoid a hard dependency for callers who only need
        # RustOperator/apply (e.g. replaying a saved patch).
        from rust.visitors.RandomCandidateReplacementGenerator import RandomCandidateReplacementGenerator
        generator = RandomCandidateReplacementGenerator(point, rng=rng)
        marked_root.accept(generator)  # rebuilt tree is discarded - only the candidate matters
        candidate = generator.replacement()

        return cls(target_file, point.get_id(), candidate)

    @staticmethod
    def get_weight_initial():
        return 1.0  # your only operator
