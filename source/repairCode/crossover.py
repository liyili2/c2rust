import copy
from typing import List
from jmetal.operator.crossover import Crossover
from .patch import PyggiPatch

"""
.. module:: crossover
   :platform: Unix, Windows
   :synopsis: Module implementing crossover operator for PyGGI-JMetal.
"""
class PyggiCrossover(Crossover[PyggiPatch, PyggiPatch]):
    def __init__(self, probability: float):
        super(PyggiCrossover, self).__init__(probability=probability)

    def execute(self, parents: List[PyggiPatch]) -> List:
        if len(parents) != 2:
            raise Exception('The number of parents is not two: {}'.format(len(parents)))

        # crossover of a pair
        pa = copy.deepcopy(parents[0])
        pb = copy.deepcopy(parents[1])
        len1 = len(pa.edit_list)
        len2 = len(pb.edit_list)
        if len1 < 1 or len2 < 1:
            tmp = copy.deepcopy(pa.edit_list)
            pa.edit_list.extend(pb.edit_list)
            pb.edit_list.extend(tmp)
            return [pa, pb]

        mid1 = len1 // 2
        mid2 = len2 // 2
        pa.edit_list.extend(pb.edit_list[mid2:len2])
        pb.edit_list.extend(pa.edit_list[mid1:len1])
        del pa.edit_list[mid1:len1]
        del pb.edit_list[mid2:len2]

        return [pa, pb]

    def get_number_of_parents(self) -> int:
        return 2

    def get_number_of_children(self) -> int:
        return 2

    def get_name(self):
        return 'Crossover for JMetal-PyGGI'
