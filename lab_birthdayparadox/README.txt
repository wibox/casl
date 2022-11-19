To run the code with default parameters just execute main.py. The simulator main variables:
- upper bound of the property (in this case the number of days in a year) -> --prop-upper-bound
- cardinalities to test (cardinality of the single class) -> --num-instances
- dataset containing the real distribution -> --real-data
can be changed via their respective flags (indicated by ->).
For example, to use a property upper bounded by 50, a different dataset and a different number of cardinalities:
python3 main.py --prop-upper-bound 50 --real-data <path/to/your/dataset> --num-instances <your cardinalities>