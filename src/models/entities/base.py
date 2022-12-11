from typing import NamedTuple, Optional


class BaseEntity(NamedTuple):
    index: int  # ! counted starting from from "1"
    max_capacity: float
    startup_cost: float

    def __repr__(self) -> str:
        return f"{self.__class__.__name__} ({self.index}): cap ({self.max_capacity}), startup ({self.startup_cost})"