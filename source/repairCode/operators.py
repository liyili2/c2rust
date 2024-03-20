"""
Possible Edit Operators
"""
import random
from abc import ABC
#from pyggi.base import BaseOperator
from lxml import etree
from pyggi.tree import StmtReplacement, StmtInsertion, StmtDeletion

## Implement new operators here

class QGateReplacement(StmtReplacement):
    def __init__(self, target, ingredient, target_tag):
        super(QGateReplacement, self).__init__(target, ingredient)
        self.target_tag = target_tag

    def apply(self, program, new_contents, modification_points):
        engine = program.engines[self.target[0]]
        return engine.do_replace(program, self, new_contents, modification_points)

    def do_replace(self, program, new_contents, modification_points):
        target_content = new_contents[self.target[0]]
        ingredient_content = new_contents[self.ingredient[0]]

        # Parse the XML content
        target_tree = etree.fromstring(target_content)

        # Find all elements with the target tag and type='Nor'
        elements = target_tree.xpath(".//{}[@type='Nor']".format(self.target_tag))

        if elements:
            # Choose a random element to replace
            element_to_replace = random.choice(elements)

            # Parse the XML content of the ingredient
            ingredient_tree = etree.fromstring(ingredient_content)

            # Create a new <pexp> element with a different gate but the same type
            new_pexp = etree.Element(self.target_tag)
            new_pexp.set('gate', 'NewGate')  # Replace 'NewGate' with desired gate
            new_pexp.set('type', 'Nor')

            # Replace the chosen element with the new <pexp> element
            parent = element_to_replace.getparent()
            parent.replace(element_to_replace, new_pexp)

            # Serialize the modified XML back to a string
            new_target_content = etree.tostring(target_tree, pretty_print=True).decode('utf-8')

            return new_target_content

        return target_content


class QGateInsertion(StmtInsertion):
    def __init__(self, target, new_gate, target_tag):
        super(QGateInsertion, self).__init__(target)
        self.new_gate = new_gate
        self.target_tag = target_tag

    def apply(self, program, new_contents, modification_points):
        engine = program.engines[self.target[0]]
        return engine.do_insert(program, self, new_contents, modification_points)

    def do_insert(self, program, new_contents, modification_points):
        target_content = new_contents[self.target[0]]

        # Parse the XML content
        target_tree = etree.fromstring(target_content)

        # Find all elements with the target tag
        elements = target_tree.xpath(".//{}".format(self.target_tag))

        if elements:
            # Choose a random element to insert the new gate after
            insertion_point = random.choice(elements)

            # Parse the XML content of the new gate
            new_gate_tree = etree.Element(self.target_tag)
            new_gate_tree.set('gate', self.new_gate)
            new_gate_tree.set('type', 'Nor')

            # Insert the new gate after the chosen element
            parent = insertion_point.getparent()
            index = parent.index(insertion_point)
            parent.insert(index + 1, new_gate_tree)

            # Serialize the modified XML back to a string
            new_target_content = etree.tostring(target_tree, pretty_print=True).decode('utf-8')

            return new_target_content

        return target_content


class QGateDeletion(StmtDeletion):
    def __init__(self, target, target_tag):
        super(QGateDeletion, self).__init__(target)
        self.target_tag = target_tag

    def apply(self, program, new_contents, modification_points):
        engine = program.engines[self.target[0]]
        return engine.do_delete(program, self, new_contents, modification_points)

    def do_delete(self, program, new_contents, modification_points):
        target_content = new_contents[self.target[0]]

        # Parse the XML content
        target_tree = etree.fromstring(target_content)

        # Find all elements with the target tag
        elements = target_tree.xpath(".//{}".format(self.target_tag))

        if elements:
            # Choose a random element to delete
            element_to_delete = random.choice(elements)

            # Remove the chosen element
            parent = element_to_delete.getparent()
            parent.remove(element_to_delete)

            # Serialize the modified XML back to a string
            new_target_content = etree.tostring(target_tree, pretty_print=True).decode('utf-8')

            return new_target_content

        return target_content
