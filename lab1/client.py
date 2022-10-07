class Client():
    def __init__(self, type, arrival_time):
        self.arrival_time = arrival_time
        self.type = type

    def set_type(self, type):
        self.type = type