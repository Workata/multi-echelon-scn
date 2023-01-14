from .de_simple import minimize
from models import MscnStructure
from . import ProfitCalculator, ConstraintsValidator, SolutionGenerator, SolutionSplitter
import random


def divide_capacity_per_entity(capacity, num_of_entities):
    containers = [[] for _ in range(num_of_entities)]
    capacity_units = [1 for _ in range(capacity)]
    for capacity_unit in capacity_units:
        random.choice(containers).append(capacity_unit)
    return [len(container) for container in containers]


def create_warehouses_shops_bounds(mscn_structure: MscnStructure):
    warehouses_shops_bounds = []
    for warehouse in mscn_structure.warehouses:
        divided_capacity = divide_capacity_per_entity(warehouse.max_capacity, mscn_structure.shops_count)
        for idx, _ in enumerate(mscn_structure.shops):
            warehouses_shops_bounds.append((0.0, divided_capacity[idx]))
    return warehouses_shops_bounds

def create_factories_warehouses_bounds(mscn_structure: MscnStructure):
    factories_warehouses_bounds = []
    for factory in mscn_structure.factories:
        divided_capacity = divide_capacity_per_entity(factory.max_capacity, mscn_structure.warehouses_count)
        for idx, _ in enumerate(mscn_structure.warehouses):
            factories_warehouses_bounds.append((0.0, divided_capacity[idx]))
    return factories_warehouses_bounds

def create_suppliers_factories_bounds(mscn_structure: MscnStructure):
    suppliers_factories_bounds = []
    for supplier in mscn_structure.suppliers:
        divided_capacity = divide_capacity_per_entity(supplier.max_capacity, mscn_structure.factories_count)
        for idx, _ in enumerate(mscn_structure.factories):
            suppliers_factories_bounds.append((0.0, divided_capacity[idx]))
    return suppliers_factories_bounds


def create_bounds(mscn_structure: MscnStructure):
    bounds = []
    bounds.extend(create_suppliers_factories_bounds(mscn_structure))
    bounds.extend(create_factories_warehouses_bounds(mscn_structure))
    bounds.extend(create_warehouses_shops_bounds(mscn_structure))
    return bounds


def do_stuff(mscn_structure: MscnStructure):
    population_size =  10 # number of instances
    bounds = create_bounds(mscn_structure)
    mutate = 0.5
    recombination = 0.7
    maxiter = 3    # max number of generations, 30

    profit_calculator = ProfitCalculator(mscn_structure)
    validator = ConstraintsValidator(mscn_structure)
    solution_generator = SolutionGenerator(mscn_structure)
    solution_splitter = SolutionSplitter(mscn_structure)

    def cost_func(solution) -> float:
        # de -> minimize so 1 / profit (we want to maximize profit)
        return 1/profit_calculator.calculate(solution)

    minimize(cost_func, bounds, population_size, mutate, recombination, maxiter, validator, solution_generator, solution_splitter)
