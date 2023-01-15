from models import MscnStructure
from typing import List


class SolutionReducer:

    DECREMENTOR = 0.1

    def __init__(self, mscn_structure: MscnStructure, solution_splitter) -> None:
        self._mscn = mscn_structure
        self._splitter = solution_splitter

    def reduce_concrete_supplier_to_factories_paths(self, solution: List[float], supplier_id: int) -> List[float]:
        supplier_to_factories =  self._splitter.get_suppliers_to_factories_partial_solution(solution)
        supplier_idx = supplier_id - 1
        starting_idx = supplier_idx * self._mscn.factories_count
        ending_idx = starting_idx + self._mscn.factories_count

        supplier_to_factories[starting_idx:ending_idx] = self._reduce_sublist(supplier_to_factories[starting_idx:ending_idx])
        return self._replace_suppliers_to_factories_paths(solution, supplier_to_factories)

    def reduce_concrete_factory_to_warehouses_paths(self, solution: List[float], factory_id: int) -> List[float]:
        factories_to_warehouses =  self._splitter.get_factories_to_warehouses_partial_solution(solution)
        factory_idx = factory_id - 1
        starting_idx = factory_idx * self._mscn.warehouses_count
        ending_idx = starting_idx + self._mscn.warehouses_count

        factories_to_warehouses[starting_idx:ending_idx] = self._reduce_sublist(factories_to_warehouses[starting_idx:ending_idx])
        return self._replace_factories_to_warehouses_paths(solution, factories_to_warehouses)

    def reduce_concrete_warehouse_to_shops_paths(self, solution: List[float], warehouse_id: int) -> List[float]:
        warehouses_to_shops = self._splitter.get_warehouses_to_shops_partial_solution(solution)
        warehouse_idx = warehouse_id - 1
        starting_idx = warehouse_idx * self._mscn.shops_count
        ending_idx = starting_idx + self._mscn.shops_count

        warehouses_to_shops[starting_idx:ending_idx] = self._reduce_sublist(warehouses_to_shops[starting_idx:ending_idx])
        return self._replace_warehouses_to_shops_paths(solution, warehouses_to_shops)

    def _reduce_sublist(self, sublist):
        reduced_sublist = []
        for x in sublist:
            reduced_sublist.append(0.0 if x - self.DECREMENTOR < 0 else round(x - self.DECREMENTOR, 2))
        return reduced_sublist

    def _replace_suppliers_to_factories_paths(self, solution: List[float], suppliers_to_factories_paths: List[float]) -> List[float]:
        solution[0:self._mscn.supp_fact_paths_count] = suppliers_to_factories_paths
        return solution

    def _replace_factories_to_warehouses_paths(self, solution: List[float], factories_to_warehouses_paths: List[float]) -> List[float]:
        solution[
            self._mscn.supp_fact_paths_count:self._mscn.supp_fact_paths_count+self._mscn.fact_wareh_paths_count
        ] = factories_to_warehouses_paths
        return solution

    def _replace_warehouses_to_shops_paths(self, solution: List[float], warehouses_to_shops_paths: List[float]) -> List[float]:
        solution[
            self._mscn.supp_fact_paths_count+self._mscn.fact_wareh_paths_count:self._mscn.all_paths_count
        ] = warehouses_to_shops_paths
        return solution
