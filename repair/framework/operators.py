"""
Possible Edit Operators
"""
import random
# from xml.dom import minidom
#from repair.pyggi.base import BaseOperator
# from lxml import etree
import copy

# from RustCode.AST_Scripts.typechecker import TypeInfer
# from framework.configs.type_env import type_envs
#from repair.pyggi.tree import AbstractTreeEngine
# from Source.quantumCode.AST_Scripts import XMLExpPrinter
# from repair.pyggi.tree.xml_engine import XmlEngine
# from repair.pyggi.tree import StmtReplacement, StmtInsertion, StmtDeletion
from repair.pyggi.tree.tree import TreeEdit
# import xml.etree.ElementTree as ET

# Rust AST operators (moved here from rust_operators.py)
from rust.visitors.Base import RustASTGenerator
from rust.visitors.MarkingVisitor import MarkingVisitor
from rust.visitors.MarkedNodeTargetUpdater import MarkedNodeTargetUpdater
from rust.visitors.NodeCollector import NodeCollector
from rust.nodes.MarkedASTNode import MarkedASTNode

# ## Implement new operators here
# class CGateReplacement(StmtReplacement):
#     def __init__(self, target, ingredient, target_tag):
#         super(CGateReplacement, self).__init__(target, ingredient)
#         self.target_tag = target_tag

#     def apply(self, program, new_contents, modification_points):
#         print(" C2Rust replacement, apply")
#         engine = program.engines[self.target[0]]
#         result = self.__class__.do_replace(self, program, new_contents, modification_points)
#         return result

#     #the following program is subject to rewrite
#     def do_replace(self, program, new_contents, modification_points):
#         print("enter into C2Rust replacement, replace")
#         target_content = new_contents[self.target[0]]
#         ingredient_content = new_contents[self.ingredient[0]]

#         # Parse the XML content
#         target_tree = etree.fromstring(target_content)
#         #TODO: please modify here.
#         elements = target_tree.xpath(".//{}[...]".format(self.target_tag))

#         if elements:
#             print("enter into C2Rust replacement, elements")
#             # Choose the specific element to replace based on modification points
#             target_element = target_tree.xpath(modification_points[self.target[0]][self.target[1]])[0]
#             print("target_element before replace:", etree.tostring(target_element))

#             current_gate = target_element.get('gate')

#             alternative_gates = [...]
#             alternative_gates.remove(current_gate)

#             new_gate = random.choice(alternative_gates)
#             new_pexp = etree.Element(self.target_tag)
#             new_pexp.set('gate', new_gate)
#             new_pexp.set('id', target_element.get('id'))  # Ensure ID is preserved if needed

#             # Copy the children (vexp elements) from the original target element
#             for child in target_element:
#                 new_pexp.append(copy.deepcopy(child))

#             parent = target_element.getparent()
#             print("parent before replace:", etree.tostring(parent))
#             parent.replace(target_element, new_pexp)
#             print("parent after replace:", etree.tostring(parent))

#             new_target_content = etree.tostring(target_tree, pretty_print=True).decode('utf-8')
#             new_contents[self.target[0]] = new_target_content  # Update the new contents with modified XML
#             print("new_target_content:", new_target_content)
#             return True

#         return False

#     @classmethod
#     def create(cls, program, target_file=None, ingr_file=None, method='random'):
#         if target_file is None:
#             target_file = program.random_file(XmlEngine)
#         if ingr_file is None:
#             ingr_file = program.random_file(engine=program.engines[target_file])
#         assert program.engines[target_file] == program.engines[ingr_file]

#         # modify here
#         # 1. program.app_target(target_file, method)
#         # 2. program.app_target(ingr_file, 'random')
#         # 3. you will be able to see candidates here.
#         # 4. based on the candidates, you will do selection and perform different actions.
#         # 5. figure out what is the pexp type -- what the gate is
#         # 5.5, need to look at type env. variables map to types
#         # 6. if gate is SKIP, SKIP can be replaced to the right types,
#         # for example, if you look at the id, id = 'x' , then find x, then find x in the env ---> Nor/Phi
#         # for Nor, SKIP can be replaced by X, CU, QFT, for Phi, SKIP can be replaced by SR, RQFT
#         # 7. if gate is SR, it means that the id has Phi type, SR can be replaced by SR or SKIP
#         # 8. if gate is X, it means that the id of the gate is Nor type,
#         # X can be replaced by SKIP, or CU, but when replaced it with CU, need more work, CU has next level.
#         # 9. if gate is CU, it means that the id is Nor type, and it can be replaced by X, SKIP, with spectial treament

#         return cls(program.random_target(target_file, method),
#                    program.random_target(ingr_file, 'random'),
#                    'pexp')



# class CGateInsertion(StmtInsertion):
#     def __init__(self, target, ingredient, direction='before'):
#         super(CGateInsertion, self).__init__(target, ingredient, direction)

#     def apply(self, program, new_contents, modification_points):
#         print("C2Rust insertion apply")
#         engine = program.engines[self.target[0]]

#         result = self.do_insert(self, program,self, new_contents, modification_points, engine)
#         return result


#     def insert_into_parent(self, parent, target, ingredient):
#         # mutate
#         for i, child in enumerate(parent):
#             if child == target:
#                 tmp = copy.deepcopy(ingredient)
#                 if self.direction == 'after':
#                     tmp.tail = child.tail
#                     child.tail = None
#                     i += 1
#                 else:
#                     tmp.tail = None
#                 parent.insert(i, tmp)
#                 break
#         else:
#             assert False

#     def delete_block(self, parent):
#         for child in parent.findall("BLOCK"):
#             parent.remove(child)


#     def do_insert(self, cls, program, op, new_contents, modification_points, engine):
#         def pretty_print_element(element):
#             if element is None:
#                 return ""
#             raw_str = ET.tostring(element, 'utf-8')
#             parsed = minidom.parseString(raw_str)
#             return parsed.toprettyxml(indent="  ")

#         # get elements
#         target = new_contents[op._target[0]].find(modification_points[op._target[0]][op._target[1]])
#         parent = new_contents[op._target[0]].find(modification_points[op._target[0]][op._target[1]] + '..')
#         ingredient = program.contents[op.ingredient[0]].find(program.modification_points[op.ingredient[0]][op.ingredient[1]])

#         if target is None or ingredient is None:
#             return False

#         initial_type_env = type_envs[self.ingredient[0]]
#         print("Initial tenv",initial_type_env)
#         type_infer = TypeInfer(initial_type_env)
#         root = new_contents[op._target[0]].find('.')
#         # TODO
#         # figure this out
#         # type_infer.visitRoot(root)


#         block_el = ET.Element("BLOCK")

#         print("block:")
#         print(pretty_print_element(block_el))
#         print("ingredient:")
#         print(pretty_print_element(ingredient))
#         print("target:")
#         print(pretty_print_element(target))

#         self.insert_into_parent(parent, target, block_el)
#         print("parent after insert block",pretty_print_element(parent))
#         self.delete_block(parent)
#         print("parent after deletion",pretty_print_element(parent))
#         self.insert_into_parent(parent, target, ingredient)
#         print("parent after insert matched",pretty_print_element(parent))

#         # update modification points
#         head, tag, pos, _ = engine.split_xpath(modification_points[op._target[0]][op._target[1]])
#         for i, xpath in enumerate(modification_points[op._target[0]]):
#             if i < op._target[1]:
#                 continue
#             h, t, p, s = engine.split_xpath (xpath, head)
#             if h != head and xpath != 'deleted':
#                 break
#             if t == tag and p == pos and op.direction == 'after':
#                 continue
#             if t in [ingredient.tag, tag]:
#                 if s:
#                     new_pos = '{}/{}[{}]/{}'.format(h, t, p+1, s)
#                 else:
#                     new_pos = '{}/{}[{}]'.format(h, t, p+1)
#                 modification_points[op._target[0]][i] = new_pos
#         return True


#     @classmethod
#     def create(cls, program, target_file=None, ingr_file=None, direction=None, method='random'):
#         if target_file is None:
#             target_file = program.random_file(XmlEngine)
#         if ingr_file is None:
#             ingr_file = program.random_file(engine=program.engines[target_file])
#         assert program.engines[target_file] == program.engines[ingr_file]
#         if direction is None:
#             direction = random.choice(['before', 'after'])
#         return cls(program.app_target(target_file, method),program.app_target(ingr_file, 'random'),direction)
#     #modify here
#     #1. program.app_target(target_file, method)
#     #2. program.app_target(ingr_file, 'random')
#     #3. you will be able to see candidates here.
#        # app/if/pexp
#     # if see app, then only allowed if, and pexp
#     #if see if/pexp.
#      # choose a variable, will have the env to tell you what variables are aviable
#     # perform if/pexp on the variable
#     #look at the type of the variable in env, if it is Phi, then use SR/RQFT gate only
#     #if it is Nor, then use X, CU,
#     #if it is nat, can only use if with two branching



# class CGateDeletion(StmtDeletion):
#     def __init__(self, target):
#        super(CGateDeletion, self).__init__(target)

#     def apply(self, program, new_contents, modification_points):
#         print("C2Rust deletion apply")
#         engine = program.engines[self.target[0]]
#         result = engine.do_delete(program, self, new_contents, modification_points)
#         return result

#     def do_delete(self, program, new_contents, modification_points):
#         target_content = new_contents[self.target[0]]

#         target_tree = etree.fromstring(target_content)
#         target_element = target_tree.xpath(modification_points[self.target[0]][self.target[1]])[0]
#         parent = target_element.getparent()
#         parent.remove(target_element)

#         new_target_content = etree.tostring(target_tree, pretty_print=True).decode('utf-8')
#         return new_target_content

#     @classmethod
#     def create(cls, program, target_file=None, method='random'):
#         if target_file is None:
#             target_file = program.random_file(XmlEngine)
#         return cls(program.random_target(target_file, method))


# ==========================================================================
# Rust AST operators
# --------------------------------------------------------------------------
# Target selection (which point / which pair / which candidate) lives on the
# program, in CProgram.replace_target / CProgram.swap_target - the same split
# as CGateInsertion.create() -> program.app_target(). The operators only store
# the chosen ids and apply them to a freshly marked tree.
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

class MarkStripper(RustASTGenerator):
    """Rebuilds a tree with every MarkedASTNode wrapper removed."""

    def visitMarkedASTNode(self, node: MarkedASTNode):
        return node.node.accept(self)


class MarkedNodeSwapUpdater(RustASTGenerator):
    """Rebuilds the tree, putting `replacements[id]` (a wrapper) where the wrapper with that id was."""

    def __init__(self, replacements):
        super().__init__()
        self._replacements = replacements

    def visitMarkedASTNode(self, node: MarkedASTNode):
        replacement = self._replacements.get(node.get_id())
        if replacement is not None:          # `is not None`: never rely on node truthiness
            return replacement               # not descended into, so nothing is swapped twice
        return super().visitMarkedASTNode(node)


def strip_marks_tree(root):
    return root.accept(MarkStripper())


def _descendant_ids(wrapper):
    """Ids of all marked nodes strictly inside `wrapper`."""
    return {n.get_id() for n in NodeCollector(MarkedASTNode, lambda n: True).collect(wrapper.node)}


def _nested(a, b):
    """True if one of the two marked points lies inside the other."""
    return b.get_id() in _descendant_ids(a) or a.get_id() in _descendant_ids(b)


class RustSwapOperator(RustOperator):
    """Swaps the positions of two marked nodes.

    Only the two point ids are stored; the nodes are looked up in a freshly marked
    tree at apply time. Ids travel with the content, so no id is duplicated and
    applying the same swap twice restores the original tree. Nested pairs and
    structurally equal pairs are rejected (in CProgram.swap_target, and re-checked
    for nesting at apply time). The result is returned without MarkedASTNode wrappers."""

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

    def do_apply(self, new_contents):
        if self.point_a_id is None or self.point_b_id is None:
            return True  # nothing eligible at create time - no-op edit

        root = strip_marks_tree(new_contents[self.target_file])  # safe for marked or unmarked input
        marked_root = root.accept(MarkingVisitor())

        a = self._find_by_id(marked_root, self.point_a_id)
        b = self._find_by_id(marked_root, self.point_b_id)
        if a is None or b is None:
            return False  # a point vanished (earlier edit) - fail this edit, don't guess
        if _nested(a, b):
            return False  # an earlier edit made one contain the other

        updater = MarkedNodeSwapUpdater({self.point_a_id: b, self.point_b_id: a})
        new_contents[self.target_file] = strip_marks_tree(marked_root.accept(updater))
        return True

    @staticmethod
    def get_weight_initial():
        return 0.5
