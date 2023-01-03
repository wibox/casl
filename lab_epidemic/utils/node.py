class Node():
    def __init__(
        self,
        idx : int,
        infection_time : float,
        generation : int
    ):
        self.idx = idx
        self.infection_time = infection_time
        self.generation = generation

    def __str__(self) -> str:
        return f"Node: {self.idx}\nGeneration: {self.generation}\nInfection time: {self.infection_time}"

class AncestorNode(Node):
    def __init__(
        self,
        idx : int,
        infection_time : float
    ):
        super().__init__(
            idx=idx,
            infection_time=infection_time,
            generation=0
            )

    def __str__(self) -> str:
        return f"Ancestor:{self.idx}\n\tInfection time: {self.infection_time}"