from typing import NamedTuple


class Shop(NamedTuple):
    index: int
    max_capacity: int   # capacity -> market demand
    income_per_product: int

    def __repr__(self) -> str:
        return f"{self.__class__.__name__} ({self.index}): cap ({self.max_capacity}), income ({self.income_per_product})"
