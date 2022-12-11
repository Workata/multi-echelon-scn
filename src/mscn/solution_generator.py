from models import Supplier, Shop, Factory, Warehouse, MscnStructure
from typing import List, Tuple
from utils import Randomizator
from random import shuffle


class SolutionGenerator:
    """
    Generate random solution (take constraints into account).
    TODO find out about random path/connection rejection (50/50, none etc) [currently turned off]
        TODO case: all connections not used on specific stage (check 0 values in sub list)
    TODO refactor this shit
    """

    def __init__(self, mscn_structure: MscnStructure):
        self._mscn = mscn_structure

    def generate(self) -> List[float]:

        # * supplier ---> factory
        suppliers_to_factories_paths, delivered_to_factories = self._get_suppliers_to_factories_paths()

        # * factory ---> warehouse
        factories_to_warehouses_paths, delivered_to_warehouses = self._get_factories_to_warehouses_paths(delivered_to_factories)

        # * warehouse ---> shop
        warehouses_shops_paths = self._get_warehouses_to_shops_paths(delivered_to_warehouses)

        return [*suppliers_to_factories_paths, *factories_to_warehouses_paths, *warehouses_shops_paths]

    def _calculate_index_in_double_nested_list(self, outer_list_index: int, outer_list_len: int, inner_list_index: int):
        return outer_list_index*outer_list_len + inner_list_index

    # * suppliers ---> factories (partial solution)
    def _get_suppliers_to_factories_paths(self) -> Tuple[List[float], List[float]]:
        suppliers_to_factories_paths: List[float] = [0.0 for _ in range(self._mscn.supp_fact_paths_count)]
        suppliers_current_capacity: List[float] = [0.0 for _ in range(self._mscn.suppliers_count)]
        delivered_to_factories: List[float] = [0.0 for _ in range(self._mscn.factories_count)]

        suppliers = self._mscn.suppliers.copy()
        shuffle(suppliers)
        factories = self._mscn.factories.copy()
        shuffle(factories)

        for supp in suppliers:
            for fact in factories:
                outer_idx = supp.index - 1
                inner_idx = fact.index - 1
                path_idx = self._calculate_index_in_double_nested_list(outer_idx, len(self._mscn.suppliers), inner_idx)

                supp_fact_transport_value = self._get_supp_fact_transport_value(supp, fact)
                # * check constraints
                if suppliers_current_capacity[supp.index-1] + supp_fact_transport_value > supp.max_capacity:
                    suppliers_to_factories_paths[path_idx] = 0.0    # connection not used
                    continue

                delivered_to_factories[fact.index-1] += supp_fact_transport_value
                suppliers_current_capacity[supp.index-1] += supp_fact_transport_value
                suppliers_to_factories_paths[path_idx] = supp_fact_transport_value

        return suppliers_to_factories_paths, delivered_to_factories

    def _get_factories_to_warehouses_paths(self, delivered_to_factories: List[float]) -> Tuple[List[float], List[float]]:
        factories_to_warehouses_paths: List[float] = [0.0 for _ in range(self._mscn.fact_wareh_paths_count)]
        factories_current_capacity: List[float] = [0.0 for _ in range(self._mscn.factories_count)]
        delivered_to_warehouses: List[float] = [0.0 for _ in range(self._mscn.warehouses_count)]

        factories = self._mscn.factories.copy()
        shuffle(factories)
        warehouses = self._mscn.warehouses.copy()
        shuffle(warehouses)

        for fact in factories:
            for wareh in warehouses:
                outer_idx = fact.index - 1
                inner_idx = wareh.index - 1
                path_idx = self._calculate_index_in_double_nested_list(outer_idx, len(self._mscn.factories), inner_idx)

                fact_wareh_transport_value = self._get_fact_wareh_transport_value(fact, wareh)
                # * check constraints
                if (factories_current_capacity[fact.index-1] + fact_wareh_transport_value > fact.max_capacity) or (
                    delivered_to_factories[fact.index-1] - fact_wareh_transport_value < 0
                ):
                    factories_to_warehouses_paths[path_idx] = 0.0   # connection not used
                    continue

                delivered_to_factories[fact.index-1] -= fact_wareh_transport_value
                delivered_to_warehouses[wareh.index-1] += fact_wareh_transport_value
                factories_current_capacity[fact.index-1] += fact_wareh_transport_value
                factories_to_warehouses_paths[path_idx] = fact_wareh_transport_value

        return factories_to_warehouses_paths, delivered_to_warehouses

    def _get_warehouses_to_shops_paths(self, delivered_to_warehouses: List[float]) -> List[float]:
        warehouses_to_shops_paths: List[float] = [0.0 for _ in range(self._mscn.wareh_shop_paths_count)]
        warhouses_current_capacity: List[float] = [0.0 for _ in range(self._mscn.warehouses_count)]
        shops_current_capacity: List[float] = [0.0 for _ in range(self._mscn.shops_count)]

        warehouses = self._mscn.warehouses.copy()
        shuffle(warehouses)
        shops = self._mscn.shops.copy()
        shuffle(shops)

        for wareh in warehouses:
            for shop in shops:
                outer_idx = wareh.index - 1
                inner_idx = shop.index - 1
                path_idx = self._calculate_index_in_double_nested_list(outer_idx, len(self._mscn.warehouses), inner_idx)

                wareh_shop_transport_value = self._get_wareh_shop_transport_value(wareh, shop)
                # * check constraints
                if (
                    warhouses_current_capacity[wareh.index-1] + wareh_shop_transport_value > wareh.max_capacity
                ) or (
                    shops_current_capacity[shop.index-1] + wareh_shop_transport_value > shop.max_capacity
                ) or (
                    delivered_to_warehouses[wareh.index-1] - wareh_shop_transport_value < 0
                ):
                    warehouses_to_shops_paths[path_idx] = 0.0    # connection not used
                    continue
                delivered_to_warehouses[wareh.index-1] -= wareh_shop_transport_value
                warhouses_current_capacity[wareh.index-1] += wareh_shop_transport_value
                shops_current_capacity[shop.index-1] += wareh_shop_transport_value
                warehouses_to_shops_paths[path_idx] = wareh_shop_transport_value

        return warehouses_to_shops_paths

    def _get_supp_fact_transport_value(self, supp: Supplier, fact: Factory) -> float:
        supp_fact_transaction = self._mscn.get_concrete_supplier_factory_transaction(supp, fact)
        return Randomizator.get_rand_float_from_range(supp_fact_transaction.min_capacity, supp_fact_transaction.max_capacity)

        # ? should we add this?
        # if Randomizator.is_coin_heads_up():
        #     return Randomizator.get_rand_float_from_range(supp_fact_transaction.min_capacity, supp_fact_transaction.max_capacity)
        # return 0.0  # connection not used

    def _get_fact_wareh_transport_value(self, fact: Factory, wareh: Warehouse) -> float:
        fact_wareh_transaction = self._mscn.get_concrete_factory_warehouse_transaction(fact, wareh)
        return Randomizator.get_rand_float_from_range(fact_wareh_transaction.min_capacity, fact_wareh_transaction.max_capacity)

    def _get_wareh_shop_transport_value(self, wareh: Warehouse, shop: Shop) -> float:
        wareh_shop_transaction = self._mscn.get_concrete_warehouse_shop_transaction(wareh, shop)
        return Randomizator.get_rand_float_from_range(wareh_shop_transaction.min_capacity, wareh_shop_transaction.max_capacity)
