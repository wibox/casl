class Clock():
    def __init__(
        self,
        starting_time : float,
    ):
        self.starting_time = starting_time
        self.current_time = self.starting_time

    def _reset_clock(self) -> None:
        self.starting_time = 0

    def increase_time_unit(self, time_step : float) -> float:
        self.current_time += time_step
        return self.current_time