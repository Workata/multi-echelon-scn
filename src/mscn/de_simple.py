from random import random, sample, uniform
from typing import List
from .constraints_validator import (
    SupplierCapacityExceeded, FactoryCapacityExceeded, WarehouseCapacityExceeded, ShopCapacityExceeded,
    FactoryOutcomeGreaterThanIncome, WarehouseOutcomeGreaterThanIncome
)


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

# def fix_supplier_capacity_exceeded_error(solution: List[float]) -> List[float]:
#     pass


# def force_bounds(solution: List[float], validator) -> None:
#     try:
#         validator.is_valid(solution, raise_err=True)
#     except SupplierCapacityExceeded:
#         solution = fix_supplier_capacity_exceeded_error(solution)
#         force_bounds(solution, validator)




def minimize(cost_func, bounds, popsize, mutate, recombination, maxiter, validator, solution_generator) -> None:

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
            x_t = population[j]     # target individual

            # subtract x3 from x2, and create a new vector (x_diff)
            x_diff = [x_2_i - x_3_i for x_2_i, x_3_i in zip(x_2, x_3)]

            # multiply x_diff by the mutation factor (F) and add to x_1
            v_donor = [x_1_i + mutate * x_diff_i for x_1_i, x_diff_i in zip(x_1, x_diff)]
            v_donor = ensure_bounds(v_donor, bounds)

            #--- RECOMBINATION (step #3.B) ----------------+

            v_trial = []
            for k in range(len(x_t)):
                crossover = random()
                if crossover <= recombination:
                    v_trial.append(v_donor[k])

                else:
                    v_trial.append(x_t[k])

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
