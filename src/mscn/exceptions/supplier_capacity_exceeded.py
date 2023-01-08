
class SupplierCapacityExceeded(Exception):

    def __init__(self, supplier_idx: int):
        self._supplier_idx = supplier_idx

    def __str__(self) -> str:
        return f"Supplier {self._supplier_idx} capacity has been exceeded!"
