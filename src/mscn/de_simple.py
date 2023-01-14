from random import random, sample, uniform
from typing import List
from .constraints_validator import (
    SupplierCapacityExceeded, FactoryCapacityExceeded, WarehouseCapacityExceeded, ShopCapacityExceeded,
    FactoryOutcomeGreaterThanIncome, WarehouseOutcomeGreaterThanIncome
)
import re

def ensure_bounds(vec, bounds):

    vec_new = []
    # cycle through each variable in vector
    for i in range(len(vec)):

        # variable exceedes the minimum boundary
        if vec[i] < bounds[i][0]:
            vec_new.append(bounds[i][0])

        # variable exceedes the maximum boundary
        if vec[i] > bounds[i][1]:
            vec_new.append(bounds[i][1])

        # the variable is fine
        if bounds[i][0] <= vec[i] <= bounds[i][1]:
            vec_new.append(round(vec[i], 2))

    return vec_new

DECREMENTOR = 0.1

def extract_entity_id_from_err_msg(err_msg: str, pattern: str) -> int:
    """this prob works"""
    id = int(re.search(pattern, err_msg, re.IGNORECASE).group(1))
    return id



def pre_reduction(solution):
    new_solution = []
    for val in solution:
        val = round(val, 2)
        new_solution.append(val if val >= 0 else 0)
    return new_solution

def force_bounds(solution: List[float], validator, splitter) -> List[float]:
    solution = pre_reduction(solution)
    counter = 0

    while(not validator.is_valid(solution)):
        try:
            print(f"Force bounds sol: {solution}")
            validator.is_valid(solution, raise_err=True)
        except SupplierCapacityExceeded as err:
            supplier_id = extract_entity_id_from_err_msg(err_msg=str(err), pattern='Supplier (.*) capacity')
            solution = splitter.reduce_concrete_supplier_to_factories_partial_solution(solution, supplier_id, DECREMENTOR)
            # return force_bounds(solution, validator, splitter)
        except FactoryCapacityExceeded as err:
            factory_id = extract_entity_id_from_err_msg(err_msg=str(err), pattern='Factory (.*) capacity')
            solution = splitter.reduce_concrete_factory_to_warehouses_partial_solution(solution, factory_id, DECREMENTOR)
            # return force_bounds(solution, validator, splitter)
        except WarehouseCapacityExceeded as err:
            warehouse_id = extract_entity_id_from_err_msg(err_msg=str(err), pattern='Warehouse (.*) capacity')
            solution = splitter.reduce_concrete_warehouse_to_shops_partial_solution(solution, warehouse_id, DECREMENTOR)
            # return force_bounds(solution, validator, splitter)
        except ShopCapacityExceeded as err:
            raise ShopCapacityExceeded
            # ???
            # supplier_id = extract_entity_id_from_err_msg(err_msg=str(err), pattern='Supplier (.*)')
            # solution = splitter.reduce_concrete_supplier_to_factories_partial_solution(solution, supplier_id, DECREMENTOR)
            # force_bounds(solution, validator)
        except FactoryOutcomeGreaterThanIncome as err:
            factory_id = extract_entity_id_from_err_msg(err_msg=str(err), pattern='Factory (.*) outcome')
            print(f"[FactoryOutcomeGreaterThanIncome] Reducing factory {factory_id}")
            solution = splitter.reduce_concrete_factory_to_warehouses_partial_solution(solution, factory_id, DECREMENTOR)
            # return force_bounds(solution, validator, splitter)
        except WarehouseOutcomeGreaterThanIncome as err:
            warehouse_id = extract_entity_id_from_err_msg(err_msg=str(err), pattern='Warehouse (.*) outcome')
            print(f"[WarehouseOutcomeGreaterThanIncome] Reducing warehouse {warehouse_id}")
            solution = splitter.reduce_concrete_warehouse_to_shops_partial_solution(solution, warehouse_id, DECREMENTOR)
            # return force_bounds(solution, validator, splitter)

        # counter += 1
        # if counter > 3:
        #     raise Exception("Dupa")

    return solution




def minimize(cost_func, bounds, popsize, mutate, recombination, maxiter, validator, solution_generator, splitter) -> None:

    # * starting population (list of solutions) - random based on bounds
    population = []
    # for i in range(0, popsize):
    #     indv = []
    #     for j in range(len(bounds)):
    #         indv.append(uniform(bounds[j][0], bounds[j][1]))
    #     population.append(indv)

    for _ in range(popsize):
        population.append(solution_generator.generate())

    #--- SOLVE --------------------------------------------+

    best_legal_solutions_counter = 0

    # * cycle through each generation (step #2)
    for i in range(1, maxiter + 1):
        print(f"GENERATION: {i}")
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
            population[j] = force_bounds(population[j], validator, splitter)
            x_t = population[j]



            # subtract x3 from x2, and create a new vector (x_diff)
            x_diff = [x_2_i - x_3_i for x_2_i, x_3_i in zip(x_2, x_3)]

            # multiply x_diff by the mutation factor (F) and add to x_1
            v_donor = [x_1_i + mutate * x_diff_i for x_1_i, x_diff_i in zip(x_1, x_diff)]
            # v_donor = ensure_bounds(v_donor, bounds)
            v_donor = force_bounds(v_donor, validator, splitter)

            #--- RECOMBINATION (step #3.B) ----------------+

            v_trial = []
            for k in range(len(x_t)):
                crossover = random()    # returns x in the internal of [0,1)
                if crossover <= recombination:
                    v_trial.append(v_donor[k])

                else:
                    v_trial.append(x_t[k])

            # * added to ensure bounds after recombinations
            v_trial = force_bounds(v_trial, validator, splitter)

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
        gen_sol = population[gen_scores.index(min(gen_scores))]     # solution of best individual
        if validator.is_valid(gen_sol):     # , raise_err=True
            best_legal_solutions_counter += 1

        print ('      > GENERATION AVERAGE:', gen_avg)
        print ('      > GENERATION BEST:', gen_best)
        print ('         > BEST SOLUTION:', gen_sol,'\n')

    print(f"Number of legal solutions: {best_legal_solutions_counter}")
    return None
