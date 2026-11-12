"""
Pair checkers: rules that decide whether two nodes may be swapped (RustSwapOperator) or
exchanged (RustSubtreeCrossover).

A pair checker is a callable

    checker(point_a, point_b, root_a=None, root_b=None) -> bool

    point_a, point_b  the two candidate points (marked nodes: .node, .get_id())
    root_a, root_b    the marked trees the points come from. For a swap both are the same
                      tree (root_b is None); for a crossover they are the two parents' trees.

Plain checkers with only (point_a, point_b) still work; call_pair_checker adapts the call.

Available checkers (combine them with AllOf):
    SameFunction()   both nodes are inside the same function (crossover: functions with the
                     same name, or at the same position when functions have no name)
    SameNodeType()   both nodes are of the same node class (e.g. identifier <-> identifier)
    AllOf(a, b, ...) every checker must accept the pair
"""
import inspect

from rust.nodes.TopLevel import FunctionDefinition
from rust.nodes.MarkedASTNode import MarkedASTNode
from rust.visitors.NodeCollector import NodeCollector


def call_pair_checker(checker, point_a, point_b, root_a=None, root_b=None):
    """Call `checker`, passing the trees only if it asks for them (has a root_a parameter)."""
    try:
        parameters = inspect.signature(checker).parameters
    except (TypeError, ValueError):
        parameters = {}
    if "root_a" in parameters:
        return checker(point_a, point_b, root_a=root_a, root_b=root_b)
    return checker(point_a, point_b)


def _function_name(function):
    """The function's name if the node exposes it as a plain string, else None."""
    for attribute in ("identifier", "name", "_name", "_identifier"):
        value = getattr(function, attribute, None)
        if isinstance(value, str):
            return value
    return None


class SameFunction:
    """True if both nodes lie inside the same function definition."""

    def __init__(self):
        self._cache = {}    # id(root) -> (root, owner, names); the root is kept so ids stay valid

    def _info(self, root):
        entry = self._cache.get(id(root))
        if entry is None or entry[0] is not root:
            if len(self._cache) > 8:
                self._cache.clear()
            functions = NodeCollector(FunctionDefinition, lambda node: True).collect(root)
            owner = {}      # id of a marked node -> index of the function containing it
            for index, function in enumerate(functions):
                for marked in NodeCollector(MarkedASTNode, lambda node: True).collect(function):
                    owner.setdefault(marked.get_id(), index)
            entry = (root, owner, [_function_name(f) for f in functions])
            self._cache[id(root)] = entry
        return entry[1], entry[2]

    def __call__(self, point_a, point_b, root_a=None, root_b=None):
        if root_a is None:
            return True                      # no tree given: cannot tell, so do not block
        same_tree = root_b is None or root_b is root_a
        owner_a, names_a = self._info(root_a)
        owner_b, names_b = (owner_a, names_a) if same_tree else self._info(root_b)

        function_a = owner_a.get(point_a.get_id())
        function_b = owner_b.get(point_b.get_id())
        if function_a is None or function_b is None:
            return False                     # a node outside any function
        if same_tree:
            return function_a == function_b
        name_a, name_b = names_a[function_a], names_b[function_b]
        if name_a is not None and name_b is not None:
            return name_a == name_b          # crossover: the same function in both parents
        return function_a == function_b      # no names: the function at the same position

    def __str__(self):
        return "same function"


class SameNodeType:
    """True if both nodes are of the same node class."""

    def __call__(self, point_a, point_b, root_a=None, root_b=None):
        return type(point_a.node) is type(point_b.node)

    def __str__(self):
        return "same node type"


class AllOf:
    """True if every checker accepts the pair."""

    def __init__(self, *checkers):
        self.checkers = checkers

    def __call__(self, point_a, point_b, root_a=None, root_b=None):
        return all(call_pair_checker(checker, point_a, point_b, root_a, root_b)
                   for checker in self.checkers)

    def __str__(self):
        return " + ".join(str(checker) for checker in self.checkers)