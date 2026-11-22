"""
Possible Edit Operators
"""
import copy

from repair.pyggi.tree.tree import TreeEdit

from rust.visitors.Base import strip_marks_tree, swap_marked_nodes
from rust.visitors.MarkingVisitor import MarkingVisitor
from rust.visitors.MarkedNodeTargetUpdater import MarkedNodeTargetUpdater
from rust.visitors.NodeCollector import NodeCollector
from rust.nodes.MarkedASTNode import MarkedASTNode

# ==========================================================================
# Rust AST operators
# --------------------------------------------------------------------------
# Target selection (which point / which pair / which candidate) lives on the
# program, in CProgram.replace_target / CProgram.swap_target. The operators
# only store the chosen ids and apply them to a freshly marked tree.
# No visitor is defined here: tree rewriting lives in rust/visitors/Base.py.
# ==========================================================================

class RustOperator(TreeEdit):
    """Base for AST-level Rust operators. Conforms to PyGGI's
    apply(program, new_contents, modification_points) call convention, since
    AbstractProgram.get_modified_contents calls it that way."""

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
    def create(cls, program, target_file=None, checker=None, scope_checker=None,
               rng=None, max_attempts=10, updated_contents=None):
        # program.replace_target -> (target_file, point_id, candidate);
        # point_id / candidate are None when nothing eligible was found.
        target_file, point_id, candidate = program.replace_target(
            target_file, checker=checker, scope_checker=scope_checker, rng=rng,
            max_attempts=max_attempts, updated_contents=updated_contents)
        return cls(target_file, point_id, candidate)

    @staticmethod
    def get_weight_initial():
        return 0.5  # operator weights sum to 1.0


# --------------------------------------------------------------------------
# Swap operator
# --------------------------------------------------------------------------

class RustSwapOperator(RustOperator):
    """Swaps the positions of two marked nodes.

    Only the two point ids are stored; the nodes are looked up in a freshly
    marked tree at apply time. Ids travel with the content, so no id is
    duplicated and applying the same swap twice restores the original tree.
    Nested pairs and structurally equal pairs are rejected (in
    CProgram.swap_target, and re-checked for nesting at apply time). The
    result is returned without MarkedASTNode wrappers."""

    TYPE = "RustSwap"

    def __init__(self, target_file: str, point_a_id, point_b_id):
        # base class: modification_point_id = a, target = b, _target = (file, a)
        super().__init__(self.TYPE, target_file, point_a_id, point_b_id)
        self.point_a_id = point_a_id
        self.point_b_id = point_b_id

    def __repr__(self):
        return f"RustSwapOperator({self.target_file}, {self.point_a_id} <-> {self.point_b_id})"

    @classmethod
    def create(cls, program, target_file=None, checker=None, scope_checker=None,
               rng=None, max_attempts=10, updated_contents=None, pair_checker=None):
        """updated_contents: the contents after the earlier edits of the patch; points are
        chosen against them when given, otherwise against program.contents.
        pair_checker: optional (point_a, point_b) -> bool to reject incompatible pairs."""
        # program.swap_target -> (target_file, id_a, id_b); ids are None if nothing eligible.
        target_file, a_id, b_id = program.swap_target(
            target_file, checker=checker, scope_checker=scope_checker, rng=rng,
            max_attempts=max_attempts, updated_contents=updated_contents,
            pair_checker=pair_checker)
        return cls(target_file, a_id, b_id)

    @staticmethod
    def _contains(outer, inner_id):
        """True if the marked point `inner_id` lies strictly inside `outer`."""
        return bool(NodeCollector(MarkedASTNode, lambda n: n.get_id() == inner_id).collect(outer.node))

    def do_apply(self, new_contents):
        if self.point_a_id is None or self.point_b_id is None:
            return True  # nothing eligible at create time - no-op edit

        # strip first so the tree is never marked twice, whatever the earlier edits left
        root = strip_marks_tree(new_contents[self.target_file])
        marked_root = root.accept(MarkingVisitor())

        a = self._find_by_id(marked_root, self.point_a_id)
        b = self._find_by_id(marked_root, self.point_b_id)
        if a is None or b is None:
            return False  # a point vanished (earlier edit) - fail this edit, don't guess
        if self._contains(a, self.point_b_id) or self._contains(b, self.point_a_id):
            return False  # an earlier edit made one contain the other

        swapped = swap_marked_nodes(marked_root, self.point_a_id, self.point_b_id, a, b)
        new_contents[self.target_file] = strip_marks_tree(swapped)
        return True

    @staticmethod
    def get_weight_initial():
        return 0.5