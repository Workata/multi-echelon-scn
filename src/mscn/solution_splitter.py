from models import MscnStructure
from typing import List


class SolutionSplitter():
    """
    Divide solution for separate 3 stages
    TODO change naming
    """

    def __init__(self, mscn_structure: MscnStructure):
        self._mscn = mscn_structure

    def reduce_sublist(self, sublist, reduce_value):
        # TODO check
        reduced_sublist = []
        for x in sublist:
            reduced_sublist.append(0 if x - reduce_value < 0 else round(x - reduce_value, 2))
        return reduced_sublist

    def get_suppliers_to_factories_partial_solution(self, solution: List[float]) -> List[float]:
        return solution[0:self._mscn.supp_fact_paths_count]

    def replace_suppliers_to_factories_partial_solution(self, solution: List[float], sublist: List[float]) -> List[float]:
        solution[0:self._mscn.supp_fact_paths_count] = sublist
        return solution

    # TODO move this to reducer
    def reduce_concrete_supplier_to_factories_partial_solution(self, solution: List[float], supplier_id: int, reduce_value: float) -> List[float]:
        supplier_to_factories =  self.get_suppliers_to_factories_partial_solution(solution)
        supplier_idx = supplier_id - 1
        starting_idx = supplier_idx * self._mscn.factories_count
        ending_idx = starting_idx + self._mscn.factories_count

        supplier_to_factories[starting_idx:ending_idx] = self.reduce_sublist(supplier_to_factories[starting_idx:ending_idx], reduce_value)
        return self.replace_suppliers_to_factories_partial_solution(solution, supplier_to_factories)

    def get_factories_to_warehouses_partial_solution(self, solution: List[float]) -> List[float]:
        return solution[
            self._mscn.supp_fact_paths_count:self._mscn.supp_fact_paths_count+self._mscn.fact_wareh_paths_count
        ]

    def replace_factories_to_warehouses_partial_solution(self, solution: List[float], sublist: List[float]) -> List[float]:
        solution[
            self._mscn.supp_fact_paths_count:self._mscn.supp_fact_paths_count+self._mscn.fact_wareh_paths_count
        ] = sublist
        return solution

    # TODO move this to reducer
    def reduce_concrete_factory_to_warehouses_partial_solution(self, solution: List[float], factory_id: int, reduce_value: float) -> List[float]:
        factories_to_warehouses =  self.get_factories_to_warehouses_partial_solution(solution)
        factory_idx = factory_id - 1
        starting_idx = factory_idx * self._mscn.warehouses_count
        ending_idx = starting_idx + self._mscn.warehouses_count

        factories_to_warehouses[starting_idx:ending_idx] = self.reduce_sublist(factories_to_warehouses[starting_idx:ending_idx], reduce_value)
        return self.replace_factories_to_warehouses_partial_solution(solution, factories_to_warehouses)

    def get_warehouses_to_shops_partial_solution(self, solution: List[float]) -> List[float]:
        return solution[
            self._mscn.supp_fact_paths_count+self._mscn.fact_wareh_paths_count:self._mscn.all_paths_count
        ]

    def replace_warehouses_to_shops_partial_solution(self, solution: List[float], sublist: List[float]) -> List[float]:
        solution[
            self._mscn.supp_fact_paths_count+self._mscn.fact_wareh_paths_count:self._mscn.all_paths_count
        ] = sublist
        return solution

    # TODO move this to reducer
    def reduce_concrete_warehouse_to_shops_partial_solution(self, solution: List[float], warehouse_id: int, reduce_value: float) -> List[float]:
        warehouses_to_shops =  self.get_warehouses_to_shops_partial_solution(solution)
        warehouse_idx = warehouse_id - 1
        starting_idx = warehouse_idx * self._mscn.shops_count
        ending_idx = starting_idx + self._mscn.shops_count

        warehouses_to_shops[starting_idx:ending_idx] = self.reduce_sublist(warehouses_to_shops[starting_idx:ending_idx], reduce_value)
        return self.replace_warehouses_to_shops_partial_solution(solution, warehouses_to_shops)
