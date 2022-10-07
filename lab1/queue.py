class Queue():
    def __init__(self, server, FES):
        self.server = server
        self.FES = FES

    def set_FES(self, FES):
        self.FES = FES

    def get_FES(self):
        return self.FES

    