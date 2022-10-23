class Logger():
    def __init__(self, log_path="log"):
        self.log_path=log_path
        self.log_files=["time_vs_area.txt", "time_vs_speed.txt", "time_vs_players.txt",
                        "winnerkills_vs_area.txt", "winner_kills_vs_speed.txt", "winnerkills_vs_players.txt",
                        "avgkills_vs_area.txt", "avg_kills_vs_speed.txt", "avgkills_vs_players.txt"]
        # self.write_header("TIME,AREA\n", filename=self.log_files[0])
        # self.write_header("TIME,SPEED\n", filename=self.log_files[1])
        # self.write_header("TIME,NUM_PLAYERS\n", filename=self.log_files[2])
        # self.write_header("WINNERKILLS,AREA\n", filename=self.log_files[3])
        # self.write_header("WINNERKILLS,SPEED\n", filename=self.log_files[4])
        # self.write_header("WINNERKILLS,NUM_PLAYERS\n", filename=self.log_files[5])
        # self.write_header("AVGKILLS,AREA\n", filename=self.log_files[6])
        # self.write_header("AVGKILLS,SPEED\n", filename=self.log_files[7])
        # self.write_header("AVGKILLS,NUM_PLAYERS\n", filename=self.log_files[8])

    def write_header(self, header, filename):
        try:
            with open(f"../{self.log_path}/{filename}", "w") as f:
                f.write(header)
        except:
            print(f"Error dealing with log file at {self.log_path}/{filename}")

    def log_time(self, filename, time, other):
        try:
            with open(f"../{self.log_path}/{filename}", "a") as f:
                f.write(f"{time},{other}\n")
        except:
            print(f"Error dealing with time_log file at {self.log_path}/{filename}")

    def log_winner_kills(self, filename, kills, other):
        try:
            with open(f"../{self.log_path}/{filename}", "a") as f:
                f.write(f"{kills},{other}\n")
        except:
            print(f"Error dealing with kills_log file at {self.log_path}/{filename}")

    def log_average(self, filename, avg, other):
        try:
            with open(f"../{self.log_path}/{filename}", "a") as f:
                f.write(f"{avg},{other}\n")
        except:
            print(f"Error dealing with avg_log file at {self.log_path}/{filename}")