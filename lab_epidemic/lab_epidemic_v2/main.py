from hawkes_process import HawkesProcess
from utils.utils import Helper, Constants, Logger
from utils.custom_parser import get_parser

import os

if __name__ == "__main__":
    
    args = get_parser()

    myLogger = Logger(verbosity=args.verbosity)
    for seed in Constants.SEEDS:
        myLogger.log_general_msg(msg=f"Working with seed: {seed}")
        for h_t in Constants.h_t:
            myLogger.log_general_msg(msg=f"Working with {h_t} h(t)")
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

            hp.simulate()
            Helper.format_output(width=os.get_terminal_size()[0])