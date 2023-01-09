from .node import Node

class AncestorNode(Node):
    def __init__(
        self,
        infection_time : float,
        idx : int = 0,
        is_alive : bool = True,
        children : list = None,
        number_of_children : int = 0
    ):
        super().__init__(
            idx = idx,
            infection_time = infection_time,
            is_alive=is_alive,
            children=children,
            number_of_children=number_of_children
        )