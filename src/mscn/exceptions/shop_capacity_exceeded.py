
class ShopCapacityExceeded(Exception):  # capacity for shop = market demand

    def __init__(self, shop_idx: int):
        self._shop_idx = shop_idx

    def __str__(self) -> str:
        return f"Shop {self._shop_idx} capacity has been exceeded!"
