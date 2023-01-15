from loaders import ConfigLoader, InstanceLoader
from mscn import ProfitCalculator, SolutionGenerator, ConstraintsValidator, MscnSolver, SolutionSplitter, SolutionReducer

CONFIG_FILE_PATH = './config.yaml'

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

solver = MscnSolver(
    profit_calculator=profit_calculator,
    validator = validator,
    generator = solution_generator,
    reducer = solution_reducer
)
de_solution = solver.solve()
is_de_solution_valid = validator.is_valid(solution=de_solution)
print(f"Is solution using differential evolution valid? {is_de_solution_valid}")
de_solution_profit = profit_calculator.calculate(solution=de_solution)
print(f"Solution using differential evolution: {de_solution} with {de_solution_profit}$ profit!")

