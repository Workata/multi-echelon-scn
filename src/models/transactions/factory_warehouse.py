from models import Factory, Warehouse
from typing import NamedTuple


# TODO use base
class FactoryWarehouseTransaction(NamedTuple):
    factory: Factory
    warehouse: Warehouse
    cost: int
    min_capacity: int
    max_capacity: int

    def __repr__(self) -> str:
        return (f"Factory ({self.factory.index}) --> Warehouse ({self.warehouse.index}): "
                f"cost ({self.cost}), min-max ({self.min_capacity}-{self.max_capacity})")
