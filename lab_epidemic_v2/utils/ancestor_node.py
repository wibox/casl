from .node import Node

class AncestorNode(Node):
    def __init__(
        self,
        infection_time : float,
        idx : int = 0,
        is_alive : bool = True,
        children : list = None
    ):
        super().__init__(
            idx = idx,
            infection_time = infection_time,
            is_alive=is_alive,
            children=children
        )
        self.parent_node = None

    # def __str__(self) -> str:
    #     """
    #     Overriding Object's __str__ to give proper formatting. Mainly used during debugging
    #     """
    #     return f"Infection time: {self.infection_time}"