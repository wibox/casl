from .hawkes_process import HawkesProcess

class HawkesProcessWithInterventions(HawkesProcess):
    def __init__(
        self,
        a : int
    ):

        self.a = a