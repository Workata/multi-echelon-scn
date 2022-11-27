from typing import TypedDict
from .. import Factory, Supplier

class SupplierFactoryTransaction(TypedDict):
    supplier: Supplier
    factory: Factory
    cost: float
