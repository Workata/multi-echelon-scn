from models import MscnStructure
from typing import List


class ConstraintsValidator():

    def __init__(self, mscn_structure: MscnStructure, solution: List[float]):
        self._mscn = mscn_structure
        self._solution = solution


    def validate(self):
        pass


