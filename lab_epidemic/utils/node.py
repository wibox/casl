import numpy as np
from json import JSONEncoder
from typing import *

class NodeEncoder(JSONEncoder):
    def default(self, o: Any) -> Any:
        return o.__dict__

class Node():
    def __init__(
        self,
        infection_time : float,
        generation : int,
        is_alive : bool
    ):
        self.infection_time = infection_time
        self.generation = generation
        self.is_alive = is_alive

    def infect(self, poisson_param : float):
        y_v = np.random.poisson(lam = poisson_param)
        return y_v

    def __str__(self) -> str:
        return f"Node: {self.idx}\nGeneration: {self.generation}\nInfection time: {self.infection_time}"

class AncestorNode(Node, JSONEncoder):
    def __init__(
        self,
        infection_time : float,
        is_alive : bool = True
    ):
        super().__init__(
            infection_time=infection_time,
            generation=0,
            is_alive=is_alive
            )

    def __str__(self) -> str:
        return f"Ancestor:{self.idx}\n\tInfection time: {self.infection_time}"