from loaders import ConfigLoader, InstanceLoader

CONFIG_FILE_PATH = './config.yaml'

config = ConfigLoader.load(CONFIG_FILE_PATH)
# print(config)
# print(type(config))

insance_loader = InstanceLoader()
mscn_structure = insance_loader.load(config['instance_file_path'])
# print(mscn_structure)
# print(type(mscn_structure))


