import numpy as np
from json import JSONEncoder
from typing import *

from .tree import LocalTree

class NodeEncoder(JSONEncoder):
    """
    Custom Json encoder to serialize Node class
    """
    def default(self, o: Any) -> Any:
        return o.__dict__

class Node():
    """
    Wrapper class encapsulating all the informations a node is supposed to carry:
    Args:
        infection_time : float => time at which current node has been infected
        generation : int => generation index referring to the generation at which Node has been infected
        is_alive : bool => whether current Node's instance is dead or alive.
    """
    def __init__(
        self,
        infection_time : float,
        # generation : int,
        is_alive : bool = True,
        tree : LocalTree = None
    ):
        self.infection_time = infection_time
        # self.generation = generation
        self.is_alive = is_alive
        self.tree = tree

    def infect(self, poisson_param : float):
        """
        Poisson's instance that gives the number of infected children a Node generates
        Args:
            poisson_param : float => pamater for sampling from the distribution
        Returns:
            y_v : float => instance of poisson r.v.; number of infected children by current Node
        """
        y_v = np.random.poisson(lam = poisson_param)
        return y_v

    def __str__(self) -> str:
        """
        Overriding Object's __str__ to give proper formatting. Mainly used during debugging
        """
        return f"Node: {self.idx}\nGeneration: {self.generation}\nInfection time: {self.infection_time}"

class AncestorNode(Node, JSONEncoder):
    """
    Node's child class, used to model Ancestor nodes. Mainly used for debugging purposes, a proper
    distinction between the two types of nodes in not really needed.
    Args:
        See Node()
    """
    def __init__(
        self,
        infection_time : float,
        is_alive : bool = True
    ):
        super().__init__(
            infection_time=infection_time,
            # generation=0,
            is_alive=is_alive
            )

    def __str__(self) -> str:
        """
        Overriding Object's __str__ to give proper formatting. Mainly used during debugging
        """
        return f"Ancestor:{self.idx}\n\tInfection time: {self.infection_time}"