from .differential_evolution import minimize
import math

class MscnSolver:

    POPULATION_SIZE = 10
    MUTATE_PROBABILITY = 0.5
    RECOMBINATION_PROBABILITY = 0.7
    TOLERANCE = 200

    def __init__(self, profit_calculator, validator, generator, reducer, time_start, max_calculation_time):
        self._profit_calculator = profit_calculator
        self._validator = validator
        self._generator = generator
        self._reducer = reducer
        self.time_start = time_start
        self.max_calculation_time = max_calculation_time
    def solve(self):

        def cost_func(solution) -> float:
            """ de -> minimize so 1 / profit (we want to maximize profit) """
            profit = self._profit_calculator.calculate(solution)
            if profit == 0.0:
                return math.inf
            return 1/profit

        best_solution = minimize(
            cost_func, self.POPULATION_SIZE, self.MUTATE_PROBABILITY, self.RECOMBINATION_PROBABILITY,
            self._validator, self._generator, self._reducer, self.TOLERANCE, self.time_start, self.max_calculation_time
        )
        return best_solution
