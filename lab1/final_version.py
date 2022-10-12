import numpy as np

CURRENT_TIME = 0
SIMULATION_TIME = 1000

LAMBDA = 3
MU = 4

SERVER_IDLE = "idle"
SERVER_BUSY = "busy"

QUEUE_LENGTH = 0

def generate_arrival_time(current_time):
    return current_time + np.random.expovariate(1/MU)

def generate_service_time(current_time):
    return np.random.expovariate(1/LAMBDA)

class Logger():
    def __init__(self):
        pass

class Server():
    def __init__(self, status):
        self.status = status

class Customer():
    def __init__(self, arrival_time, type):
        self.arrival_time = arrival_time
        self.type = type

class Queue():
    def __init__(self, server, FES):
        self.server = server
        self.FES = FES

    def arrival(self, customer):
        self.FES.append(customer)
        self.FES = sorted(self.FES, key=lambda x : x.arrival_time, reversed=False)

    def departure(self):
        pass

if __name__ == "__main__":
    FES = list()
    myServer = Server(status=SERVER_IDLE)
    myQueue = Queue(server=myServer, FES=FES)
    new_customer = Customer(arrival_time = generate_arrival_time(CURRENT_TIME), type="arrival")
    while CURRENT_TIME < SIMULATION_TIME:
        if(myQueue.server.status==SERVER_IDLE):
            #gestisci arrivo e mettilo in servizio
            myQueue.server.status = SERVER_BUSY
            if(QUEUE_LENGTH != 0):
                QUEUE_LENGTH = QUEUE_LENGTH - 1
        elif(myQueue.server.status==SERVER_BUSY):
            #aumenta il numero di elementi nella FES e il numero di utenti in coda
            QUEUE_LENGTH = QUEUE_LENGTH + 1