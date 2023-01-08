from .de_simple import minimize
from models import MscnStructure
from . import ProfitCalculator, ConstraintsValidator, SolutionGenerator


def create_warehouses_shops_bounds(mscn_structure: MscnStructure):
    warehouses_shops_bounds = []
    for warehouse in mscn_structure.warehouses:
        for _ in mscn_structure.shops:
            warehouses_shops_bounds.append((0.0, warehouse.max_capacity))
    return warehouses_shops_bounds

def create_factories_warehouses_bounds(mscn_structure: MscnStructure):
    factories_warehouses_bounds = []
    for factory in mscn_structure.factories:
        for _ in mscn_structure.warehouses:
            factories_warehouses_bounds.append((0.0, factory.max_capacity))
    return factories_warehouses_bounds

def create_suppliers_factories_bounds(mscn_structure: MscnStructure):
    suppliers_factories_bounds = []
    for supplier in mscn_structure.suppliers:
        for _ in mscn_structure.factories:
            suppliers_factories_bounds.append((0.0, supplier.max_capacity))
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
    maxiter = 30    # max number of generations

    profit_calculator = ProfitCalculator(mscn_structure)
    validator = ConstraintsValidator(mscn_structure)
    solution_generator = SolutionGenerator(mscn_structure)

    def cost_func(solution) -> float:
        # de -> minimize so 1 / profit (we want to maximize profit)
        return 1/profit_calculator.calculate(solution)

    minimize(cost_func, bounds, population_size, mutate, recombination, maxiter, validator, solution_generator)






