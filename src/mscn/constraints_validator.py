from models import MscnStructure
from typing import List
from .solution_splitter import SolutionSplitter
from .exceptions import (
    SupplierCapacityExceeded, FactoryCapacityExceeded, WarehouseCapacityExceeded, ShopCapacityExceeded,
    FactoryOutcomeGreaterThanIncome, WarehouseOutcomeGreaterThanIncome
)


InvalidSolutionExceptions = (
    SupplierCapacityExceeded, FactoryCapacityExceeded, WarehouseCapacityExceeded, ShopCapacityExceeded,
    FactoryOutcomeGreaterThanIncome, WarehouseOutcomeGreaterThanIncome
)

class ConstraintsValidator:
    """
    After creating new solution using DE (Differential Evolution) we have to check constraints.
    """

    def __init__(self, mscn_structure: MscnStructure):
        self._mscn = mscn_structure
        self._solution_splitter = SolutionSplitter(mscn_structure)


    def is_valid(self, solution: List[float], raise_err: bool = False) -> bool:

        try:
            # * supplier ---> factory
            delivered_to_factories = self._check_suppliers_to_factories_paths(solution)

            # * factory ---> warehouse
            delivered_to_warehouses = self._check_factories_to_warehouses_paths(solution, delivered_to_factories)

            # * warehouse ---> shop
            self._check_warehouses_to_shops_paths(solution, delivered_to_warehouses)
        except InvalidSolutionExceptions as err:
            print(f"[INFO] Given solution doesn't meet the restrictions! {err}")
            if raise_err:
                raise
            return False

        print("[INFO] Given solution is valid!")
        return True

    def _calculate_index_in_double_nested_list(self, outer_list_index: int, outer_list_len: int, inner_list_index: int):
        return outer_list_index*outer_list_len + inner_list_index

    def _check_suppliers_to_factories_paths(self, solution: List[float]) -> List[float]:
        suppliers_to_factories_paths: List[float] = self._solution_splitter.get_suppliers_to_factories_partial_solution(solution)
        suppliers_current_capacity: List[float] = [0.0 for _ in range(self._mscn.suppliers_count)]
        delivered_to_factories: List[float] = [0.0 for _ in range(self._mscn.factories_count)]

        for supp_idx, supp in enumerate(self._mscn.suppliers):
            for fact_idx, _ in enumerate(self._mscn.factories):
                path_idx = self._calculate_index_in_double_nested_list(supp_idx, self._mscn.suppliers_count, fact_idx)

                # * check constraints
                if suppliers_current_capacity[supp_idx] + suppliers_to_factories_paths[path_idx] > supp.max_capacity:
                    raise SupplierCapacityExceeded(supp.index)

                delivered_to_factories[fact_idx] += suppliers_to_factories_paths[path_idx]
                suppliers_current_capacity[supp_idx] += suppliers_to_factories_paths[path_idx]

        return delivered_to_factories

    def _check_factories_to_warehouses_paths(self, solution: List[float], delivered_to_factories: List[float]) -> List[float]:
        factories_to_warehouses_paths: List[float] = self._solution_splitter.get_factories_to_warehouses_partial_solution(solution)
        factories_current_capacity: List[float] = [0.0 for _ in range(self._mscn.factories_count)]
        delivered_to_warehouses: List[float] = [0.0 for _ in range(self._mscn.warehouses_count)]

        for fact_idx, fact in enumerate(self._mscn.factories):
            for wareh_idx, _ in enumerate(self._mscn.warehouses):
                path_idx = self._calculate_index_in_double_nested_list(fact_idx, self._mscn.factories_count, wareh_idx)

                # * check constraints
                if factories_current_capacity[fact_idx] + factories_to_warehouses_paths[path_idx] > fact.max_capacity:
                    raise FactoryCapacityExceeded(fact.index)
                if delivered_to_factories[fact_idx] - factories_to_warehouses_paths[path_idx] < 0:
                    raise FactoryOutcomeGreaterThanIncome(fact.index)

                delivered_to_factories[fact_idx] -= factories_to_warehouses_paths[path_idx]
                delivered_to_warehouses[wareh_idx] += factories_to_warehouses_paths[path_idx]
                factories_current_capacity[fact_idx] += factories_to_warehouses_paths[path_idx]

        return delivered_to_warehouses

    def _check_warehouses_to_shops_paths(self, solution: List[float], delivered_to_warehouses: List[float]) -> None:
        warehouses_to_shops_paths: List[float] = self._solution_splitter.get_warehouses_to_shops_partial_solution(solution)
        warhouses_current_capacity: List[float] = [0.0 for _ in range(self._mscn.warehouses_count)]
        shops_current_capacity: List[float] = [0.0 for _ in range(self._mscn.shops_count)]

        for wareh_idx, wareh in enumerate(self._mscn.warehouses):
            for shop_idx, shop in enumerate(self._mscn.shops):
                path_idx = self._calculate_index_in_double_nested_list(wareh_idx, self._mscn.warehouses_count, shop_idx)

                # * check constraints
                if warhouses_current_capacity[wareh.index-1] + warehouses_to_shops_paths[path_idx] > wareh.max_capacity:
                    raise WarehouseCapacityExceeded(wareh.index)
                if shops_current_capacity[shop.index-1] + warehouses_to_shops_paths[path_idx] > shop.max_capacity:
                    raise ShopCapacityExceeded(shop.index)
                if delivered_to_warehouses[wareh.index-1] - warehouses_to_shops_paths[path_idx] < 0:
                    raise WarehouseOutcomeGreaterThanIncome(wareh.index)

                delivered_to_warehouses[wareh.index-1] -= warehouses_to_shops_paths[path_idx]
                warhouses_current_capacity[wareh.index-1] += warehouses_to_shops_paths[path_idx]
                shops_current_capacity[shop.index-1] += warehouses_to_shops_paths[path_idx]

        return None
