from typing import List
from . import MscnStructure
import random


def get_rand_from_range(mini: float, maxi: float):
    return random.uniform(mini, maxi) # get random value from float range


def get_random_solution(mscn: MscnStructure):
    # num_of_supp_fac_conn = len(mscn_structure.suppliers) * len(mscn_structure.factories)
    # num_of_fac_ware_conn = len(mscn_structure.factories) * len(mscn_structure.warehouses)
    # num_of_ware_shop_conn = len(mscn_structure.warehouses) * len(mscn_structure.shops)
    solution = []

    for supp in mscn.suppliers:
        for fact in mscn.factories:

            supp_fact_trans = mscn.get_concrete_supplier_factory_transaction(supp, fact)

            # get_rand(min, max) -> supp, fact or 0
            # solution.append()



class Solution():
    instance: List[float]

    def __init__(self, ):
        pass

    def _calculate_transportation_costs(self, mscn_structure: MscnStructure) -> float:
        pass

    def _calculate_contract_costs(self, mscn_structure: MscnStructure) -> float:
        pass

    def _calculate_profit(self, mscn_structure: MscnStructure) -> float:
        pass

    def calculate_income(self, mscn_structure: MscnStructure) -> float:
        tranportation_costs = self._calculate_transportation_costs(mscn_structure)
        contract_costs = self._calculate_contract_costs(mscn_structure)
        profit = self._calculate_profit(mscn_structure)
        return profit - contract_costs - tranportation_costs

