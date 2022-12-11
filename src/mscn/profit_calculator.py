from models import MscnStructure
from typing import List
from .solution_splitter import SolutionSplitter


class ProfitCalculator:
    """
    - Profit is the positive amount remaining after subtracting expenses incurred from the revenues
    - Income is the earnings gained from the provision of services or goods
    """

    def __init__(self, mscn_structure: MscnStructure, solution: List[float]):
        self._mscn = mscn_structure
        self._solution = solution
        self._solution_splitter = SolutionSplitter(mscn_structure, solution)

    def calculate(self) -> float:
        tranportation_costs = self._calculate_transportation_costs()
        contract_costs = self._calculate_contract_costs()
        income = self._calculate_income()
        profit = round(income - contract_costs - tranportation_costs, 2)
        print(f"PROFIT $$$: {profit}")
        return profit

    def _calculate_partial_trans_cost(self, paths, num_of_entities_from, num_of_entities_to, transactions):
        total_cost = 0.0
        for from_idx in range(num_of_entities_from):
            for to_idx in range(num_of_entities_to):
                idx = from_idx*num_of_entities_from + to_idx
                transport_amount = paths[idx]
                transport_cost = transactions[idx].cost
                total_cost += (transport_amount * transport_cost)
        return total_cost

    def _calculate_transportation_costs(self) -> float:
        """K_t"""
        supp_to_fact_trans_cost = self._calculate_partial_trans_cost(
            paths=self._solution_splitter.get_suppliers_to_factories_partial_solution(),
            num_of_entities_from=self._mscn.suppliers_count,
            num_of_entities_to=self._mscn.factories_count,
            transactions=self._mscn.supplier_factory_transactions
        )
        fact_to_wareh_trans_cost = self._calculate_partial_trans_cost(
            paths=self._solution_splitter.get_factories_to_warehouses_partial_solution(),
            num_of_entities_from=self._mscn.factories_count,
            num_of_entities_to=self._mscn.warehouses_count,
            transactions=self._mscn.factory_warehouse_transactions
        )
        wareh_to_shop_trans_cost = self._calculate_partial_trans_cost(
            paths=self._solution_splitter.get_warehouses_to_shops_partial_solution(),
            num_of_entities_from=self._mscn.warehouses_count,
            num_of_entities_to=self._mscn.shops_count,
            transactions=self._mscn.warehouse_shop_transactions
        )
        total_transportation_cost = round(supp_to_fact_trans_cost + fact_to_wareh_trans_cost + wareh_to_shop_trans_cost, 2)
        print(f"Total trans cost: {total_transportation_cost}")
        return total_transportation_cost

    def _calculate_contract_costs(self) -> float:
        return 0.0

    def _calculate_income(self) -> float:
        wareh_shops_paths=self._solution_splitter.get_warehouses_to_shops_partial_solution()
        shops_amount: List[float] = [0.0 for _ in range(self._mscn.shops_count)]

        for wareh_idx in range(self._mscn.warehouses_count):
            for shop_idx in range(self._mscn.shops_count):
                idx = wareh_idx*self._mscn.warehouses_count + shop_idx
                delivered_amount = wareh_shops_paths[idx]
                shops_amount[shop_idx] += delivered_amount

        all_shops_income = 0.0
        for idx, shop_amount in enumerate(shops_amount):
            all_shops_income += shop_amount*self._mscn.shops[idx].income_per_product
        all_shops_income = round(all_shops_income, 2)
        print(f"Total income: {all_shops_income}")
        return all_shops_income


