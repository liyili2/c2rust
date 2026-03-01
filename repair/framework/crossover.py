import copy
from typing import List
from jmetal.operator.crossover import Crossover
from .cpatch import CPatch

"""
.. module:: crossover
   :platform: Unix, Windows
   :synopsis: Module implementing crossover operator for PyGGI-JMetal.
"""
class PyGGiCrossover(Crossover[CPatch, CPatch]):
    def __init__(self, probability: float):
        super(PyGGiCrossover, self).__init__(probability=probability)

    def execute(self, parents: List[CPatch]) -> List:
        if len(parents) != 2:
            raise Exception('The number of parents is not two: {}'.format(len(parents)))
        print("CROSSOVER!!")
        # crossover of a pair
        parent_a = copy.deepcopy(parents[0])
        parent_b = copy.deepcopy(parents[1])
        len_parent_a = len(parent_a.edit_list)
        len_parent_b = len(parent_b.edit_list)
        # If either edit list is empty, return the other parent
        if len_parent_a < 1 or len_parent_b < 1:
            tmp = copy.deepcopy(parent_a.edit_list)
            parent_a.edit_list.extend(parent_b.edit_list)
            parent_b.edit_list.extend(tmp)
            return [parent_a, parent_b]
        # crossover point is the middle of the list
        mid1 = len_parent_a // 2
        mid2 = len_parent_b // 2
        parent_a.edit_list.extend(parent_b.edit_list[mid2:len_parent_b])
        parent_b.edit_list.extend(parent_a.edit_list[mid1:len_parent_a])
        del parent_a.edit_list[mid1:len_parent_a]
        del parent_b.edit_list[mid2:len_parent_b]
        #print("parenta" , parent_a.diff,"/n parentb",parent_b.diff)
        return [parent_a, parent_b]

    def get_number_of_parents(self) -> int:
        return 2

    def get_number_of_children(self) -> int:
        return 2

    def get_name(self):
        return 'Crossover for C2Rust'
