class Logger():
    def __init__(self, log_path):
        self.log_path=log_path
        self.log_files=["time_vs_area.txt", "time_vs_speed.txt", "time_vs_players.txt",
                        "winnerkills_vs_area.txt", "winner_kills_vs_speed.txt", "winnerkills_vs_players.txt",
                        "avgkills_vs_area.txt", "avg_kills_vs_speed.txt", "avgkills_vs_players.txt"]

    def write_header(self, header, filename):
        try:
            with open(f"{self.log_path}/{filename}", "w") as f:
                f.write(header)
        except:
            print(f"Error dealing with log file at {self.log_path}/{filename}")

    def log_time(self, filename, time, other):
        try:
            with open(f"{self.log_path}/{filename}", "a") as f:
                f.write(f"{time},{other}")
        except:
            print(f"Error dealing with time_log file at {self.log_path}/{filename}")

    def log_winner_kills(self, filename, kills, other):
        try:
            with open(f"{self.log_path}/{filename}", "a") as f:
                f.write(f"{kills},{other}")
        except:
            print(f"Error dealing with kills_log file at {self.log_path}/{filename}")

    def log_average(self, filename, avg, other):
        try:
            with open(f"{self.log_path}/{filename}", "a") as f:
                f.write(f"{avg},{other}")
        except:
            print(f"Error dealing with avg_log file at {self.log_path}/{filename}")