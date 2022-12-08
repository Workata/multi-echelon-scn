from models import MscnStructure
from utils import YamlReader
from typing import List
from models import (
    Factory, Warehouse, Shop, Supplier, SupplierFactoryTransaction,
    FactoryWarehouseTransaction, WarehouseShopTransaction
)
import numpy as np


class InstanceLoader:
    """
        TODO refactor this shit
    """

    def load(self, instance_file_path: str) -> MscnStructure:
        print("[INFO] Loading instance...")
        instance_data = YamlReader.read(file_path=instance_file_path)

        shops = self._create_shops(instance_data)
        print(shops)
        factories = self._create_factories(instance_data)
        print(factories)
        warehouses = self._create_warehouses(instance_data)
        print(warehouses)
        suppliers = self._create_suppliers(instance_data)
        print(suppliers)

        factory_warehouse_transactions = self._create_factory_to_warehouse_transactions(instance_data, factories, warehouses)
        print(factory_warehouse_transactions)
        supplier_factory_transactions = self._create_supplier_to_factory_transactions(instance_data, suppliers, factories)
        print(supplier_factory_transactions)
        warehouse_shop_transactions = self._create_warehouse_to_shop_transactions(instance_data, warehouses, shops)
        print(warehouse_shop_transactions)

        mscn = MscnStructure(
            suppliers=suppliers,
            factories=factories,
            warehouses=warehouses,
            shops=shops,

            supplier_factory_transactions=supplier_factory_transactions,
            factory_warehouse_transactions=factory_warehouse_transactions,
            warehouse_shop_transactions=warehouse_shop_transactions
        )
        print(mscn)
        return mscn

    # TODO these methods (create_someting) are pretty similar
    # TODO so they can be somehow refactored
    def _create_shops(self, instance_data: dict) -> List[Shop]:
        shops = []
        num_of_shops = instance_data['S']
        shops_capacity = instance_data['ss']
        shops_income = instance_data['p']

        for i in range(num_of_shops):
            shops.append(Shop(
                index=i+1,
                max_capacity=shops_capacity[i],
                income_per_product=shops_income[i]
            ))
        return shops

    def _create_factories(self, instance_data: dict) -> List[Factory]:
        factories = []
        num_of_factories = instance_data['F']
        capacity = instance_data['sf']
        startup_cost = instance_data['uf']

        for i in range(num_of_factories):
            factories.append(Factory(
                index=i+1,
                max_capacity=capacity[i],
                startup_cost=startup_cost[i]
            ))
        return factories

    def _create_warehouses(self, instance_data: dict) -> List[Warehouse]:
        warehouses = []
        num_of_warehouses = instance_data['M']
        capacity = instance_data['sm']
        startup_cost = instance_data['um']

        for i in range(num_of_warehouses):
            warehouses.append(Warehouse(
                index=i+1,
                max_capacity=capacity[i],
                startup_cost=startup_cost[i]
            ))
        return warehouses

    def _create_suppliers(self, instance_data: dict) -> List[Supplier]:
        suppliers = []
        num_of_suppliers = instance_data['D']
        capacity = instance_data['sd']
        startup_cost = instance_data['ud']

        for i in range(num_of_suppliers):
            suppliers.append(Supplier(
                index=i+1,
                max_capacity=capacity[i],
                startup_cost=startup_cost[i]
            ))
        return suppliers

    def _create_factory_to_warehouse_transactions(self,
        instance_data: dict, factories: List[Factory], warehouses: List[Warehouse]
    ):
        transactions = []
        min_max_capacity = instance_data['xfminmax']
        cost = np.array(instance_data['cf'])
        matrix_shape = (len(factories), len(warehouses))
        cost_matrix = np.reshape(cost, matrix_shape)
        # print(cost_matrix)
        min_capacity = np.array(min_max_capacity[::2])
        min_capacity_matrix = np.reshape(min_capacity, matrix_shape)
        max_capacity = np.array(min_max_capacity[1::2])
        max_capacity_matrix = np.reshape(max_capacity, matrix_shape)
        # print(min_capacity)
        # print(max_capacity)
        for i, factory in enumerate(factories):
            for j, warehouse in enumerate(warehouses):
                transactions.append(FactoryWarehouseTransaction(
                    factory=factory,
                    warehouse=warehouse,
                    cost=cost_matrix[i][j],
                    min_capacity=min_capacity_matrix[i][j],
                    max_capacity=max_capacity_matrix[i][j]
                ))
        return transactions

    def _create_supplier_to_factory_transactions(self,
        instance_data: dict, suppliers: List[Supplier], factories: List[Factory]
    ):
        transactions = []
        min_max_capacity = instance_data['xdminmax']
        cost = np.array(instance_data['cd'])
        matrix_shape = (len(suppliers), len(factories))
        cost_matrix = np.reshape(cost, matrix_shape)
        # print(cost_matrix)
        min_capacity = np.array(min_max_capacity[::2])
        min_capacity_matrix = np.reshape(min_capacity, matrix_shape)
        max_capacity = np.array(min_max_capacity[1::2])
        max_capacity_matrix = np.reshape(max_capacity, matrix_shape)
        # print(min_capacity)
        # print(max_capacity)
        for i, supplier in enumerate(suppliers):
            for j, factory in enumerate(factories):
                transactions.append(SupplierFactoryTransaction(
                    supplier=supplier,
                    factory=factory,
                    cost=cost_matrix[i][j],
                    min_capacity=min_capacity_matrix[i][j],
                    max_capacity=max_capacity_matrix[i][j]
                ))
        return transactions

    def _create_warehouse_to_shop_transactions(self,
        instance_data: dict, warehouses: List[Warehouse], shops: List[Shop]
    ):
        transactions = []
        min_max_capacity = instance_data['xmminmax']
        cost = np.array(instance_data['cm'])
        matrix_shape = (len(warehouses), len(shops))
        cost_matrix = np.reshape(cost, matrix_shape)
        # print(cost_matrix)
        min_capacity = np.array(min_max_capacity[::2])
        min_capacity_matrix = np.reshape(min_capacity, matrix_shape)
        max_capacity = np.array(min_max_capacity[1::2])
        max_capacity_matrix = np.reshape(max_capacity, matrix_shape)
        # print(min_capacity)
        # print(max_capacity)
        for i, warehouse in enumerate(warehouses):
            for j, shop in enumerate(shops):
                transactions.append(WarehouseShopTransaction(
                    warehouse=warehouse,
                    shop=shop,
                    cost=cost_matrix[i][j],
                    min_capacity=min_capacity_matrix[i][j],
                    max_capacity=max_capacity_matrix[i][j]
                ))
        return transactions




