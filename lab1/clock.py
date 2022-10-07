class Clock():
    def __init__(self, current_time):
        self.current_time = current_time

    def get_current_time(self):
        return self.current_time()

    def set_current_time(self, time=1):
        self.current_time = self.current_time + time