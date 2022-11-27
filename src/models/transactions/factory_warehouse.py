from typing import TypedDict
from .. import Factory, Warehouse

class FactoryWarehouseTransaction(TypedDict):
    factory: Factory
    warehouse: Warehouse
    cost: float
