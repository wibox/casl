from .node import Node, AncestorNode

from typing import *

class LocalTree(object):
    def __init__(
        self,
        root_node : AncestorNode,
        children : List[Node] = None
    ):
        self.root_node = root_node
        if children:
            self.children = children
        else:
            self.children = list()

class GlobalTree(LocalTree):
    def __init__(
        self,
        root_node : AncestorNode,
        children : List[Node] = None
    ):
        super().__init__(
            
        )