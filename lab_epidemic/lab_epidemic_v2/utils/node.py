import numpy as np

class Node:
    def __init__(
        self,
        idx : int,
        infection_time : float,
        parent_node = None,
        is_alive : bool = True,
        children : list = None
    ):
        self.idx = idx
        self.infection_time = infection_time
        self.is_alive = is_alive
        self.parent_node = parent_node
        if children:
            self.children = children
        else:
            self.children = list()

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
        return f"Node{self.idx}"