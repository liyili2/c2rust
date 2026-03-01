import random
from jmetal.core.operator import Mutation
from jmetal.util.ckecking import Check
from .cpatch import CPatch

"""
.. module:: mutation
   :platform: Unix, Windows
   :synopsis: Module implementing mutation operators.

.. moduleauthor:: 
"""
class NullMutation(Mutation[CPatch]):
    """
    Null Mutation which does nothing
    """
    def __init__(self):
        super(NullMutation, self).__init__(probability=0)

    def execute(self, solution: CPatch) -> CPatch:
        return solution

    def get_name(self):
        return 'Null mutation'

class PyGGiMutation(Mutation[CPatch]):
    """
    Pyggi Mutation which changes the pyggi edit lists
    """
    def __init__(self, probability):
        super(PyGGiMutation, self).__init__(probability=probability)

    def execute(self, solution: CPatch) -> CPatch:
        """
        What Mutations:
        Add to edit list

        Remove from edit list

        Change order of edit list [Not Implemented]

        Change an item in the item list (remove and replace in same location)
        """
        Check.that(type(solution) is CPatch, "Solution type invalid")

        edit_list_length = len(solution.edit_list)
        # For all items in the edit list
        for j in range(edit_list_length):
            rand = random.random()
            if rand <= self.probability:
                rnd = random.random()
                # 1/3rd Chance of removal
                if edit_list_length > 1 and rnd < 0.33:
                    if j < edit_list_length:
                        solution.remove(j)
                    j -= 1
                    edit_list_length -= 1
                # 1/3rd Chance of add
                elif edit_list_length == 0 or rnd < 0.66:
                    edit_operator = random.choice(solution.program.operators)
                    solution.add(edit_operator.create(solution.program))
                # 1/3rd Chance replace
                else:
                    edit_operator = random.choice(solution.program.operators)
                    if j < edit_list_length:
                        solution.edit_list[j] = edit_operator.create(solution.program)

        #print("Mutation Solution",solution.diff)
        return solution

    def get_name(self):
        return 'C2Rust Mutation'