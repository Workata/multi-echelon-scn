from loaders import ConfigLoader, InstanceLoader
from mscn import ProfitCalculator, SolutionGenerator

CONFIG_FILE_PATH = './config.yaml'

config = ConfigLoader.load(CONFIG_FILE_PATH)
# print(config)
# print(type(config))

insance_loader = InstanceLoader()
mscn_structure = insance_loader.load(config['instance_file_path'])
random_solution = SolutionGenerator(mscn_structure = mscn_structure).generate()
print(random_solution)
print(len(random_solution))
# 2*3 + 3*3 + 3*5 - example1.yaml
assert len(random_solution) == 30


profit_calculator = ProfitCalculator(mscn_structure, solution=random_solution)
profit_calculator.calculate()

# print(mscn_structure)
# print("--------\n\n")
# supp = mscn_structure.suppliers[1]
# print(supp)
# fact = mscn_structure.factories[2]
# print(fact)
# trans_fact_supp = mscn_structure.get_concrete_supplier_factory_transaction(supp, fact)
# print(trans_fact_supp)
# print(type(mscn_structure))
