from numpy import random
import time

SIMULATION_TIME = 100000
current_time = 0

server_idle = "idle"
server_busy = "busy"
busy_time = 0

LAMBDA = 1.0
MU = .95

customers_in_queue = 0
total_customers_served = 0

def generate_arrival_time(current_time):
    return round(current_time + random.exponential(1/LAMBDA))

def generate_service_time(current_time):
    return round(current_time + random.exponential(1/MU))

class customer():
    def __init__(self, arrival_time):
        self.arrival_time = arrival_time

    def get_arrival_time(self):
        return self.arrival_time

class Server():
    def __init__(self, status):
        self.status = status

class Queue():
    def __init__(self, FES):
        self.FES = FES
    
    def add_arrival(self, new_customer):
        self.FES.append(new_customer)
        self.FES = sorted(self.FES, key=lambda x : x.get_arrival_time())

    def sortFES(self):
        self.FES = sorted(self.FES, key=lambda x : x.get_arrival_time())

class Clock():
    def __init__(self):
        self.current_time = 0

    def set_current_time(self, increase=1):
        self.current_time = self.current_time + increase


def handle_arrival():
    pass

def handle_departure():
    pass

if __name__ == "__main__":

    FES = list()

    myClock = Clock()
    myServer = Server(server_idle)
    myQueue = Queue(FES)
    #Starting Event LOOP
    while myClock.current_time < SIMULATION_TIME:

        starttime = time.time()
        #ratg = random arrival time generator
        ratg = round(random.uniform(1, 5))

        #generate a random arrival time
        new_arrival_time = generate_arrival_time(myClock.current_time) #generate a new arrival_time every X seconds
        #insert the new customer inside the Queue's FES
        myQueue.add_arrival(customer(new_arrival_time))
        print(f"Customers in queue: {customers_in_queue} , server: {myServer.status}, total customers served: {total_customers_served}")

        customers_in_queue = customers_in_queue + 1

        time.sleep(ratg - ((time.time() - starttime) % ratg))

        #check if next arrival time in FES is time to schedule the event for service
        if(myClock.current_time == myQueue.FES[0].get_arrival_time() and myServer.status == "idle"):
                service_time = generate_service_time(myClock.current_time)
                myServer.status = server_busy
                customers_in_queue = customers_in_queue - 1
                total_customers_served = total_customers_served + 1
                busy_time = myClock.current_time + service_time
                print("Serving customer. Server:BUSY.")
        #make server IDLE if current_time + service_time = busy_time = new_current_time
        if(myClock.current_time == busy_time):
            myServer.status = server_idle
            print("Customer served. Server:IDLE.")
        #remove just served customer and move onto the next one
        myQueue.FES.pop(0)
        myQueue.sortFES()
        myClock.set_current_time()