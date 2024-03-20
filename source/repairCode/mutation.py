import random
from jmetal.core.operator import Mutation
from .patch import PyggiPatch

"""
.. module:: mutation
   :platform: Unix, Windows
   :synopsis: Module implementing mutation operators.

.. moduleauthor:: 
"""
class NullMutation(Mutation[PyggiPatch]):
    """
    Null Mutation which does nothing
    """
    def __init__(self):
        super(NullMutation, self).__init__(probability=0)

    def execute(self, solution: PyggiPatch) -> PyggiPatch:
        return solution

    def get_name(self):
        return 'Null mutation'

class PyggiMutation(Mutation[PyggiPatch]):
    """
    Pyggi Mutation which changes the pyggi edit lists
    """
    def __init__(self):
        super(NullMutation, self).__init__(probability=0)

    def execute(self, solution: PyggiPatch) -> PyggiPatch:
        """
        What Mutations:
        Add to edit list

        Remove from edit list

        Change order of edit list

        Change an item in the item list (remove and replace in same location)
        """
        return solution

    def get_name(self):
        return 'Pyggi mutation'