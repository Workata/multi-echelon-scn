from random import random, sample
from typing import List
from .constraints_validator import (
    SupplierCapacityExceeded, FactoryCapacityExceeded, WarehouseCapacityExceeded, ShopCapacityExceeded,
    FactoryOutcomeGreaterThanIncome, WarehouseOutcomeGreaterThanIncome
)
import re
import timeit

def extract_entity_id_from_err_msg(err_msg: str, pattern: str) -> int:
    id = int(re.search(pattern, err_msg, re.IGNORECASE).group(1))
    return id


def pre_reduction(solution):
    new_solution = []
    for val in solution:
        val = round(val, 2)
        new_solution.append(val if val >= 0 else 0)
    return new_solution


def force_bounds(solution: List[float], validator, reducer) -> List[float]:
    solution = pre_reduction(solution)

    while(not validator.is_valid(solution)):
        try:
            validator.is_valid(solution, raise_err=True)

        except SupplierCapacityExceeded as err:
            supplier_id = extract_entity_id_from_err_msg(err_msg=str(err), pattern='Supplier (.*) capacity')
            solution = reducer.reduce_concrete_supplier_to_factories_paths(solution, supplier_id)

        except FactoryCapacityExceeded as err:
            factory_id = extract_entity_id_from_err_msg(err_msg=str(err), pattern='Factory (.*) capacity')
            solution = reducer.reduce_concrete_factory_to_warehouses_paths(solution, factory_id)

        except WarehouseCapacityExceeded as err:
            warehouse_id = extract_entity_id_from_err_msg(err_msg=str(err), pattern='Warehouse (.*) capacity')
            solution = reducer.reduce_concrete_warehouse_to_shops_paths(solution, warehouse_id)

        except ShopCapacityExceeded as err:
            raise ShopCapacityExceeded      # TODO reduce solution per shop

        except FactoryOutcomeGreaterThanIncome as err:
            factory_id = extract_entity_id_from_err_msg(err_msg=str(err), pattern='Factory (.*) outcome')
            solution = reducer.reduce_concrete_factory_to_warehouses_paths(solution, factory_id)

        except WarehouseOutcomeGreaterThanIncome as err:
            warehouse_id = extract_entity_id_from_err_msg(err_msg=str(err), pattern='Warehouse (.*) outcome')
            solution = reducer.reduce_concrete_warehouse_to_shops_paths(solution, warehouse_id)

    return solution



def minimize(cost_func, popsize, mutate, recombination, validator, generator, reducer,tolerance, start_time, max_time) -> None:
    # * starting population (list of solutions) - random based on bounds
    population = []
    for _ in range(popsize):
        population.append(generator.generate())

    #--- SOLVE --------------------------------------------+

    best_legal_solutions_counter = 0
    best_sol_from_all_gens = population[0]
    best_sol_score_from_all_gens = 1000000
    best_gen_scores_history = []
    EARLY_STOP = False
    IS_TIME_UP = False
    # * cycle through each generation (step #2)
    while EARLY_STOP is not True and IS_TIME_UP is not True:

        gen_scores = [] # score keeping
        # * cycle through each individual in the population
        for j in range(popsize):

            #--- MUTATION (step #3.A) ---------------------+

            # select three random vector index positions [0, popsize), not including current vector (j)
            candidates = list(range(popsize))
            candidates.remove(j)
            random_index = sample(candidates, 3)

            x_1 = population[random_index[0]]
            x_2 = population[random_index[1]]
            x_3 = population[random_index[2]]
                 # target individual
            # * added to ensure bounds after recombinations
            population[j] = force_bounds(population[j], validator, reducer)
            x_t = population[j]

            # subtract x3 from x2, and create a new vector (x_diff)
            x_diff = [x_2_i - x_3_i for x_2_i, x_3_i in zip(x_2, x_3)]

            # multiply x_diff by the mutation factor (F) and add to x_1
            v_donor = [x_1_i + mutate * x_diff_i for x_1_i, x_diff_i in zip(x_1, x_diff)]
            # v_donor = ensure_bounds(v_donor, bounds)
            v_donor = force_bounds(v_donor, validator, reducer)

            #--- RECOMBINATION (step #3.B) ----------------+

            v_trial = []
            for k in range(len(x_t)):
                crossover = random()    # returns x in the internal of [0,1)
                if crossover <= recombination:
                    v_trial.append(v_donor[k])

                else:
                    v_trial.append(x_t[k])

            # * added to ensure bounds after recombinations
            v_trial = force_bounds(v_trial, validator, reducer)

            #--- GREEDY SELECTION (step #3.C) -------------+

            score_trial  = cost_func(v_trial)
            score_target = cost_func(x_t)

            if score_trial < score_target:
                population[j] = v_trial
                gen_scores.append(score_trial)
                # print( '   >', score_trial, v_trial)

            else:
                # print( '   >', score_target, x_t)
                gen_scores.append(score_target)

        #--- SCORE KEEPING --------------------------------+

        gen_avg = sum(gen_scores) / popsize                         # current generation avg. fitness
        gen_best = min(gen_scores)                                  # fitness of best individual
        gen_sol = population[gen_scores.index(min(gen_scores))]     # best individual from generation
        best_gen_scores_history.append(gen_best)
        if validator.is_valid(gen_sol):     # just in case check
            if best_sol_score_from_all_gens > gen_best:
                best_sol_score_from_all_gens = gen_best
                best_sol_from_all_gens = gen_sol
            best_legal_solutions_counter += 1

        #--- EARLY STOPPING ----------------+
        if len(best_gen_scores_history) > tolerance:
            best_gen_scores_history.pop(0)
            if min(best_gen_scores_history) > best_sol_score_from_all_gens or len(set(best_gen_scores_history)) == 1:
                EARLY_STOP = True
        if timeit.default_timer() - start_time >= max_time:
            IS_TIME_UP = True
        # print ('      > GENERATION AVERAGE:', gen_avg)
        # print ('      > GENERATION BEST:', gen_best)
        # print ('         > BEST SOLUTION:', gen_sol,'\n')

    # print(f"Number of legal solutions: {best_legal_solutions_counter}")
    return best_sol_from_all_gens