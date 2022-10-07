from numpy import random

SIMULATION_TIME = 1000000
current_time = 0

SERVERS = 3

server_idle = "idle"
server_busy = "busy"

def generate_arrival_time(current_time):
    return current_time + random.exponential()

def generate_service_time(current_time):
    return current_time + random.exponential()

class Client():
    def __init__(self, arrival_time, type):
        self.arrival_time = arrival_time
        self.type = type

    def get_arrival_time(self):
        return self.arrival_time

class Server():
    def __init__(self, status):
        self.status = status

class Queue():
    def __init__(self, FES):
        self.FES = sorted(FES, key=lambda x: x.get_arrival_time(), reversed=True)
    
    def serve_next_client(self):
        pass


servers = [Server(server_idle) for i in range(SERVERS)]

if __name__ == "__main__":
    while current_time < SIMULATION_TIME:
        print("Ciao!")