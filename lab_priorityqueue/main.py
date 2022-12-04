import numpy as np
np.random.seed(299266)
import matplotlib.pyplot as plt

from typing import *

import argparse
import os

from sympy import symbols, Eq, solve

SIMULATION_TIME = 1000

class Logger():

    def __init__(self, verbosity : int = 0):
        self.verbosity = verbosity

    def log_departure(self, time : float, queue_length : int) -> None:
        if self.verbosity==2:
            print(f"Departure at time: {time}. Current Queue length: {queue_length}.")
        else:
            pass

    def log_arrival(self, time : float, queue_length : int) -> None:
        if self.verbosity==2:
            print(f"Arrival scheduled at time: {time}. Current Queue length: {queue_length}.")
        else:
            pass

class Server():
    def __init__(self, id : int, status : str, customer):
        self.id = id
        self.status = status
        self.customer = customer

class Customer():
    def __init__(self, type : str, arrival_time : float, priority : str, server : Server):
        self.type = type
        self.arrival_time = arrival_time
        self.priority = priority
        self.server = server

def boot_servers(k : int) -> List[Server]:
    return [Server(id=i, status="idle", customer=None) for i in range(k)]

def generate_arrival_time(priority : str, lhp : float, llp : float) -> float:
    if priority == "LP":
        return np.random.exponential(1/llp)
    elif priority == 'HP':
        return np.random.exponential(1/lhp)
    else:
        raise Exception("Invalid priority selected for customer. No arrival time can be generated.")

def hyperexp_s_time(mean : float, std : float) -> float:

    p = .5

    l1, l2 = symbols("lambda1 lambda2")

    eq1 = Eq(p/l1 + (1-p)/l2, mean)
    eq2 = Eq(2*p/(l1**2) + 2*(1-p)/(l2**2)-mean, std**2)

    sols = solve((eq1,eq2), (l1, l2))

    l1 = sols[0][0]
    l2 = sols[0][1]

    U1 = np.random.uniform()
    if U1 <= p:
        l = l1
    else:
        l = l2
    if l < 0:
        l = l * -1
    return np.random.exponential(1/l)

def det_s_time(c : float = 1) -> float:
    return float(c)

def exp_s_time(mean : float) -> float:
    return np.random.exponential(1/mean)

def generate_service_time(priority : str, cat : str, params = dict) -> float:
    if priority=='HP':
        if cat=="hyperexp":
            service_time = hyperexp_s_time(mean = params.get("mean_hp"), std = params.get("std_hp"))
        elif cat=="det":
            service_time = det_s_time(c = params.get("mean_hp"))
        elif cat=="exp":
            service_time = exp_s_time(mean = params.get("mean_hp"))
        else:
            raise Exception("Invalid category for service time selected.")
    elif priority=='LP':
        if cat=="hyperexp":
            service_time = hyperexp_s_time(mean = params.get("mean_lp"), std = params.get("std_lp"))
        elif cat=="det":
            service_time = det_s_time(c = params.get("mean_lp"))
        elif cat=="exp":
            service_time = exp_s_time(mean = params.get("mean_lp"))
        else:
            raise Exception("Invalid category for service time selected.")
    else:
        raise Exception("Invalid priority for customer selected.")

    return service_time

def arrival(limit:int, customers : int, time : float, queue : List[Customer], FES : List[Tuple[int, str, str]], s_time_flag : str, params : Dict[str, float], logger : Logger, llp : float, lhp : float, server : Server) -> int:
    priority = np.random.choice(["HP", "LP"], 1)[0]
    inter_arrival = generate_arrival_time(priority=priority, lhp=lhp, llp = llp)
    if len(queue) <= limit:
        FES.append((time+inter_arrival, "arrival", priority))
        customers = customers + 1
        customer = Customer(type="arrival", arrival_time=time, priority=priority, server=server)
        queue.append(customer)
        logger.log_arrival(time+inter_arrival, customers)
    if customers == 1:
        customer.server = server
        server.customer = customer
        server.status = "busy"
        service_time = generate_service_time(priority=priority, cat=s_time_flag, params=params)
        FES.append((time+service_time, "departure", priority))
    return customers

def departure(customers : int, time : float, queue : List[Customer], FES : List[Tuple[int, str, str]], logger : Logger, s_time_flag : str, params : Dict[str, float]) -> int:
    customer = queue.pop(0)
    server = customer.server
    if server is not None:
        server.status = "idle"
    customers = customers - 1
    if customers > 0:
        service_time = generate_service_time(priority=customer.priority, cat=s_time_flag, params=params)
        FES.append((time+service_time, "departure", customer.priority))
        logger.log_departure(time+service_time, customers)
    return customers, customer.arrival_time

def cumulative_delays(delays : List[float]) -> List[float]:
    delays = np.array(delays)
    cs = np.cumsum(delays, axis=0)
    for idx in range(cs.shape[0]):
        if idx == 0:
            continue
        cs[idx] = cs[idx]/(idx+1)
    return list(cs)

def plot_results(delays : List[float], filepath : str, filename : str, title : str, xlabel : str, ylabel : str, savefig_bool : bool) -> None:
    fig, ax = plt.subplots(figsize=(5,5))
    ax.plot(delays)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid()
    if savefig_bool:
        fig.savefig(os.path.join(filepath, filename))
    plt.close()
if __name__ == '__main__':

    MAX_QUEUE_LENGTH = 1000

    LAMBDAS = [0.2, 0.4, 0.8, 1.4, 2.0, 2.4, 2.8]

    MEANS_HP = [1.0, .5]
    MEANS_LP = [1.0, 1.5]
    STDS_HP = [10*m for m in MEANS_HP]
    STDS_LP = [10*m for m in MEANS_LP]

    SERVICE_TIMES_CAT = ["det", "exp", "hyperexp"]

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--num-servers",
        type=int,
        default=2,
        help="Number of servers to instantiate at the beginning of the simulator."
        )
    parser.add_argument(
        "--plot-path",
        type=str,
        default="results/",
        help="Default folder into which plots should be saved."
        )
    parser.add_argument(
        "--results-path",
        type=str,
        default="results/",
        help="Directory into which saving the requested plots."
    )

    args = parser.parse_args()

    #main event loop
    for lambda_arrival in LAMBDAS:
        print(f"Using arrival parameter lambda = {lambda_arrival}")
        for s_time_cat in SERVICE_TIMES_CAT:
            print(f"Working with service time generated through: {s_time_cat}")
            for mean_hp, mean_lp, std_hp, std_lp in zip(MEANS_HP, MEANS_LP, STDS_HP, STDS_LP):
                delays_lp = list()
                delays_hp = list()
                params = {
                    "mean_hp": mean_hp,
                    "mean_lp":mean_lp,
                    "std_hp": std_hp,
                    "std_lp": std_lp,
                }
                print(f"Current parameters: {params}")

                customers = 0
                current_time = 0
                queue = list()
                FES = list()
                servers = boot_servers(k = args.num_servers)
                FES.append((0, "arrival", np.random.choice(["LP", "HP"], 1)[0]))
                queue.append(Customer(type="arrival", arrival_time=0, priority="LP", server=np.random.choice(servers, 1)[0]))
                myLogger = Logger()
                while(current_time < SIMULATION_TIME):
                    if len(queue) > 0:

                        FES = sorted(FES, key=lambda x : x[2])
                        time, event_type, priority = FES.pop(0)
                        current_time = time

                        if event_type == "arrival" and priority == "LP":

                            for server_idx in range(args.num_servers):
                                if servers[server_idx].status == 'idle':
                                    customers = arrival(limit=MAX_QUEUE_LENGTH, customers=customers, time=current_time, queue=queue, FES=FES, s_time_flag=s_time_cat, params=params, logger=myLogger, lhp=lambda_arrival, llp=lambda_arrival, server=servers[server_idx])
                                    break
                        elif event_type == "arrival" and priority == "HP":

                            for server_idx in range(args.num_servers):
                                # controllo se uno è libero co ha LP dentro
                                if servers[server_idx].status == "idle":
                                    # ready to accept customer
                                    customers = arrival(limit=MAX_QUEUE_LENGTH, customers=customers, time=current_time, queue=queue, FES=FES, s_time_flag=s_time_cat, params=params, logger=myLogger, lhp=lambda_arrival, llp=lambda_arrival, server=servers[server_idx])
                                    break
                                # se tutti occupati, allora ne scelgo uno a caso e rimetto il LP in cima alla FES
                                elif servers[server_idx].status == "busy" and servers[server_idx].customer.priority=="LP":
                                    server = servers[np.random.choice([k for k in range(args.num_servers)], 1)[0]]
                                    customers = arrival(limit=MAX_QUEUE_LENGTH, customers=customers, time=current_time, queue=queue, FES=FES, s_time_flag=s_time_cat, params=params, logger=myLogger, lhp=lambda_arrival, llp=lambda_arrival, server=servers[server_idx])
                                    FES.insert(0, (current_time, "arrival", "LP"))
                                    break
                                # se arriva HP e tutti i server sono occupati con HP, allora semplicemente tratto tutto come LP
                                elif servers[server_idx].status == "busy" and servers[server_idx].customer.priority=="HP":
                                    customers = arrival(limit=MAX_QUEUE_LENGTH, customers=customers, time=current_time, queue=queue, FES=FES, s_time_flag=s_time_cat, params=params, logger=myLogger, lhp=lambda_arrival, llp=lambda_arrival, server=servers[server_idx])
                                    break
                        elif event_type == "departure":
                            customers, leave_time = departure(
                                customers=customers,
                                time=current_time,
                                queue=queue,
                                FES=FES,
                                logger=myLogger,
                                s_time_flag=s_time_cat,
                                params=params
                                    )
                            if priority == "HP":
                                delays_hp.append(current_time-leave_time)
                            elif priority == "LP":
                                delays_lp.append(current_time-leave_time)
                    else:
                        print("Queue is empty. Terminating.")
                        break
                plot_results(
                    delays = cumulative_delays(delays_hp),
                    filepath=args.results_path,
                    filename=f"{lambda_arrival}_{s_time_cat}_delays.png",
                    title=f"{lambda_arrival}_{s_time_cat}_delays",
                    xlabel="Customers",
                    ylabel="Delay",
                    savefig_bool=True
                )

                plot_results(
                    delays = cumulative_delays(delays_lp),
                    filepath=args.results_path,
                    filename=f"{lambda_arrival}_{s_time_cat}_delays.png",
                    title=f"{lambda_arrival}_{s_time_cat}_delays",
                    xlabel="Customers",
                    ylabel="Delay",
                    savefig_bool=True
                )