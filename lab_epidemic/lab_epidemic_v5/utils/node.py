import numpy as np

class Node:
    def __init__(
        self,
        idx : int,
        infection_time : float,
        is_alive : bool = True,
        children : list = None,
        number_of_children : int = 0
    ):
        self.idx = idx
        self.infection_time = infection_time
        self.is_alive = is_alive
        if children:
            self.children = children
        else:
            self.children = list()
        self.number_of_children = number_of_children

    def infect(self, poisson_param : float):
        y_v = np.random.poisson(lam = poisson_param)
        return y_v

    def __str__(self) -> str:
        """
        Overriding Object's __str__ to give proper formatting. Mainly used during debugging
        """
        return f"Node{self.idx}"