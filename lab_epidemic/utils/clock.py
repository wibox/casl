class Clock():
    """
    Clock class employed in keeping track of the Hawkes process time.
    """
    def __init__(
        self,
        starting_time : float = .0, # starting time of the clock, deafults to 0.0 seconds
    ):
        self.starting_time = starting_time # starting time
        self.current_time = self.starting_time # current time

    def _reset_clock(self) -> None:
        """
        Resets Clock's instance to self.starting time
        """
        self.starting_time = 0

    def increase_time_unit(self, time_step : float) -> float:
        """
        Increases Clock's instance current time by a specific amount
        """
        self.current_time += time_step
        return self.current_time