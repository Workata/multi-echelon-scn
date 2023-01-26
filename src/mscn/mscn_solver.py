from .differential_evolution import DifferentialEvolution
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
        self._time_start = time_start
        self._max_calculation_time = max_calculation_time

    def solve(self):

        def cost_func(solution) -> float:
            """ de -> minimize so 1 / profit (we want to maximize profit) """
            profit = self._profit_calculator.calculate(solution)
            if profit == 0.0:
                return math.inf
            return 1/profit

        de = DifferentialEvolution(self._generator, self._validator, self._reducer)
        best_solution = de.minimize(
            cost_func, self.POPULATION_SIZE, self.MUTATE_PROBABILITY, self.RECOMBINATION_PROBABILITY,
            self.TOLERANCE, self._time_start, self._max_calculation_time
        )
        return best_solution
