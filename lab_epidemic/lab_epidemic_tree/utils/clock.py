class Clock:
    
    starting_time = 0
    current_time = 0

    def _reset_clock(self):
        self.current_time = self.starting_time

    def tick(self, amount):
        self.current_time += amount