import json
import traceback
import os

from .node import Node

class Logger():
    def __init__(
        self,
        verbosity : int = 1
    ):
        self.verbosity=verbosity

    def log_msg(self, msg : str) -> None:
        if self.verbosity > 0:
            print(msg)

class Constants:
    LOG_FOLDER_PATH = "log"
    PLOT_FOLDER_PATH = "plots"

class Helper:

    @staticmethod
    def plot_results():
        pass

    @staticmethod
    def format_output(width : int) -> None:
        for _ in range(width):
            print("=", end="")


    @staticmethod
    def log_json(filepath : str, filename : str, data : dict) -> bool:
        completed = False
        try:
            with open(os.path.join(filepath, filename), "w") as fp:
                json.dump(data, fp, indent=4)
            completed = True
        except Exception as e:
            print(traceback.format_exc())
        finally:
            return completed 

    @staticmethod
    def node_from_json(json_obj) -> Node:
        return Node(
            infection_time=json_obj.get("infection_time"),
            generation=json_obj.get("generation"),
            is_alive=json_obj.get("is_alive")
        )