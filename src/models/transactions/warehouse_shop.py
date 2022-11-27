from typing import TypedDict
from .. import Warehouse, Shop

class WarehouseShopTransaction(TypedDict):
    warehouse: Warehouse
    shop: Shop
    cost: float
