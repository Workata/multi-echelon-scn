from random import random, sample
from typing import List
from .constraints_validator import (
    SupplierCapacityExceeded, FactoryCapacityExceeded, WarehouseCapacityExceeded, ShopCapacityExceeded,
    FactoryOutcomeGreaterThanIncome, WarehouseOutcomeGreaterThanIncome
)
import re
import timeit
import math


class DifferentialEvolution:

    def __init__(self, generator, validator, reducer) -> None:
        self._generator = generator
        self._validator = validator
        self._reducer = reducer

    def minimize(
        self, cost_func, popsize, mutate, recombination, tolerance, start_time, max_time
    ) -> List[float]:
        # * select starting population (list of solutions) - random based on bounds
        population = []
        for _ in range(popsize):
            population.append(self._generator.generate())

        best_sol_from_all_gens = population[0]
        best_sol_score_from_all_gens = math.inf
        best_gen_scores_history = []
        EARLY_STOP = False
        IS_TIME_UP = False

        # * cycle through as long as time permits or up to early stop condition
        while EARLY_STOP is not True and IS_TIME_UP is not True:

            gen_scores = []
            # * cycle through each individual in the population
            for j in range(popsize):

                # * mutation
                # select three random vector index positions [0, popsize), not including current vector (j)
                candidates = list(range(popsize))
                candidates.remove(j)
                random_index = sample(candidates, 3)

                x_1 = population[random_index[0]]
                x_2 = population[random_index[1]]
                x_3 = population[random_index[2]]

                # * added to ensure bounds after recombinations
                population[j] = self._force_bounds(population[j])
                x_t = population[j]

                # subtract x3 from x2, and create a new vector (x_diff)
                x_diff = [x_2_i - x_3_i for x_2_i, x_3_i in zip(x_2, x_3)]

                # multiply x_diff by the mutation factor (F) and add to x_1
                v_donor = [x_1_i + mutate * x_diff_i for x_1_i, x_diff_i in zip(x_1, x_diff)]
                # v_donor = ensure_bounds(v_donor, bounds)
                v_donor = self._force_bounds(v_donor)

                # * recombination
                v_trial = []
                for k in range(len(x_t)):
                    # random returns x in the internal of [0,1)
                    crossover = random()
                    if crossover <= recombination:
                        v_trial.append(v_donor[k])

                    else:
                        v_trial.append(x_t[k])

                # * added to ensure bounds after recombinations
                v_trial = self._force_bounds(v_trial)

                # * greedy selection
                score_trial  = cost_func(v_trial)
                score_target = cost_func(x_t)

                if score_trial < score_target:
                    population[j] = v_trial
                    gen_scores.append(score_trial)
                else:
                    gen_scores.append(score_target)

            # * score and validations
            gen_best = min(gen_scores)                                  # fitness of best individual
            gen_sol = population[gen_scores.index(min(gen_scores))]     # best individual from generation
            best_gen_scores_history.append(gen_best)
            if self._validator.is_valid(gen_sol):     # just in case check
                if best_sol_score_from_all_gens > gen_best:
                    best_sol_score_from_all_gens = gen_best
                    best_sol_from_all_gens = gen_sol

            # * EARLY STOPPING mechanism
            if len(best_gen_scores_history) > tolerance:
                best_gen_scores_history.pop(0)
                if min(best_gen_scores_history) > best_sol_score_from_all_gens or len(set(best_gen_scores_history)) == 1:
                    EARLY_STOP = True
            if timeit.default_timer() - start_time >= max_time:
                IS_TIME_UP = True

        return best_sol_from_all_gens

    def _extract_entity_id_from_err_msg(self, err_msg: str, pattern: str) -> int:
        id = int(re.search(pattern, err_msg, re.IGNORECASE).group(1))
        return id

    def _pre_reduction(self, solution: List[float]) -> List[float]:
        new_solution = []
        for val in solution:
            val = round(val, 2)
            new_solution.append(val if val >= 0 else 0)
        return new_solution

    def _force_bounds(self, solution: List[float]) -> List[float]:
        solution = self._pre_reduction(solution)

        while(not self._validator.is_valid(solution)):
            try:
                # this can be refactored cause right now it does double validation
                self._validator.is_valid(solution, raise_err=True)

            except SupplierCapacityExceeded as err:
                supplier_id = self._extract_entity_id_from_err_msg(err_msg=str(err), pattern='Supplier (.*) capacity')
                solution = self._reducer.reduce_concrete_supplier_to_factories_paths(solution, supplier_id)

            except FactoryCapacityExceeded as err:
                factory_id = self._extract_entity_id_from_err_msg(err_msg=str(err), pattern='Factory (.*) capacity')
                solution = self._reducer.reduce_concrete_factory_to_warehouses_paths(solution, factory_id)

            except WarehouseCapacityExceeded as err:
                warehouse_id = self._extract_entity_id_from_err_msg(err_msg=str(err), pattern='Warehouse (.*) capacity')
                solution = self._reducer.reduce_concrete_warehouse_to_shops_paths(solution, warehouse_id)

            except ShopCapacityExceeded as err:
                shop_id = self._extract_entity_id_from_err_msg(err_msg=str(err), pattern='Shop (.*) capacity')
                solution = self._reducer.reduce_warehouses_to_concrete_shop_paths(solution, shop_id)

            except FactoryOutcomeGreaterThanIncome as err:
                factory_id = self._extract_entity_id_from_err_msg(err_msg=str(err), pattern='Factory (.*) outcome')
                solution = self._reducer.reduce_concrete_factory_to_warehouses_paths(solution, factory_id)

            except WarehouseOutcomeGreaterThanIncome as err:
                warehouse_id = self._extract_entity_id_from_err_msg(err_msg=str(err), pattern='Warehouse (.*) outcome')
                solution = self._reducer.reduce_concrete_warehouse_to_shops_paths(solution, warehouse_id)

        return solution
