
class FactoryOutcomeGreaterThanIncome(Exception):

    def __init__(self, factory_idx: int):
        self._factory_idx = factory_idx

    def __str__(self) -> str:
        return f"Factory {self._factory_idx} outcome is greater than its income!"
