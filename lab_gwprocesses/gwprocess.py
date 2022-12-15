from typing import *

from node import Node
from arc import Arc

import numpy as np

class GWProcess():
    def __init__(self, _lambda : float = 0, max_generation : int = 100):
        self._lambda = _lambda
        self._nodes_idx = 0
        self._arc_idx = 0
        self._generation_counter = 0
        self._nodes = list()
        self._root_node = None
        
        self.max_generation = max_generation
        self.extinction = False
        self.tree = list() # structure : [([arcs], [Nodes]), ([arcs], [Nodes]), ([arcs], [Nodes])] -> self.tree[k] == generation k

    def _process_ignition(self) -> Node:
        if self._nodes_idx > 0:
            raise Exception("Current process has no root node. Please restart.")
        else:
            self._root_node = Node(idx=self._nodes_idx, is_root=True, generation=self._generation_counter)
            self.tree.append(self._root_node)
        return self._root_node

    def _generate_children(self, p_node : Node = None) -> Tuple[int, List[Arc], List[Node], int]:
        """
        This function generates children for an input Node according to Poisson distribution with parameter self._lambda.
        """
        # first we generate the number of children
        gen_children = np.random.poisson(lam=self._lambda)
        # now we generate a number of arcs equals to the number of created children
        gen_arcs = [Arc(idx=self._arc_idx+i, parent_node=p_node) for i in range(gen_children)]
        # we set for each arc the children nodes
        gen_nodes = [Node(idx=self._nodes_idx+i, generation=self._generation_counter, parent_node=p_node.idx, arc=gen_arcs[i]) for i in range(gen_children)]
        for arc, arc_idx in zip(gen_arcs, range(len(gen_arcs))):
            arc.child_node = gen_nodes[arc_idx]
        # we set for each children node its corresponding arc
        self.tree.append((gen_arcs, gen_nodes))
        # increase instance generation counter
        self._generation_counter += 1
        # eventually we return arcs.
        return gen_children, gen_arcs, gen_nodes, self._generation_counter

    def run_simulation(self) -> bool:
        while not self.extinction and self._generation_counter<self.max_generation:
            pass
        
        return self.extinction