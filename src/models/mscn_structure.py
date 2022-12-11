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

    @property
    def suppliers_count(self):
        return len(self.suppliers)

    @property
    def factories_count(self):
        return len(self.factories)

    @property
    def warehouses_count(self):
        return len(self.warehouses)

    @property
    def shops_count(self):
        return len(self.shops)

    @property
    def supp_fact_paths_count(self):
        return self.suppliers_count * self.factories_count

    @property
    def fact_wareh_paths_count(self):
        return self.factories_count * self.warehouses_count

    @property
    def wareh_shop_paths_count(self):
        return self.warehouses_count * self.shops_count

    @property
    def all_paths_count(self):
        return self.supp_fact_paths_count + self.fact_wareh_paths_count + self.wareh_shop_paths_count

    def get_concrete_supplier_factory_transaction(self, supplier: Supplier, factory: Factory) -> SupplierFactoryTransaction:
        for transaction in self.supplier_factory_transactions:
            if transaction.supplier is supplier and transaction.factory is factory:
                return transaction

    def get_concrete_factory_warehouse_transaction(self, factory: Factory, warehouse: Warehouse) -> FactoryWarehouseTransaction:
        for transaction in self.factory_warehouse_transactions:
            if transaction.factory is factory and transaction.warehouse is warehouse:
                return transaction

    def get_concrete_warehouse_shop_transaction(self, warehouse: Warehouse, shop: Shop) -> WarehouseShopTransaction:
        for transaction in self.warehouse_shop_transactions:
            if transaction.warehouse is warehouse and transaction.shop is shop:
                return transaction
