from typing import NamedTuple
from models import Warehouse, Shop


# TODO use base
class WarehouseShopTransaction(NamedTuple):
    warehouse: Warehouse
    shop: Shop
    cost: int
    min_capacity: int
    max_capacity: int

    def __repr__(self) -> str:
        return (f"Warehouse ({self.warehouse.index}) --> Shop ({self.shop.index}): "
                f"cost ({self.cost}), min-max ({self.min_capacity}-{self.max_capacity})")
