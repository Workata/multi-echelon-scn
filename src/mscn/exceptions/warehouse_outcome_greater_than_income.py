

class WarehouseOutcomeGreaterThanIncome(Exception):
    def __init__(self, warehouse_idx: int):
        self._warehouse_idx = warehouse_idx

    def __str__(self) -> str:
        return f"Warehouse {self._warehouse_idx} outcome is greater than its income!"
