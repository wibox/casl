import os
import numpy as np

exp_width = list()
det_width = list()
hyperexp_width = list()

with open("width_log.csv", "r") as logfile:
    logs = logfile.readlines()
    for log in logs:
        current_width = log.split(",")[2]
        current_s_time = log.split(",")[1]
        if current_s_time == "det":
            det_width.append(float(current_width.strip()))
        elif current_s_time == "exp":
            exp_width.append(float(current_width))
        elif current_s_time == "hyperexp":
            hyperexp_width.append(float(current_width))

print(f"Exponential avg ci width: {np.mean(exp_width)}")
print(f"Deterministic avg ci width: {np.mean(det_width)}")
print(f"Hyperexponential avg ci width: {np.mean(hyperexp_width)} ")
