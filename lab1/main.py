from queue import Queue
from client import Client
from server import Server
from clock import Clock

from numpy import random

SIMULATION_TIME = 1000000
STARTING_TIME = 0
CURRENT_TIME = 0

LAMBDA = .95
MU = 1.0

client_served = 0

server_idle = 'idle'
server_busy = 'busy'

def generate_arrival_time(current_time):
    return current_time + random.exponential(1/LAMBDA)

def generate_service_time():
    return random.exponential(1/MU)

if __name__ == "__main__":
    FES = list()
    myClock = Clock(CURRENT_TIME)
    myServer = Server(status=server_idle)
    myQueue = Queue(server=myServer, FES=FES)

    while myClock.current_time < 15:
        #genero un nuovo tempo di arrivo
        new_arrival_time = generate_arrival_time(myClock.current_time)
        #adding new client with specific arrival time to FES
        FES.append(Client(type="arrival", arrival_time=new_arrival_time))
        #sorting FES based on clients arrival time
        sorted_FES = sorted(FES, key=lambda x: x.arrival_time, reverse=True)
        myQueue.set_FES(sorted_FES)
        #Check if current_time == next service time in myQueue.FES and serve the client with random service time
        if(myClock.current_time == myQueue.get_FES()[0]):
            myServer.set_status(server_busy)
        myClock.set_current_time()