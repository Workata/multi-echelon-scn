from .differential_evolution import minimize


class MscnSolver:

    POPULATION_SIZE = 10
    MUTATE_PROBABILITY = 0.5
    RECOMBINATION_PROBABILITY = 0.7
    MAX_NUM_OF_GENERATIONS = 100


    def __init__(self, profit_calculator, validator, generator, reducer):
        self._profit_calculator = profit_calculator
        self._validator = validator
        self._generator = generator
        self._reducer = reducer

    def solve(self):

        def cost_func(solution) -> float:
            # * de -> minimize so 1 / profit (we want to maximize profit)
            return 1/self._profit_calculator.calculate(solution)

        best_solution = minimize(
            cost_func, self.POPULATION_SIZE, self.MUTATE_PROBABILITY, self.RECOMBINATION_PROBABILITY,
            self.MAX_NUM_OF_GENERATIONS, self._validator, self._generator, self._reducer
        )
        return best_solution
