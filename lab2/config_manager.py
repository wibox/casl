import json
from sklearn.model_selection import ParameterGrid
from logger import Logger

myLogger = Logger(log_path="log")

myLogger.write_header("TIME,SPEED\n", filename=myLogger.log_files[1])
myLogger.write_header("TIME,AREA\n", filename=myLogger.log_files[0])
myLogger.write_header("TIME,NUM_PLAYERS\n", filename=myLogger.log_files[2])
myLogger.write_header("WINNERKILLS,AREA\n", filename=myLogger.log_files[3])
myLogger.write_header("WINNERKILLS,SPEED\n", filename=myLogger.log_files[4])
myLogger.write_header("WINNERKILLS,NUM_PLAYERS\n", filename=myLogger.log_files[5])
myLogger.write_header("AVGKILLS,AREA\n", filename=myLogger.log_files[6])
myLogger.write_header("AVGKILLS,SPEED\n", filename=myLogger.log_files[7])
myLogger.write_header("AVGKILLS,NUM_PLAYERS\n", filename=myLogger.log_files[8])

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
    'speed': [1, 2],
    'players':[2, 5, 10]
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
