from .clock import Clock
from .node import Node, AncestorNode

import numpy as np

from typing import *

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

    def _generate_ancestor_time(self) -> float:
        return np.random.exponential(1/self.ancestors_rate)

    def _initialise_hprocess(self) -> Clock:
        process_clock = Clock(starting_time=self.clock_starting_time)
        return process_clock
        
    def _get_ht(self) -> float:
        if self.h_t == "uniform":
            return np.random.uniform(low=0, high=20)
        elif self.h_t == "exp":
            return np.random.exponential(scale=1/self.l)

    def _generate_ancestor_epidemic(self, ancestor : AncestorNode = None) -> None:
        if ancestor:
            curr_time = ancestor.infection_time
            while curr_time < self.time_horizon:
                pass
        else:
            raise Exception("Ancestor is None.")

    def simulate_process(self) -> None:
        process_clock : Clock = self._initialise_hprocess()
        ancestors : List[AncestorNode] = list()

        while process_clock.current_time < self.ancestors_horizon:
            new_ancestor_time : float = self._generate_ancestor_time()
            process_clock.increase_time_unit(time_step=new_ancestor_time) 
            ancestors.append(AncestorNode(infection_time=process_clock.current_time, idx=len(ancestors)))
        
        for ancestor in ancestors:
            process_clock._reset_clock()
            process_clock.current_time : float = ancestor.infection_time
            # da qui in poi iniziamo il processo di simulazione per ogni ancestor con il tempo di quell'ancestor
            self._generate_ancestor_epidemic(ancestor=ancestor)