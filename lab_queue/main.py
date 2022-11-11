import numpy as np

np.random.seed(123456789)

current_time = 0
SIMULATION_TIME = 100000

LAMBDA = 3
MU = 4

customers = 0

queue = list()
FES = list()

def generate_arrival_time():
    return np.random.exponential(1/MU)

def generate_service_time():
    return np.random.exponential(1/LAMBDA)

def arrival(time, queue, FES, logger):
    global customers
    inter_arrival = generate_arrival_time()
    FES.append((time+inter_arrival, "arrival"))
    customers = customers + 1
    customer = Customer(type="arrival", arrival_time=time)
    queue.append(customer)
    logger.log_arrival(time+inter_arrival, customers)
    service_time = generate_service_time()
    FES.append((time+service_time, "departure"))

def departure(time, queue, FES, logger):
    global customers
    customer = queue.pop(0)
    customers = customers - 1
    if customers > 0:
        service_time = generate_service_time()
        FES.append((time+service_time, "departure"))
        logger.log_departure(time+service_time, customers)

class Logger():
    def log_departure(self, time, queue_length):
        print(f"Departure at time: {time}. Current Queue length: {queue_length}.")

    def log_arrival(self, time, queue_length):
        print(f"Arrival scheduled at time: {time}. Current Queue length: {queue_length}.")

class Customer():
    def __init__(self, type, arrival_time):
        self.type = type
        self.arrival_time = arrival_time

if __name__ == '__main__':
    #main event loop
    FES.append((0, "arrival"))
    queue.append(Customer(type="arrival", arrival_time=0))
    myLogger = Logger()
    while(current_time < SIMULATION_TIME) or (not FES):
        time, event_type = FES.pop(0)
        current_time = time
        if len(queue) > 0:
            if event_type == "arrival":
                arrival(current_time, queue, FES, myLogger)
            elif event_type == "departure":
                departure(current_time, queue, FES, myLogger)
        else:
            print("Queue is empty. Terminating.")
            break
        FES = sorted(FES, key=lambda x : x[0])