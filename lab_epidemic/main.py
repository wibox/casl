from utils.hawkes_process import HawkesProcess
from utils.utils import Helper, Constants, Logger
from utils.custom_parser import get_parser

if __name__ == "__main__":
    args = get_parser()

    myLogger = Logger(verbosity=args.verbosity)
    
    for seed in Constants.SEEDS:
        hp = HawkesProcess(
            h_t = "uniform",
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

        hp.simulate_process()