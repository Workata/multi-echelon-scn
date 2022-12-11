import random


class Randomizator:

    ROUND_TO_DECIMAL = 2

    @classmethod
    def get_rand_float_from_range(cls, mini: float, maxi: float) -> float:
        return round(random.uniform(mini, maxi), cls.ROUND_TO_DECIMAL)

    @classmethod
    def is_coin_heads_up(cls) -> bool:
        return random.randint(1, 2) == 1
