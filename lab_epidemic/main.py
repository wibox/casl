from utils.hawkes_process import HawkesProcess

if __name__ == "__main__":
    hp = HawkesProcess(
        h_t = "uniform",
        a = 0,
        b = 20,
        l = .1,
        m = 2,
        ancestors_rate=20,
        extinction_rate=.2,
        ancestors_horizon=10,
        time_horizon=100,
        starting_time=0,
        simulate_interventions=False
    )

    hp.simulate_process()