import numpy as np
import matplotlib.pyplot as plt

from scipy.stats import t
from typing import *

import os

class Logger():
    def log_departure(self, time, queue_length):
        print(f"Departure at time: {time}. Current Queue length: {queue_length}.")

    def log_arrival(self, time, queue_length) -> None:
        print(f"Arrival scheduled at time: {time}. Current Queue length: {queue_length}.")

class Customer():
    def __init__(self, type, arrival_time):
        self.type = type
        self.arrival_time = arrival_time

def generate_arrival_time(arrival) -> float:
    return np.random.exponential(arrival)

def generate_service_time(l) -> float:
    return np.random.exponential(1/l)

def generate_exponential_service_time() -> float:
    return generate_service_time(1)

def generate_deterministic_service_time() -> float:
    return 1

def generate_hyperexponential_service_time() -> float:
    p = .5
    l1 = 1/6
    l2 = 1/8
    u1 = np.random.random()
    if u1 <= p:
        scale = l1
    else:
        scale = l2
    u2 = np.random.random()
    service = -np.log(u2)/scale
    return service

def arrival(customers, time, queue, FES, logger, service_time_flag, u=0.1) -> int:

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

def departure(customers, time, queue, FES, logger, service_time_flag) -> int:
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

def delay_mean(delays):
    cumsum = np.cumsum(delays, axis=0)
    for i in range(cumsum.shape[0]):
        if i == 0:
            continue
        cumsum[i] = cumsum[i]/(i+1)
    return list(cumsum)

def plot_results(delays, x_for_transient, filepath, filename, show_flag, save_pict_flag, title, label):
    
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.plot(delays, label=label)
    plt.axvline(x_for_transient, c="r")
    ax.set_title(title)
    ax.legend()
    ax.grid()
    if show_flag:
        plt.show()
    if save_pict_flag:
        plt.savefig(os.path.join(filepath, filename))
     
def plot_batch_means(delays_means, delay_ci_lower, delay_ci_upper, filepath, filename, show_flag, save_pict_flag, title, label):
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.plot(delays_means, label=label)
    ax.fill_between([x for x in range(len(delays_means))], delay_ci_lower, delay_ci_upper, alpha=.5)
    ax.set_title(title)
    ax.legend()
    ax.grid()
    if show_flag:
        plt.show()
    if save_pict_flag:
        plt.savefig(os.path.join(filepath, filename))

def remove_transient(arr, u):
    len_window = int(u*1000)
    n_window = int(len(arr)/len_window)
    thr = 0.95 
    if u == 0.9 or u == 0.95:
        thr = 0.98
    elif u == 0.99:
        thr = 0.995
    for i in range(n_window):
        if i*len_window >= len(arr):
            break
        else:
            window = arr[i*len_window: (i+1)*len_window]
            if window != []:
                min1,max1 = min(window),max(window)
                normalized = min1/max1
            if normalized>thr:
                arr = arr[(i+1)*len_window:]
                print('found T at:', len_window*(i+1))
                break
    return arr,len_window*(i+1)

def batch_means_wrong(arr, u, n, confidence):
    confidence_intervals = list()
    means = list()
    arr = np.array(arr)
    batches = np.array_split(arr, len(arr)//n)
    i = 0
    while True:
        batch = batches[i]
        x = np.mean(batch)
        ci = t.interval(.95, len(batches)-1, x, np.std(batch))
        z = ci[1] - x
        if ((2*z)/x) > u:
            i = i+1
            arr = np.concatenate(batches[i:])
            batches = np.array_split(arr, len(arr)//n)
        else:
            cis = [x-z, x+z]
            means.append(x)
            confidence_intervals.append(cis)
            print(f"Stopping batch num {i} - Mean: {x} - Confidence interval: {cis}")
        return confidence_intervals, means

def find_number_of_batches(delays, u, n, confidence=.95):
    # delays è senza transient
    delays = np.array(delays)
    while True:
        batches = np.array_split(delays, n)
        for batch in batches:
            x = np.mean(batch)
            ci = t.interval(confidence, len(batches)-1, x, np.std(batch))
            z = ci[1] - x
            if (2*z/x) > u:
                n += 1
                break
            else: 
                return n

def perform_batch_means(delays, correct_n, confidence=.95):
    means = list()
    ci_lower = list()
    ci_upper = list()
    delays = np.array(delays)
    batches = np.array_split(delays, correct_n)
    for batch in batches:
        x = np.mean(batch)
        ci = t.interval(confidence, len(batches)-1, x, np.std(batch))
        ci_lower.append(ci[0])
        ci_upper.append(ci[1])
        means.append(x)
    
    return means, ci_lower, ci_upper
    
