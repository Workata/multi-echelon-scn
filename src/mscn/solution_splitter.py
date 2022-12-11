from models import MscnStructure
from typing import List


class SolutionSplitter():
    """
    Divide solution for separate 3 stages
    """
    def __init__(self, mscn_structure: MscnStructure, solution: List[float]):
        self._mscn = mscn_structure
        self._solution = solution

    def get_suppliers_to_factories_partial_solution(self) -> List[float]:
        supp_to_fact_paths = self._solution[0:self._mscn.supp_fact_paths_count]
        # print(f"Supp to fact paths: {supp_to_fact_paths}, {len(supp_to_fact_paths)}")
        return supp_to_fact_paths

    def get_factories_to_warehouses_partial_solution(self) -> List[float]:
        return self._solution[
            self._mscn.supp_fact_paths_count:self._mscn.supp_fact_paths_count+self._mscn.fact_wareh_paths_count
        ]

    def get_warehouses_to_shops_partial_solution(self) -> List[float]:
        return self._solution[
            self._mscn.supp_fact_paths_count+self._mscn.fact_wareh_paths_count:self._mscn.all_paths_count
        ]
