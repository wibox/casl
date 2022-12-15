from typing import *

from node import Node

class Arc():
    def __init__(self, idx : int = 0, parent_node : Node = None, child_nodes : List[Node] = None):
        self.idx = idx
        self.parent_node = parent_node
        self.child_node = child_nodes

    def __str__(self) -> str:
        return f"Vertex {self.idx}. \n Parent node: {self.parent_node.idx} \n Child node: {self.child_node.idx}"