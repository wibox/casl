from .clock import Clock
from .node import Node, AncestorNode, NodeEncoder
from .utils import Helper

import numpy as np
np.random.seed(299266)

from typing import *
import os
from json import JSONDecoder

class HawkesProcess():
    def __init__(
        self,
        h_t : str,
        a : int,
        b : int,
        l : float,
        m : int,
        ancestors_rate : float,
        extinction_rate : float,
        ancestors_horizon : int,
        time_horizon : int,
        starting_time : int,
        simulate_interventions : bool
    ):
        self.h_t = h_t
        self.a = a
        self.b = b
        self.l = l
        self.m = m
        self.ancestors_rate = ancestors_rate
        self.extinction_rate = extinction_rate
        self.ancestors_horizon = ancestors_horizon
        self.time_horizon = time_horizon
        self.clock_starting_time = starting_time
        self.simulate_interventions = simulate_interventions

        self.node_counter = 0

    def _generate_ancestor_time(self) -> float:
        return np.random.exponential(1/self.ancestors_rate)

    def _initialise_hprocess(self) -> Clock:
        process_clock = Clock(starting_time=self.clock_starting_time)
        return process_clock
        
    def _get_ht(self) -> float:
        if self.h_t == "uniform":
            return np.random.uniform(low=self.a, high=self.b)
        elif self.h_t == "exp":
            return np.random.exponential(scale=1/self.l)

    # def _generate_ancestor_epidemic(self, ancestor : AncestorNode) -> None:
    #     population : List[List[Node]] = list()
    #     population.append([ancestor])
    #     gen_idx = 0
    #     if ancestor:
    #         Helper.format_output(width=os.get_terminal_size()[0])
    #         print(f"Working with ancestor: {ancestor.idx}\nStarting time: {ancestor.infection_time}")
    #         curr_time = ancestor.infection_time
    #         ancestor.idx = self.node_counter
    #         while curr_time < self.time_horizon:
    #             if gen_idx > len(population)-1:
    #                 print("No more infections recorded.")
    #                 break
    #             print(f"\tInfecting generation {gen_idx+1}")
    #             curr_infection_time = curr_time + self._get_ht()
    #             for node in population[gen_idx]:
    #                 num_infected_children : float = node.infect(poisson_param=self.m)
    #                 print(f"\t\tNode {node.idx} infections: {num_infected_children} @ time: {curr_infection_time}")
    #                 infected_children : List[Node] = [Node(idx=node.idx+(i+1), generation=gen_idx, is_alive=True, infection_time=node.infection_time+curr_infection_time) for i in range(num_infected_children)]
    #                 population.append(infected_children)
    #                 self.node_counter += num_infected_children
    #             curr_time += curr_infection_time
    #             gen_idx += 1
    #     else:
    #         raise Exception("Ancestor is None.")

    def _test_generate_ancestor_epidemic(self, ancestor : AncestorNode) -> Dict[int, List[Node]]:
        population : Dict[int, List[Node]] = dict()
        gen_idx = 0
        population[gen_idx] = [NodeEncoder().encode(ancestor)]
        curr_time = ancestor.infection_time
        #print(f"Working with ancestor: {ancestor.idx}")
        while curr_time < self.time_horizon:
            curr_infection_time = curr_time + self._get_ht()
            if gen_idx > len(population.keys())-1:
                break
            for node in population.get(gen_idx):
                node = JSONDecoder(object_hook=Helper.node_from_json).decode(node)
                if node.is_alive:
                    num_infected_children = node.infect(poisson_param=self.m)
                    if num_infected_children < 1:
                        break
                    infected_children = [Node(infection_time=curr_infection_time, generation=gen_idx+1, is_alive=True) for i in range(num_infected_children)]
                    population[gen_idx+1] = [NodeEncoder().encode(item) for item in infected_children]
            curr_time += curr_infection_time
            gen_idx += 1
        return population

    def simulate_process(self) -> None:
        process_clock : Clock = self._initialise_hprocess()
        ancestors : List[AncestorNode] = list()

        while process_clock.current_time < self.ancestors_horizon:
            new_ancestor_time : float = self._generate_ancestor_time()
            process_clock.increase_time_unit(time_step=new_ancestor_time) 
            ancestors.append(AncestorNode(infection_time=process_clock.current_time))
        
        print(f"Generated {len(ancestors)} ancestors.")
        population : Dict[str, Dict[str, Dict[int, List[Node]]]] = {"infections" : dict()}
        ancestor_counter = 0
        for ancestor in ancestors:
            process_clock._reset_clock()
            process_clock.current_time = ancestor.infection_time
            # da qui in poi iniziamo il processo di simulazione per ogni ancestor con il tempo di quell'ancestor
            population['infections'][f'ancestor{ancestor_counter}'] = self._test_generate_ancestor_epidemic(ancestor=ancestor)
            ancestor_counter += 1
        Helper.log_json(filepath="log", filename="population.json", data=population)
