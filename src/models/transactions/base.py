from typing import NamedTuple


class BaseTransaction(NamedTuple):

    cost: int
    min_capacity: int
    max_capacity: int
