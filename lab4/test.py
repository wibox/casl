from scipy.stats import t
import math
print(t.interval(0.99,
8,
65,
math.sqrt(445/9)))