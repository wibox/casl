import numpy as np
import matplotlib.pyplot as plt
np.random.seed(4899)
from utils import *

import time as t

SIMULATION_TIME = 100000

U = [0.1, 0.2, 0.4, 0.7, 0.8, 0.9, 0.95, 0.99]
S_TIME_FLAGS = ["det", "exp", "hyperexp"]

if __name__ == '__main__':
    #main event loop
    for u in U:
        print(f"Utilization value: {u}.")
        for s_time_flag in S_TIME_FLAGS:
            current_time = 0
            customers = 0
            queue = list()
            delays = list()
            FES = list()
            print(f"\tService time generated through {s_time_flag}")
            FES.append((0, "arrival"))
            queue.append(Customer(type="arrival", arrival_time=0))
            myLogger = Logger()
            while(current_time < SIMULATION_TIME):
                FES = sorted(FES, key=lambda x : x[0])
                time, event_type = FES.pop(0)
                current_time = time
                if len(queue) > 0:
                    if event_type == "arrival":
                        customers = arrival(customers=customers, time=current_time, queue=queue, FES=FES, logger=myLogger, service_time_flag=s_time_flag, u=u)
                    elif event_type == "departure":
                        customers, delay_time = departure(customers=customers, time=current_time, queue=queue, FES=FES, logger=myLogger, service_time_flag=s_time_flag)
                        delays.append(delay_time)
                else:
                    print("Queue is empty. Terminating.")
                    break
            delaymean = delay_mean(delays=delays)
            delay_wo_transient, transient_index = remove_transient(delaymean, u)
            plot_results(
                delays=delaymean,
                x_for_transient=transient_index,
                filepath="results/",
                filename=f"{u}_{s_time_flag}.png",
                show_flag=False,
                save_pict_flag=True,
                title=f"{u}, {s_time_flag}",
                label=f"{s_time_flag}"
            )

            correct_num_batches = find_number_of_batches(delays=delay_wo_transient, u=u, n=10)
            means, ci_lower, ci_upper = perform_batch_means(delays=delay_wo_transient, correct_n=correct_num_batches)
            plot_batch_means(delays_means=means,
                            delay_ci_lower=ci_lower,
                            delay_ci_upper=ci_upper,
                            filepath="batch_results/",
                            filename=f"{u}_{s_time_flag}.png",
                            show_flag=False,
                            save_pict_flag=True,
                            title=f"{u}, {s_time_flag}",
                            label=f"{s_time_flag}")
            

