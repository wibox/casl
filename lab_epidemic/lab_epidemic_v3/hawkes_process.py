from utils.clock import Clock
from utils.utils import Constants, Logger

import numpy as np
from tqdm import tqdm

from typing import *

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
        
    def simulate(self) -> None:
        """
        Simulates an Hawkes process with a new of ancestors defined by self.ancestors_rate through a PPP.
        """
        process_clock : Clock = self._initialise_hprocess() #Global clock for the process
        ancestors : List[float] = list() # global list of ancestors
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
            ancestors.append(process_clock.current_time)
            ancestor_counter += 1

        self.logger.log_hp_msg(msg=f"Generated {len(ancestors)} ancestors.")
        sim_start_time = time()
        evolution : Dict[float, int] = dict() # k=tempo di infezione, v=numero di infetti a quel tempo
        evolution_per_day : Dict[int, Tuple[int, int]] = dict() #k=indice del giorno, v=(n_infetti, n_morti)
        intensity : Dict[int, float] = dict() #v=valore, k=giorno
        for ancestor_idx in tqdm(range(len(ancestors))):
            process_clock._reset_clock()
            ancestor = ancestors[ancestor_idx]
            process_clock.current_time = ancestor
            while process_clock.current_time < self.time_horizon:
                taus = list()
                # genero un certo numero di nuove infezioni
                new_infections = np.random.poisson(lam=self.m)
                # genero dei tempi diversi per ogni infetto
                for _ in range(new_infections):
                    new_tau = process_clock.current_time + self._get_ht()
                    taus.append(new_tau)
                    # controllo che questo viva o muoia
                    u = np.random.uniform(low=0, high=1)
                    if u < self.extinction_rate:
                        pass # qui lo devo ammazzare
                    if not evolution.get(new_tau):
                        evolution[new_tau] = 1
                    else:
                        evolution[new_tau] += 1
                # appendo tutto in un dizionario globale: evolution
                process_clock.current_time += min(taus)
            # calcolo le statistiche finali con una funzione apposita
        print(evolution)
        print("Total number of infections: ", self.infection_counter)
        print("Total number of deaths: ", self.death_counter)
        print(f"Percentage of deaths: {self.death_counter/self.infection_counter*100:.2f}%")
        print("Time to simulate: ", time() - sim_start_time)