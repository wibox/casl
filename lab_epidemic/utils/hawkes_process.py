from .clock import Clock
from .node import Node, AncestorNode, NodeEncoder
from .utils import Helper, Logger, Constants

import numpy as np

from typing import *
import os

# from json import JSONDecoder

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

    def _generate_ancestor_time(self) -> float:
        """
        Returns ancestor's "arrival time" according to PPP rate
        """
        return np.random.exponential(1/self.ancestors_rate)

    def _initialise_hprocess(self) -> Clock:
        """
        Initialises process's clock
        """
        return Clock(starting_time=self.clock_starting_time)
        
    def _get_ht(self) -> float:
        """
        Returns instance of uniformely distributed or exponentially distributed RV for infection time generation
        """
        if self.h_t == "uniform":
            return np.random.uniform(low=self.a, high=self.b)
        elif self.h_t == "exp":
            return np.random.exponential(scale=1/self.l)

    def _generate_hawkes_process(self, ancestor : AncestorNode) -> Tuple[Dict[int, List[Node]], bool, bool, int]:
        """
        This function enables the simulation of an Hawkes process.
        Args:
            ancestor : AncestorNode => One ancestor which acts as root_node for current process
        Returns:
            population : Dict[int, List[Node]] => a data structure recording the dynamics of the infection
            extinction_per_overtime : bool => True if extinction happened due to reacing self.time_horizon
            extinction_of_illness : bool => True if each node generated 0 new infected nodes
            death_counter : int => counter of total deaths caused by illness
        """
        # ancestor_nodes is the total list of nodes of the current hawkes process.
        # it is useful to keep the total number of nodes generated logged and to allow
        # nodes of previous generations to continue infections
        ancestor_nodes : List[Node] = list()
        population : Dict[int, List[Node]] = dict() # total population of the current hawkes process
        gen_idx : int = 0 # generation index
        extinction_per_overtime : bool = False # boolean variable used to address time limit
        extinction_of_illness : bool = False # boolean variable used to address illness's spreading
        death_counter : int = 0 # counter to keep track of deaths caused by the illness
        curr_time : float = ancestor.infection_time # starting time = ancestor's time
        # adding the first ancestor to total population
        # and global list of nodes for current hawkes process
        population[gen_idx] = [NodeEncoder().encode(ancestor)]
        ancestor_nodes.append(ancestor)
        # starting time loop for hawkes process
        while curr_time < self.time_horizon:
            self.logger.log_lp_msg(msg=f"Generation: {gen_idx}")
            # updating generation's time throught h_t(t)
            curr_infection_time = curr_time + self._get_ht()
            # breaking condition
            if gen_idx > len(population.keys())-1:
                self.logger.log_lp_msg(msg="Illness extinguished.")
                extinction_of_illness = True
                break
            # here it is decided if node should die or live (== keep infecting)
            # by means of a uniform distribution
            for node in ancestor_nodes:
                u = np.random.uniform(low=0, high=1)
                if u < self.extinction_rate:
                    node.is_alive = False
                    death_counter += 1
            # by iterating over every alive node in the hawkes process
            # each of them is allowed to keep infecting also after
            # their current generation. New infected nodes are inserted into last generation
            # since the whole process keeps track of the process's time.
            for node in ancestor_nodes:
                #node = JSONDecoder(object_hook=Helper.node_from_json).decode(node)
                if node.is_alive:
                    num_infected_children = node.infect(poisson_param=self.m)
                    if num_infected_children < 1:
                        node.is_alive = False
                        death_counter += 1
                        break
                    infected_children = [Node(infection_time=curr_infection_time, generation=gen_idx+1, is_alive=True) for i in range(num_infected_children)]
                    # here we update the total list of nodes in the current hawkes process
                    for infected_child in infected_children:
                        ancestor_nodes.append(infected_child)
                    # eventually the total population of the hawkes process is properly formatted for logging
                    # by means of a custom json encoder (inside Node class)
                    population[gen_idx+1] = [NodeEncoder().encode(child) for child in infected_children]
            # time is updated
            curr_time += curr_infection_time
            # check over time horizon
            if curr_time > self.time_horizon:
                self.logger.log_lp_msg(msg="Reached time horizon. Terminating current Hawkes process.")
                extinction_per_overtime = True
                break
            # generation index is updated
            gen_idx += 1
        return population, extinction_per_overtime, extinction_of_illness, death_counter

    def simulate_process(self) -> None:
        """
        Simulates an Hawkes process with a new of ancestors defined by self.ancestors_rate through a PPP.
        """
        process_clock : Clock = self._initialise_hprocess() #Global clock for the process
        ancestors : List[AncestorNode] = list() # global list of ancestors
        # counter useful for logging purposes.
        extinction_for_overtime_counter = 0 # counting how many times the hawkes process exits for overtime
        illness_extinction_counter = 0 # countering how many times the illneans goes extinct
        global_death_counter = 0 # counting how many death the overall process records

        while process_clock.current_time < self.ancestors_horizon:
            # generating an ancestor "arrival time" through PPP
            new_ancestor_time : float = self._generate_ancestor_time()
            # increasing time unit for process's clock to keep track of passing time
            process_clock.increase_time_unit(time_step=new_ancestor_time) 
            # updating ancestors' list
            ancestors.append(AncestorNode(infection_time=process_clock.current_time))
        
        self.logger.log_hp_msg(msg=f"Generated {len(ancestors)} ancestors.")
        # main data structure to log whole process
        population : Dict[str, Dict[str, Dict[int, List[Node]]]] = {"infections" : dict()}
        ancestor_counter = 0 # idx that allows keeping track of ancestors in <population>
        for ancestor in ancestors:
            self.logger.log_lp_msg(msg=f"Loading ancestor {ancestor_counter}")
            self.logger.log_lp_msg(msg=f"Resetting clock to {ancestor.infection_time}")
            process_clock._reset_clock() # resetting the process's clock
            process_clock.current_time = ancestor.infection_time # setting clock's starting time to current ancestors "arrival time"
            # initialise an hawkes process for each ancestor
            self.logger.log_lp_msg(msg=f"Starting Hawkes process for ancestor {ancestor_counter}")
            population['infections'][f'ancestor{ancestor_counter}'],\
                extinction_for_over_time,\
                    extinction_of_illnes,\
                        death_counter = self._generate_hawkes_process(ancestor=ancestor)
            # updating counters
            ancestor_counter += 1
            global_death_counter += death_counter
            if extinction_for_over_time:
                extinction_for_overtime_counter += 1
            if extinction_of_illnes:
                illness_extinction_counter += 1
        self.logger.log_hp_msg(msg=f"Times the process terminated for overtime: {extinction_for_overtime_counter}")
        self.logger.log_hp_msg(msg=f"Times the process terminated for illness extinction: {illness_extinction_counter}")
        self.logger.log_hp_msg(msg=f"Deaths: {global_death_counter}")
        # logging final results into json format is specified to do so
        if self.log_to_file_bool:
            self.logger.log_general_msg(msg=f"Logging Hawkes process information in {os.path.join(Constants.LOG_FOLDER_PATH, f'{self.seed}_{Constants.HAWKES_PROCESS_LOGFILENAME}')}")
            Helper.log_json(
                filepath=Constants.LOG_FOLDER_PATH,
                filename=f"{self.seed}_{Constants.HAWKES_PROCESS_LOGFILENAME}",
                data=population
            )
