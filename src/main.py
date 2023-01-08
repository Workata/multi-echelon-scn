from loaders import ConfigLoader, InstanceLoader
from mscn import ProfitCalculator, SolutionGenerator, ConstraintsValidator
from mscn.differential_evolution import do_stuff

CONFIG_FILE_PATH = './config.yaml'

config = ConfigLoader.load(CONFIG_FILE_PATH)
# print(config)

insance_loader = InstanceLoader()
mscn_structure = insance_loader.load(config['instance_file_path'])

validator = ConstraintsValidator(mscn_structure)
profit_calculator = ProfitCalculator(mscn_structure)
solution_generator = SolutionGenerator(mscn_structure)

random_solution = solution_generator.generate()
validator.is_valid(solution=random_solution)
profit_calculator.calculate(solution=random_solution)
print(f"Random solution: {random_solution}")



print("\n------------------------\n")
do_stuff(mscn_structure)
