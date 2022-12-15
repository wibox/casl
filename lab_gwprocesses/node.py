from typing import *

class Node():
    def __init__(self, idx : int = 0, is_root : bool = False, generation : int = 0, children : List[Any] = None, parent_node : Any = None):
        self.idx = idx
        self.is_root = is_root
        self.children = children
        self.parent_node = parent_node
        self.generation = generation

        if self.parent_node is not None and self.is_root == True:
            raise Exception("Generated root node from parent. Aborting.")

    def _add_children(self, children : List[Any] = None) -> bool:
        completed = False
        if children and len(children) > 0:
            self.children = children
            completed = True
        else:
            raise Exception("Expected children list to not be None or Empty.")
        
        return completed

    def __str__(self) -> str:
        return f"Generation: {self.generation} \n Parent Node: {self.parent_node} \n Number of children: {len(self.children)}"