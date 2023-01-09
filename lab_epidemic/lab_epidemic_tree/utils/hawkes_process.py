from .clock import Clock
from .utils import Logger, Helper
from .ancestor_node import AncestorNode

import numpy as np
from tqdm import tqdm
from bigtree import dict_to_tree, print_tree, tree_to_dict, tree_to_dot, Node

from typing import *

import os
from time import time
from collections import OrderedDict
import math

class HawkesProcess():
    """
    Class that simulates Hawkes Process with according parameters.
    Acts as base class for HawkesProcessWithInterventions.
    """
    def __init__(
        self,
        h_t : str, # type of distribution from which to sample infection times
        a : int, # lower_bound for h_t == 'uniform'
        b : int, # upper_bound for h_t == 'uniform'
        l : float, # lambda for h_t == 'exp'
        m : int, # poisson's distribution parameter for generating infected nodes
        ancestors_rate : float, # rate at which ancestors arrive
        extinction_rate : float, # rate at which infected nodes die
        ancestors_horizon : int, # time limit after which no more ancestors can join the system
        time_horizon : int, # time limit after which infection's spreading simulation ends
        starting_time : int, # simulation starting time
        seed : int, # numpy's seed
        logger : Type[Logger], # Logger's class instance for general purpose logging
        log_to_file_bool : bool = True #whether or not to save <population> to file
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
        self.seed = seed
        np.random.seed(self.seed)
        self.logger = logger
        self.log_to_file_bool = log_to_file_bool

        self.infection_counter = 0
        self.death_counter = 0

    def _generate_ancestor_time(self) -> float:
        """
        Returns ancestor's "arrival time" according to PPP rate
        """
        return np.random.exponential(1/self.ancestors_rate)
        
    def _initialise_hprocess(self) -> Clock:
        """
        Initialises process's clock
        """
        return Clock()
        
    def _get_ht(self) -> float:
        """
        Returns instance of uniformely distributed or exponentially distributed RV for infection time generation
        """
        if self.h_t == "uniform":
            return np.random.uniform(low=self.a, high=self.b)
        elif self.h_t == "exp":
            return np.random.exponential(scale=1/self.l)
        
    def _simulate_hawkes_process(self, ancestor : AncestorNode):
        current_tree = dict()
        node_idx = 0
        nodes = [{"idx":node_idx, "is_alive":True, "infection_time":ancestor.infection_time, "pns":"0"}]
        current_tree[f"{node_idx}"] = {"infection_time":ancestor.infection_time}
        current_time = 0
        #pns : str = "0" # "parent node string" to keep track of generations and print final tree
        while current_time < self.time_horizon:
            for node in nodes:
                #pns += f"/{node['idx']}" if f"{node['idx']}" not in pns.split("/")[-1] and node['idx']>=node_idx else ""
                u = np.random.uniform(low=0, high=1)
                if u < self.extinction_rate:
                    node["is_alive"] = False
                    self.death_counter += 1
                else:
                    new_infections = np.random.poisson(lam=self.m)
                    self.infection_counter += new_infections
                    for infection_idx in range(new_infections):
                        new_infection_time = current_time + node["infection_time"] + self._get_ht()
                        pns = node['pns'] + (f"/{node_idx+infection_idx+1}" if f"{node_idx+infection_idx+1}" not in node['pns'].split("/") else "")
                        new_node = {
                            "idx":node_idx+infection_idx+1,
                            "infection_time":new_infection_time,
                            "is_alive":True,
                            "pns":pns
                        }
                        print(node_idx+infection_idx)
                        node_idx += 1
                        current_tree.update({f"{pns}":{"infection_time":new_node['infection_time']}})
                        nodes.extend([new_node])
                    break
            current_time += 1
        tree = dict_to_tree(current_tree)
        # print_tree(tree, attr_list=['infection_time'])
        Helper.log_json(filepath="log", filename="tree.json", data=current_tree)

    def _simulate_hawkes_process_v2(self, ancestor : AncestorNode):
        node_idx = 0
        root = Node(name=f"{node_idx}", infection_time=ancestor.infection_time, is_alive=True)
        nodes = [root]
        current_time = 0
        while current_time < self.time_horizon:
            for node in nodes:
                u = np.random.uniform(low=0, high=1)
                if u < self.extinction_rate:
                    node.is_alive = False
                    self.death_counter += 1
                else:
                    new_infections = np.random.poisson(lam=self.m)
                    self.infection_counter += new_infections
                    for infection_idx in range(new_infections):
                        new_tau = self._get_ht()
                        new_infection_time = current_time + node.infection_time + new_tau
                        node_idx += 1
                        new_node = Node(name=f"{node_idx+infection_idx+np.random.randint(low=0, high=int(1e16))}", infection_time=new_infection_time, is_alive=True, parent=node)
                        nodes.extend([new_node])
                break
            current_time += .1
        graph = tree_to_dot(root)
        graph.write_png("tree.png")

    def simulate(self) -> None:
        """
        Simulates an Hawkes process with a new of ancestors defined by self.ancestors_rate through a PPP.
        """
        process_clock : Clock = self._initialise_hprocess() #Global clock for the process
        ancestors : List[AncestorNode] = list() # global list of ancestors
        ancestor_counter : int = 0 # counter that keeps track of the number of generated ancestors

        while process_clock.current_time < self.ancestors_horizon:
            # generating an ancestor "arrival time" through PPP
            new_ancestor_time : float = self._generate_ancestor_time()
            # increasing time unit for process's clock to keep track of passing time
            process_clock.tick(amount=new_ancestor_time)
            # exit if new ancestor's "arrival time" is greater than specified time horizon
            if process_clock.current_time > self.ancestors_horizon:
                break
            # updating ancestors' list
            ancestors.append(AncestorNode(idx=ancestor_counter, infection_time=process_clock.current_time))
            ancestor_counter += 1

        self.logger.log_hp_msg(msg=f"Generated {len(ancestors)} ancestors.")
        sim_start_time = time()
        for ancestor_idx in tqdm(range(len(ancestors[:1]))):
            ancestor = ancestors[ancestor_idx]
            self._simulate_hawkes_process_v2(ancestor=ancestor)
        print("Total number of infections: ", self.infection_counter)
        print("Total number of deaths: ", self.death_counter)
        print(f"Percentage of deaths: {self.death_counter/self.infection_counter*100:.2f}%")
        print("Time to simulate: ", time() - sim_start_time)


    def simulate_v2(self):
        """
        Simulates an Hawkes process with a new of ancestors defined by self.ancestors_rate through a PPP.
        """
        process_clock : Clock = self._initialise_hprocess() #Global clock for the process
        ancestors : List[AncestorNode] = list() # global list of ancestors
        ancestor_counter : int = 0 # counter that keeps track of the number of generated ancestors

        while process_clock.current_time < self.ancestors_horizon:
            # generating an ancestor "arrival time" through PPP
            new_ancestor_time : float = self._generate_ancestor_time()
            # increasing time unit for process's clock to keep track of passing time
            process_clock.tick(amount=new_ancestor_time)
            # exit if new ancestor's "arrival time" is greater than specified time horizon
            if process_clock.current_time > self.ancestors_horizon:
                break
            # updating ancestors' list
            ancestors.append(AncestorNode(idx=ancestor_counter, infection_time=process_clock.current_time))
            ancestor_counter += 1

        self.logger.log_hp_msg(msg=f"Generated {len(ancestors)} ancestors.")
        sim_start_time = time()
        pandemic_evolution : Dict[float, int] = dict()
        pandemic_evolution_per_day : Dict[int, int] = dict()
        for ancestor_idx in tqdm(range(len(ancestors))):
            process_clock._reset_clock()
            ancestor = ancestors[ancestor_idx]
            # inserisco l'ancestor
            if pandemic_evolution.get(ancestor.infection_time) is None:
                pandemic_evolution[ancestor.infection_time] = 1
            else:
                pandemic_evolution[ancestor.infection_time] += 1
            # faccio generare all'ancestor un certo numero di tempi di infezione (prima generazione)
            new_infections = np.random.poisson(lam=self.m)
            for _ in range(new_infections):
                new_infection_time = self._get_ht()
                if pandemic_evolution.get(new_infection_time + ancestor.infection_time) is None:
                    pandemic_evolution[new_infection_time+ancestor.infection_time] = 1
                else:
                    pandemic_evolution[new_infection_time+ancestor.infection_time] += 1
            for infection in list(pandemic_evolution.keys()):
                while max(list(pandemic_evolution.keys())) < self.time_horizon:
            # while max(list(pandemic_evolution.keys())) < self.time_horizon:
            #     for infection in list(pandemic_evolution.keys()):
                    # print(max(list(pandemic_evolution.keys())), min(list(pandemic_evolution.keys())))
                    new_infections = np.random.poisson(lam=self.m)
                    for _ in range(new_infections):
                        new_infection_time = self._get_ht()
                        if pandemic_evolution.get(new_infection_time + infection) is None:
                            pandemic_evolution[new_infection_time+infection] = 1
                        else:
                            pandemic_evolution[new_infection_time+infection] += 1
        print(max(list(pandemic_evolution.values())))
            