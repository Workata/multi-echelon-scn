from models import MscnStructure
from typing import List


class ConstraintsValidator():
    """
    After creating new solution using DE (Differential Evolution) we have to check constraints.
    """

    def __init__(self, mscn_structure: MscnStructure, solution: List[float]):
        self._mscn = mscn_structure
        self._solution = solution


    def validate(self):
        pass


