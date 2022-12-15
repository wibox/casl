from typing import *

from arc import Arc

class Node():
    def __init__(self, idx : int = 0, is_root : bool = False, generation : int = 0, parent_node : Any = None, arc : Arc = None):
        self.idx = idx
        self.is_root = is_root
        self.generation = generation
        self.parent_node = parent_node
        self.children = list()
        self.arc = arc.idx

        if self.parent_node is not None and self.is_root == True:
            raise Exception("Generated root node from parent. Aborting.")

    def _add_children(self, arcs : List[Arc] = None) -> Tuple[bool, int]:
        completed = False
        for arc in arcs:
            if arc.parent_node.idx == self.idx:
                self.children.append(arc.child_node)
            else:
                raise Exception("Vertex associated to wrong Node. Aborting.")
            completed = True
        return completed, len(self.children)

    def __str__(self) -> str:
        return f"Generation: {self.generation} \n Parent Node: {self.parent_node.idx} \n Number of children: {len(self.children)}"