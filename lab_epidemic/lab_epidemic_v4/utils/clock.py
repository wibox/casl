class Clock:
    def __init__(self):
        self.starting_time = 0
        self.current_time = self.starting_time

    def _reset_clock(self) -> None:
        self.current_time = self.starting_time

    def tick(self, amount : float) -> float:
        self.current_time += amount
        return self.current_time