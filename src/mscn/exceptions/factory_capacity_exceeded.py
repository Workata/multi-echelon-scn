
class FactoryCapacityExceeded(Exception):

    def __init__(self, factory_idx: int):
        self._factory_idx = factory_idx

    def __str__(self) -> str:
        return f"Factory {self._factory_idx} capacity has been exceeded!"

