from models import MscnStructure
from typing import List


class SolutionSplitter():
    """
    Divide solution for separate 3 stages
    """
    def __init__(self, mscn_structure: MscnStructure):
        self._mscn = mscn_structure

    def get_suppliers_to_factories_partial_solution(self, solution: List[float]) -> List[float]:
        return solution[0:self._mscn.supp_fact_paths_count]

    def get_factories_to_warehouses_partial_solution(self, solution: List[float]) -> List[float]:
        return solution[
            self._mscn.supp_fact_paths_count:self._mscn.supp_fact_paths_count+self._mscn.fact_wareh_paths_count
        ]

    def get_warehouses_to_shops_partial_solution(self, solution: List[float]) -> List[float]:
        return solution[
            self._mscn.supp_fact_paths_count+self._mscn.fact_wareh_paths_count:self._mscn.all_paths_count
        ]
