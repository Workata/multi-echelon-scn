from typing import NamedTuple


class BaseEntity(NamedTuple):
    index: int
    max_capacity: int
    startup_cost: int

    def __repr__(self) -> str:
        return f"{self.__class__.__name__} ({self.index}): cap ({self.max_capacity}), startup ({self.startup_cost})"