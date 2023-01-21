from loaders import ConfigLoader, InstanceLoader
from mscn import ProfitCalculator, SolutionGenerator, ConstraintsValidator, MscnSolver, SolutionSplitter, SolutionReducer
import timeit

CONFIG_FILE_PATH = './config.yaml'
MAX_CALCULATION_TIME = 600

config = ConfigLoader.load(CONFIG_FILE_PATH)
# print(config)

insance_loader = InstanceLoader()
mscn_structure = insance_loader.load(config['instance_file_path'])

validator = ConstraintsValidator(mscn_structure)
profit_calculator = ProfitCalculator(mscn_structure)
solution_generator = SolutionGenerator(mscn_structure)
solution_splitter = SolutionSplitter(mscn_structure)
solution_reducer = SolutionReducer(mscn_structure, solution_splitter)


print("\n--------- Single random solution ---------------\n")

random_solution = solution_generator.generate()
is_random_solution_valid = validator.is_valid(solution=random_solution)
print(f"Is random solution valid? {is_random_solution_valid}")
random_solution_profit = profit_calculator.calculate(solution=random_solution)
print(f"Single random solution: {random_solution} with {random_solution_profit}$ profit!")


print("\n--------- Solution using differential evolution ---------------\n")
time_start = timeit.default_timer()

solution_history = []
solution_profit_history = []
while timeit.default_timer() - time_start < MAX_CALCULATION_TIME:
    solver = MscnSolver(
        profit_calculator=profit_calculator,
        validator = validator,
        generator = solution_generator,
        reducer = solution_reducer,
        time_start=time_start,
        max_calculation_time=MAX_CALCULATION_TIME
    )
    de_solution = solver.solve()
    solution_history.append(de_solution)
    de_solution_profit = profit_calculator.calculate(solution=de_solution)
    solution_profit_history.append(de_solution_profit)

best_de_solution_index = max(range(len(solution_profit_history)), key=solution_profit_history.__getitem__)
best_de_solution = solution_history[best_de_solution_index]
best_de_solution_profit = solution_profit_history[best_de_solution_index]

is_best_de_solution_valid = validator.is_valid(solution=best_de_solution)
print(f"Is solution using differential evolution valid? {is_best_de_solution_valid}")
print(f"Solution using differential evolution: {best_de_solution} with {best_de_solution_profit}$ profit!")

