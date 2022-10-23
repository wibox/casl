import json
from sklearn.model_selection import ParameterGrid

class ConfigSetter():
    def __init__(self, config_path, config_file):
        self.path=config_path
        self.config_file=config_file

    def write_config(self, configs):
        configurations = {'configurations':[]}
        try:
            with open(f"{self.path}/{self.config_file}", "w") as f:
                for config in configs:
                    configurations["configurations"].append(config)
                json.dump(configurations, f, indent=4)
        except:
            print(f"Error dealing with configurations file at {self.path}/{self.config_file}")

class ConfigGetter():
    def __init__(self, config_path, config_file):
        self.path=config_path
        self.config_file=config_file

    def retrieve_configs(self):
        try:
            with open(f"{self.path}/{self.config_file}", "r") as f:
                configs = json.load(f)
                return configs["configurations"]
        except:
            print(f"Error dealing with configurations file at {self.path}/{self.config_file}")
            return []

PARAMETERS = {
    'area' : [200, 400, 800],
    'speed': [1, 2, 3],
    'players':[2, 4, 5, 10]
}

CONFIG_PATH = "log"
CONFIG_FILE = "configurations.txt"

myConfigSetter = ConfigSetter(config_path=CONFIG_PATH, config_file=CONFIG_FILE)
myConfigSetter.write_config(configs=ParameterGrid(PARAMETERS))
myConfigGetter = ConfigGetter(config_path=CONFIG_PATH, config_file=CONFIG_FILE)
test_configurations = myConfigGetter.retrieve_configs()

with open("execute.sh", "w") as f:
    print(f"Writing {len(test_configurations)} configuratons to {myConfigGetter.path}/{myConfigGetter.config_file}")
    for configuration in test_configurations:
        f.write(f"python3 main.py --area {configuration['area']} --speed {configuration['speed']} --players {configuration['players']} \n")
