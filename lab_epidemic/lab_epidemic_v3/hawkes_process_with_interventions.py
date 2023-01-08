from .hawkes_process import HawkesProcess
from utils.utils import Logger
from utils.clock import Clock

from typing import *

import numpy as np

class HawkesProcessWithInterventions(HawkesProcess):
    def __init__(
        self,
        time_for_interventions : int,
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
        super().__init__(
            h_t=h_t,
            a=a,
            b=b,
            l=l,
            m=m,
            ancestors_rate=ancestors_rate,
            extinction_rate=extinction_rate,
            ancestors_horizon=ancestors_horizon,
            time_horizon=time_horizon,
            starting_time=starting_time,
            seed=seed,
            logger=logger,
            log_to_file_bool=log_to_file_bool
        )
        self.time_for_interventions = time_for_interventions
    # COSTO = (k *) rho**2
    # VOGLIO TROVARE UN TRADEOFF TRA INTENSITA' STOCASTICA E COSTO(RHO)
    # ho la mia intensità
    # fino a T=20 questa intensità deve rimare la stessa
    # quando arrivo a T=20
        # genero il mio costo
        # scalo l'intensità per il costo
        # aumento il tempo
        # cosa succede al costo quando aumento il tempo in funzione del parametro rho?
        # ---> COSA SUCCEDE A RHO???
        # SICCOME VOGLIO LIMITARE IL NUMERO DI MORTI MEDI SU TUTTO IL PERIODO DI SIMULAZIONE
        # (UN ANNO) ALLORA:

        # COSTO PROPORIZIONALE A RHO**2
        # RHO VIENE CAMBIATO SULLA BASE DI m(T)/m(T-1)
        # CHE E' SINTOMO DIRETTO DI QUANTO IL COSTO SIA EFFETTIVO, INFATTI
        # SE IL COSTO AUMENTA TANTO --> IL NUMERO DI MORTI M(T) DIMINUISCE MOLTO E
        # CONSEGUENTMENTE RHO DIMINUISCE
        # SE INVECE IL COSTO DIMINUISCE, ALLORA IL NUMERO DI MORTI AUMENTA E RHO AUMENTA
        # RHO INIZIALE = 1 E AD OGNI GIORNO LO AUMENTO PER QUEL RAPPORTO
        # E DEFINISCO IL COSTO SEMPLICEMENTE COME RHO**2
        # COME LO INTERLACCIO CON L'INTENSITA?
        # DI SEGUITO L'INTENSITA' VIENE SCALATA DI UN FATTORE RHO 
        # SE RHO < 1 L'INTENSITA' DIMINUISCE E CONSEGUENTEMENTE DIMINUISCE IL NUMERO DI MORTI
        # E IL COSTO PUO' DIMINUIRE
        # E VICEVERSA

        """
        QUELLO CHE BISOGNA FARE E' RIUSCIRE A LEGARE OGNI PROCESSO DI HAWKES ALLA SUA INTENSITA'

        STIAMO LAVORANDO CON TEMPI DISCRETI E QUINDI L'INTENSITA' è UNA SEMPLICE SOMMATORIA CHE AUMENTA
        MAN MANO INIZIALIZZANDOLA A SIGMA*RHO
        LA SOMMATORIA DI TUTTE LE INTENSITA' DAL TEMPO OROGINARIO AL TEMPO CORRENTE E' IL NUMERO DI INFETTI
        AL TEMPO CORRENTE QUINDI IN QUESTO MODO POSSO EVITARE DI LAVORARE CON UN BRANCHING PROCESS
        E LAVORARE SEMPLICEMENTE CON L'INTENSITA' E I RELATIVI TEMPI
        """