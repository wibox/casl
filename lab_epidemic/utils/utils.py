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

    