from typing import NamedTuple


class Shop(NamedTuple):
    index: int # ! counted starting from from "1"
    max_capacity: float   # capacity -> market demand
    income_per_product: float

    def __repr__(self) -> str:
        return f"{self.__class__.__name__} ({self.index}): cap ({self.max_capacity}), income ({self.income_per_product})"
