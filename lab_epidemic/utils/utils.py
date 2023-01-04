import json
import traceback
import os

from .node import Node

class Logger():
    """
    Simple Logger class employed in logging basic information about the ongoing Hawkes Process
    Args:
        verbosity: verbosity level for logging various types of messages. Suggested: 0
    """
    def __init__(
        self,
        verbosity : int = 1
    ):
        self.verbosity=verbosity

    def log_lp_msg(self, msg : str) -> None:
        if self.verbosity >= 1:
            print(msg)
    
    def log_hp_msg(self, msg : str) -> None:
        if self.verbosity >= 0:
            print(msg)
    
    def log_general_msg(self, msg : str) -> None:
        if self.verbosity == 0:
            print(msg)

class Constants:
    """
    Wrapper final class for the most used constants.
    """
    LOG_FOLDER_PATH = "log"
    PLOT_FOLDER_PATH = "plots"

    SEEDS = [247548, 299266, 777, 123456, 124056]
    h_t = ['exp', 'uniform']

    HAWKES_PROCESS_LOGFILENAME = "population.json"

class Helper:
    """
    Static class wrapping miscellaneous methods.
    """
    @staticmethod
    def plot_results():
        """
        Function used to plot requested informations.
        Args:
            ---
        Returns:
            None
        """
        pass

    @staticmethod
    def format_output(width : int) -> None:
        """
        Routine employed in formatting logger's messages in the terminal.
        Args:
            width : int => should be os.get_terminal_size()[0]
        """
        for _ in range(width):
            print("=", end="")


    @staticmethod
    def log_json(filepath : str, filename : str, data : dict) -> bool:
        """
        Logs json serialized data to file.
        Args:
            filepath : str => desired log folder
            filename : str => desired log filename
            data : dict => python object to be json-serialized
        """
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
        """
        Routine used to decode json data into custom Node class.
        Used in JSONDecoder for debugging purposes, should be called by JSONDecoder.object_hook
        Args:
            json_obj : Any => json serailized data
        Returns:
            Node's class instance
        """
        return Node(
            infection_time=json_obj.get("infection_time"),
            generation=json_obj.get("generation"),
            is_alive=json_obj.get("is_alive")
        )