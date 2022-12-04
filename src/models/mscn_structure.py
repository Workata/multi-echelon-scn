from typing import NamedTuple, List
from . import (
    Factory, Warehouse, Shop, Supplier, SupplierFactoryTransaction,
    FactoryWarehouseTransaction, WarehouseShopTransaction
)


class MscnStructure(NamedTuple):

    suppliers: List[Supplier]
    factories: List[Factory]
    warehouses: List[Warehouse]
    shops: List[Shop]

    supplier_factory_transactions: List[SupplierFactoryTransaction]
    factory_warehouse_transactions: List[FactoryWarehouseTransaction]
    warehouse_shop_transactions: List[WarehouseShopTransaction]
