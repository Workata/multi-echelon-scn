from typing import NamedTuple
from models import Factory, Supplier


# TODO use base
class SupplierFactoryTransaction(NamedTuple):
    supplier: Supplier
    factory: Factory
    cost: int
    min_capacity: int
    max_capacity: int

    def __repr__(self) -> str:
        return (f"Supplier ({self.supplier.index}) --> Factory ({self.factory.index}): "
                f"cost ({self.cost}), min-max ({self.min_capacity}-{self.max_capacity})")
