from hawkes_process import HawkesProcess
from utils.utils import Helper, Constants, Logger
from utils.custom_parser import get_parser

import os

if __name__ == "__main__":
    
    args = get_parser()

    myLogger = Logger(verbosity=args.verbosity)
    populations = list()
    for h_t in Constants.h_t:
        myLogger.log_general_msg(msg=f"Working with {h_t} h(t)")
        for seed in Constants.SEEDS:
            myLogger.log_general_msg(msg=f"Working with seed: {seed}")
            Helper.format_output(width=os.get_terminal_size()[0])
            hp = HawkesProcess(
                h_t = h_t,
                a = 0,
                b = 20,
                l = .1,
                m = 2,
                ancestors_rate=20,
                extinction_rate=.02,
                ancestors_horizon=10,
                time_horizon=100,
                starting_time=0,
                seed = seed,
                logger = myLogger
            )

            population = hp.simulate()
            populations.append(population)
            Helper.format_output(width=os.get_terminal_size()[0])
            
        formatted_population = Helper.compute_populations_statistics(populations=populations)
        mean = []
        lb = []
        up = []
        for item in list(formatted_population.values()):
            mean.append(item[0])
            lb.append(item[1])
            up.append(item[2])
        Helper.plot_results(mean=mean, lb=lb, up=up, h=h_t)