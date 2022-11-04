def log_tot(bins, balls):
    for bin, ball in zip(bins, balls):
        print(f"{bin}\n{ball}")

def log(bins):
    result = [bin.num_balls for bin in bins]
    print(result)