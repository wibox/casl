import numpy as np
np.random.seed(299266)
import matplotlib.pyplot as plt
import time as t
import argparse
from scipy.stats import t
from typing import *
import os

parser = argparse.ArgumentParser()
parser.add_argument("--verbose", type=int, help="Verbosity level for default logger.\n 0: logs nothing 1: logs high level events 2: logs everything (including queues arrivals and departures)", default=1)
parser.add_argument("--starting-batches", type=int, help="Initial number of batches to perform batch means", default=10)
args = parser.parse_args()

SIMULATION_TIME = 100000

U = [0.1, 0.2, 0.4, 0.7, 0.8, 0.9, 0.95, 0.99]
S_TIME_FLAGS = ["det", "exp", "hyperexp"]

class Logger():
    """
    This class is a simple logger to visualize information during the simulator's execution.
    Mainly used to log arrivals and departures (highly not recommended).
    Suggest verbosity level: 1
    If self.verbosity == 0: logs nothing
    If self.verbosity == 1: logs high level events (change in parameters, saving graphs etc...)
    If self.verbosity == 2: logs everything
    """
    def __init__(self, verbosity : int = 0):
        self.verbosity = verbosity

    def log_departure(self, time : float, queue_length : int):
        if self.verbosity == 2:
            print(f"Departure at time: {time}. Current Queue length: {queue_length}.")

    def log_arrival(self, time : float, queue_length : int) -> None:
        if self.verbosity == 2:
            print(f"Arrival scheduled at time: {time}. Current Queue length: {queue_length}.")

    def general_log_message(self, msg : str):
        if self.verbosity == 1:
            print(msg)

class Customer():
    """
    This class is a wrapper for the customer to be appended in the queue.
    Properties:
        - Type: arrival/departure
        - Arrival time
    """
    def __init__(self, type : str, arrival_time : float):
        self.type = type
        self.arrival_time = arrival_time

def generate_arrival_time(arrival : float) -> float:
    """
    This function returns an exponential arrival time
    """
    return np.random.exponential(arrival)

def generate_service_time(l : float) -> float:
    """
    This function returns an exponential service time
    """
    return np.random.exponential(1/l)

def generate_exponential_service_time() -> float:
    """
    This function return an exponential service time according to the problem's specifications.
    """
    return generate_service_time(1)

def generate_deterministic_service_time() -> float:
    """
    This function returns a deterministic service time, always costant.
    """
    return 1

from scipy.optimize import fsolve
import math
import random as rd
def sim_exp_hyper(pmf:list, expects:list, n:int, whi_seed:int=123) -> list:
    """
    This function represents the mathematically accurate way of generating an instance of the
    Hyperexponential distribution. It is highly inefficient since it requires solving a non-linear
    equation to generate just one sample. It is NOT USED in the code; generate_hyperexponential_service_time() is used instead.
    """

    if len(pmf) != len(expects):
        raise ValueError("len(pmf) != len(expects).")
    elif sum([i < 0 for i in pmf]) > 0:
        raise ValueError(f"There are negative values in the probablity mass "
            f"function {pmf}.")

    def get_eq(u, x):
        eq = 1 - sum(pmf[i] * math.exp(- x / expects[i]) for i in range(len(pmf))) - u
        return eq

    rd.seed(whi_seed)
    us = [rd.random() for i in range(n)]
    xs = [fsolve(lambda x: get_eq(u, x), 0.1)[0] for u in us]
    return xs[0]

def generate_hyperexponential_service_time() -> float:
    """
    This function generate an hyperexponential time according the definition of the hyperexponential itself.
    Distribution's parameters found by solving the corresponding linear system for target mean and std.
    More on that in the report.
    """
    p = .5
    l1 = 1/6
    l2 = 1/8
    u = np.random.random()
    if u <= p:
        expec = l1
    else:
        expec = l2
    service = np.random.exponential(1/expec)
    return service

def arrival(customers : int, time : float, queue : List[Customer], FES : List[Tuple[int, str]], logger : Logger, service_time_flag : bool, u : float) -> int:
    """
    This function simulates an arrival in the queue with a specific arrival time
    related to the service time distribution.
    """
    if service_time_flag == "hyperexp":
        service_time = generate_hyperexponential_service_time()
        SERVICE = service_time
    elif service_time_flag == "det":
        service_time = generate_deterministic_service_time()
        SERVICE = service_time
    elif service_time_flag == "exp":
        service_time = generate_exponential_service_time()
        SERVICE=1
    else:
        service_time = generate_service_time()

    inter_arrival = generate_arrival_time(SERVICE/u)
    FES.append((time+inter_arrival, "arrival"))
    customers = customers + 1
    customer = Customer(type="arrival", arrival_time=time)
    queue.append(customer)
    logger.log_arrival(time+inter_arrival, customers)
    if customers == 1:

        if service_time_flag == "hyperexp":
            service_time = generate_hyperexponential_service_time()
        elif service_time_flag == "det":
            service_time = generate_deterministic_service_time()
        elif service_time_flag == "exp":
            service_time = generate_exponential_service_time()
        else:
            service_time = generate_service_time()

        FES.append((time+service_time, "departure"))
    return customers

def departure(customers : int, time : float, queue : List[Customer], FES : List[Tuple[int, str]], logger : Logger, service_time_flag : bool) -> Tuple[int, float]:
    """
    This function simulates a departure in the queue when a the corresponding customer has been served.
    """
    
    customer = queue.pop(0)
    customers = customers - 1
    if customers > 0:

        if service_time_flag == "hyperexp":
            service_time = generate_hyperexponential_service_time()
        elif service_time_flag == "det":
            service_time = generate_deterministic_service_time()
        elif service_time_flag == "exp":
            service_time = generate_exponential_service_time()
        else:
            service_time = generate_service_time()

        FES.append((time+service_time, "departure"))
        logger.log_departure(time+service_time, customers)
    return customers, time-customer.arrival_time

def delay_cum_mean(delays : List[float]) -> List[float]:
    """
    This function perform the cumulative mean and then normalized the delays array when transient is yet to be removed.
    """
    cumsum = np.cumsum(delays, axis=0)
    for i in range(cumsum.shape[0]):
        if i == 0:
            continue
        cumsum[i] = cumsum[i]/(i+1)
    return list(cumsum)

def plot_results(logger : Logger, u : float, service_time_flag : str, delays : List[float], x_for_transient : int, filepath : str, filename : str, show_flag : bool, save_pict_flag : bool, title : str, label : str, xlabel : str, ylabel : str) -> None:
    """
    Simpe visualization function for transient identification.
    """
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.plot(delays, label=label)
    ax.set_xlabel(xlabel=xlabel)
    ax.set_ylabel(ylabel=ylabel)
    plt.axvline(x_for_transient, c="r")
    ax.set_title(title)
    ax.legend()
    ax.grid()
    if show_flag:
        plt.show()
    if save_pict_flag and logger:
        logger.general_log_message(msg=f"Saving picture generated with u={u} and service_time={service_time_flag}")
        plt.savefig(os.path.join(filepath, filename))
    plt.close()
     
def plot_batch_means(logger : Logger, u : float, service_time_flag : str, delays_means : List[float], delay_ci_lower : List[float], delay_ci_upper : List[float], filepath : str, filename : str, show_flag : bool, save_pict_flag : bool, title : str, label : str, xlabel : str, ylabel : str) -> None:
    """
    Visualization function for batched delays with corresponding Utilization value and service time distribution.
    """
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.plot(delays_means, label=label)
    ax.set_xlabel(xlabel=xlabel)
    ax.set_ylabel(ylabel=ylabel)
    ax.fill_between([x for x in range(len(delays_means))], delay_ci_lower, delay_ci_upper, alpha=.5)
    ax.set_title(title)
    ax.legend()
    ax.grid()
    if show_flag:
        plt.show()
    if save_pict_flag and logger:
        logger.general_log_message(msg=f"Saving picture generated with u={u} and service_time={service_time_flag}")
        plt.savefig(os.path.join(filepath, filename))
    plt.close()

def plot_delay_u(delays : List[float], label : List[str] , u : List[float], xlabel : str, ylabel : str, title : str, save_pic_flag : bool, show_flag : bool, filepath : str, filename : str) -> None:

    fig, ax = plt.subplots(figsize=(5, 5))
    ax.plot(u, delays, label=label)
    ax.set_xlabel(xlabel=xlabel)
    ax.set_ylabel(ylabel=ylabel)
    ax.set_title(title)
    if save_pic_flag:
        fig.savefig(os.path.join(filepath, filename))
    if show_flag:
        fig.show()

def remove_transient(s_time_flag : str, delays : List[float], u : float) -> Tuple[List[float], int]:
    """
    This function performs transient removal according to min/max normalization.
    Once indentified, transient is divided into windows
    """
    len_window = int(u*1000)
    n_window = int(len(delays)/len_window)
    # following threshold values discovered experimentally
    if s_time_flag=='det' or s_time_flag=='exp':
        thr = 0.98
    else:
        thr = 0.9
    for i in range(n_window):
        if i*len_window >= len(delays):
            # outreached
            break
        else:
            window = delays[i*len_window:(i+1)*len_window]
            if window != []:
                min1,max1 = min(window),max(window)
                normalized = min1/max1
            if normalized>thr:
                # going in the next window
                delays = delays[(i+1)*len_window:]
                print(f'Transient stop at: {len_window*(i+1)}')
                break
    return delays,len_window*(i+1)

def find_number_of_batches(s_time_flag : str, delays : List[float], u : float, n : int, confidence : float =.95, logger : Logger = None) -> Tuple[int, float]:
    """
    This function finds the optimal number of batches for the delays array once transient has been removed.
    """
    
    delays = np.array(delays)
    if s_time_flag == 'exp' or 'hyperexp':
        thr = 0.045
    elif s_time_flag == 'det':
        thr = 0.03
    else:
        thr = 0.04
    while True:
        batches = np.array_split(delays, n)
        for batch in batches:
            x = np.mean(batch)
            ci = t.interval(confidence, len(batches)-1, x, np.std(batch))
            z = ci[1] - x
            width = 2*z/x
            if width > thr:
                n += 1
                break
            else:
                if logger:
                    logger.general_log_message(msg=f"Found correct number of batches: {n}")
                return n, width

def perform_batch_means(delays : List[float], correct_n : int, confidence : float=.95, logger : Logger = None) -> Tuple[List[float], List[float], List[float]]:
    """
    This function performs batch means over the delays array (without transient).
    Returns a tuple containing the batch means, upper and lower bounds of the confidence intervals.
    """
    
    means = list()
    ci_lower = list()
    ci_upper = list()
    delays = np.array(delays)
    batches = np.array_split(delays, correct_n)
    if logger:
        logger.general_log_message(msg="Performing batch means...")
    for batch in batches:
        x = np.mean(batch)
        ci = t.interval(confidence, len(batches)-1, x, np.std(batch))
        ci_lower.append(ci[0])
        ci_upper.append(ci[1])
        means.append(x)
    if logger:
        logger.general_log_message(msg=f"ci_upper:{ci_upper}\nci_lower:{ci_lower}\nmeans:{means}")
    
    return means, ci_lower, ci_upper

def log_p_header(header : str, filepath : str, filename : str) -> None:
    """
    Write heads into logs/width_log.csv
    """
    with open(os.path.join(filepath, filename), "w") as logfile:
        logfile.write(header)

def log_p(u : float, s_time_flag : str, width : float, filepath : str, filename : str) -> None:
    """
    Logs current utilization, service time distribution, CI width into logs/width_log.csv
    """
    with open(os.path.join(filepath, filename), "a") as logfile:
        logfile.write(f"{u},{s_time_flag},{width}\n")

if __name__ == '__main__':
    #main event loop
    myLogger = Logger(verbosity=args.verbose)
    log_p_header(header="utilization,service_time_distribution,ci_width\n", filepath="logs/", filename="width_log.csv")
    delay_det_transient = list()
    det_transient_upper = list()
    det_transient_lower = list()

    delay_exp_transient = list()
    exp_transient_upper = list()
    exp_transient_lower = list()

    delay_hyperexp_transient = list()
    hyperexp_transient_upper = list()
    hyperexp_transient_lower = list()

    delay_det_notransient = list()
    det_notransient_upper = list()
    det_notransient_lower = list()

    delay_exp_notransient = list()
    exp_notransient_upper = list()
    exp_notransient_lower = list()

    delay_hyperexp_notransient = list()
    hyperexp_notransient_upper = list()
    hyperexp_notransient_lower = list()

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
            delaymean = delay_cum_mean(delays=delays)
            delay_wo_transient, transient_index = remove_transient(s_time_flag, delaymean, u)
            plot_results(
                logger=myLogger,
                u=u,
                service_time_flag=s_time_flag,
                delays=delaymean,
                x_for_transient=transient_index,
                filepath="results/",
                filename=f"{u}_{s_time_flag}.png",
                show_flag=False,
                save_pict_flag=True,
                title=f"Identify transient for: ({u}, {s_time_flag})",
                label=f"{s_time_flag}",
                xlabel="Steps",
                ylabel="Delays"
            )

            correct_num_batches, width = find_number_of_batches(s_time_flag=s_time_flag, logger=myLogger, delays=delay_wo_transient, u=u, n=10)
            log_p(u=u, width=width, s_time_flag=s_time_flag, filepath="logs/", filename="width_log.csv")
            means, ci_lower, ci_upper = perform_batch_means(logger=myLogger, delays=delay_wo_transient, correct_n=correct_num_batches)
            plot_batch_means(
                            logger=myLogger,
                            u=u,
                            service_time_flag=s_time_flag,
                            delays_means=means,
                            delay_ci_lower=ci_lower,
                            delay_ci_upper=ci_upper,
                            filepath="batch_results/",
                            filename=f"{u}_{s_time_flag}.png",
                            show_flag=False,
                            save_pict_flag=True,
                            title=f"Batched : ({u}, {s_time_flag})",
                            label=f"{s_time_flag}",
                            xlabel="steps",
                            ylabel="Batched delays")
                
            if s_time_flag == 'exp':

                delay_exp_transient.append(np.mean(delays))
                transient_exp_ci = t.interval(0.95, len(delays)-1, np.mean(delays), np.std(delays))
                exp_transient_upper.append(transient_exp_ci[1])
                exp_transient_lower.append(transient_exp_ci[0])

                delay_exp_notransient.append(np.mean(delay_wo_transient))
                notransient_exp_ci = t.interval(0.95, len(delay_wo_transient)-1, np.mean(delay_wo_transient), np.std(delay_wo_transient))
                exp_notransient_upper.append(notransient_exp_ci[1])
                exp_notransient_lower.append(notransient_exp_ci[0])

            elif s_time_flag == 'hyperexp':

                delay_hyperexp_transient.append(np.mean(delays))
                transient_hyperexp_ci = t.interval(0.95, len(delays)-1, np.mean(delays), np.std(delays))
                hyperexp_transient_upper.append(transient_hyperexp_ci[1])
                hyperexp_transient_lower.append(transient_hyperexp_ci[0])

                delay_hyperexp_notransient.append(np.mean(delay_wo_transient))
                notransient_hyperexp_ci = t.interval(0.95, len(delay_wo_transient)-1, np.mean(delay_wo_transient), np.std(delay_wo_transient))
                hyperexp_notransient_upper.append(notransient_hyperexp_ci[1])
                hyperexp_notransient_lower.append(notransient_hyperexp_ci[0])

            elif s_time_flag == 'det':

                delay_det_transient.append(np.mean(delays))
                transient_det_ci = t.interval(0.95, len(delays)-1, np.mean(delays), np.std(delays))
                det_transient_upper.append(transient_det_ci[1])
                det_transient_lower.append(transient_det_ci[0])

                delay_det_notransient.append(np.mean(delay_wo_transient))
                notransient_det_ci = t.interval(0.95, len(delay_wo_transient)-1, np.mean(delay_wo_transient), np.std(delay_wo_transient))
                det_notransient_upper.append(notransient_det_ci[1])
                det_notransient_lower.append(notransient_det_ci[0])

            else:
                pass

    # plot average delay vs utilization per distribution (with transient)
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.plot(U, delay_exp_transient, label="exp")
    ax.plot(U, delay_det_transient, label="det")
    ax.plot(U, delay_hyperexp_transient, label="hyperexp")
    ax.fill_between(U, det_transient_lower, det_transient_upper, alpha=.5)
    ax.fill_between(U, exp_transient_lower, exp_transient_upper, alpha=.5)
    ax.fill_between(U, hyperexp_transient_lower, hyperexp_transient_upper, alpha=.5)
    ax.grid()
    ax.legend()
    ax.set_xlabel(xlabel="Utilisation")
    ax.set_ylabel(ylabel="Delay")
    ax.set_title("Delay vs Utilisation (with transient)")
    fig.savefig(os.path.join("final_results/", "delayvsu_transient.png"))
    plt.close()
    # plot average delay vs utilization per distribution (without transient)
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.plot(U, delay_exp_notransient, label="exp")
    ax.plot(U, delay_det_notransient, label="det")
    ax.plot(U, delay_hyperexp_notransient, label="hyperexp")
    ax.fill_between(U, det_notransient_lower, det_notransient_upper, alpha=.5)
    ax.fill_between(U, exp_notransient_lower, exp_notransient_upper, alpha=.5)
    ax.fill_between(U, hyperexp_notransient_lower, hyperexp_notransient_upper, alpha=.5)
    ax.grid()
    ax.legend()
    ax.set_xlabel(xlabel="Utilisation")
    ax.set_ylabel(ylabel="Delay")
    ax.set_title("Delay vs Utilisation (no transient)")
    fig.savefig(os.path.join("final_results/", "delayvsu_notransient.png"))
    plt.close()

