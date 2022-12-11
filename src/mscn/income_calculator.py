from models import MscnStructure
from typing import List


class IncomeCalculator():

    def __init__(self, mscn_structure: MscnStructure, solution: List[float]):
        self._mscn = mscn_structure
        self._solution = solution

    def calculate_income(self) -> float:
        tranportation_costs = self._calculate_transportation_costs()
        contract_costs = self._calculate_contract_costs()
        profit = self._calculate_profit()
        return profit - contract_costs - tranportation_costs

    def _calculate_transportation_costs(self) -> float:
        pass

    def _calculate_contract_costs(self) -> float:
        pass

    def _calculate_profit(self) -> float:
        pass


