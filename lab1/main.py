from numpy import random

from clock_random_gen import SIMULATION_TIME

#paramenters
LAMBDA = 3
MU = 4
SIMULATION_TIME = 1000

server_busy = "busy"
server_idle = "idle"
client_arrival = "arrival"
client_departure = "departure"

client = 0

#main functions for generating random arrival and service times
def generate_arrival_time(current_time):
    return current_time + random.exponential(1/LAMBDA)

def generate_service_time():
    return random.exponential(1/MU)

#main classes of the system
class Queue():
    def __init__(self, FES, server):
        self.FES = FES
        self.server = server
        self.customers_in_queue = 0
        self.current_time = 0

    def add_arrival(self, client):
        self.FES = sorted(self.FES.append(client), key=lambda x : x.get_arrival_time())

    def set_departure(self):
        return self.FES.pop(0)

    def get_next_event(self):
        return self.FES[0]

    def change_server_status(self, status):
        self.server.status = status

    def set_time(self, increase=1):
        self.current_time = self.current_time + increase

class Server():
    def __init__(self, status):
        self.status = status

class Client():
    def __init__(self, arrival_time, type):
        self.arrival_time = arrival_time
        self.type = type

    def get_arrival_time(self):
        return self.arrival_time

    def set_type(self, type):
        self.type = type

class Logger():
    def __init__(self):
        pass

FES = list()
myServer = Server(server_idle)
myQueue = Queue(FES, myServer)

if __name__ == "__main__":
    #generate first event of type arrival
    # if(myQueue.server.status == server_idle):
    #     newClient = Client(generate_arrival_time(myQueue.current_time), "arrival")
    #     #schedule its service time making server busy
    #     service_time = generate_service_time(myQueue.current_time)
    #     myQueue.change_server_status(server_busy)
    #     myQueue.set_time(myQueue.current_time + service_time)
    #     myQueue.set_departure()
    #     newClient.set_type(client_departure)
    #main even loop
    while myQueue.current_time < SIMULATION_TIME:
        print(myQueue.current_time)
        service_time = generate_service_time()
        print(f"service time: {service_time}")
        myQueue.set_time(myQueue.current_time + service_time)