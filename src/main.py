from loaders import ConfigLoader, InstanceLoader

CONFIG_FILE_PATH = './config.yaml'

config = ConfigLoader.load(CONFIG_FILE_PATH)
# print(config)
# print(type(config))

insance_loader = InstanceLoader()
mscn_structure = insance_loader.load(config['instance_file_path'])
print(mscn_structure)
print("--------\n\n")
supp = mscn_structure.suppliers[1]
print(supp)
fact = mscn_structure.factories[2]
print(fact)
trans_fact_supp = mscn_structure.get_concrete_supplier_factory_transaction(supp, fact)
print(trans_fact_supp)
# print(type(mscn_structure))


