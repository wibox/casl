import matplotlib.pyplot as plt
import pandas as pd

from logger import Logger

class Warhol():
    def __init__(self, graph_path="../graphs"):
        self.graph_path=graph_path
    
    def make_visualization(self, filename, x, y, xlabel, ylabel):
        fig, ax = plt.subplots(figsize=(10, 5))

        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)

        ax.plot(x, y)
        fig.savefig(f"{self.graph_path}/{filename}.svg")

myLogger = Logger()
myWarhol = Warhol()
for log_file in myLogger.log_files:
    data = pd.read_csv(f"../{myLogger.log_path}/{log_file}")
    myWarhol.make_visualization(
                                filename=log_file,
                                x=data.iloc[:, 0],
                                y=data.iloc[:, 1],
                                xlabel=data.columns[0],
                                ylabel=data.columns[1])

