To run the simulator it is sufficient to run main.py with default parameters.
Other inputs parameters (simulation time, verbosity level and initial number of batches)
can be modified via their respective flags. For example, to run the simulator
with 15 starting batches, 10000 simulation time and a verbosity of 1 (suggested):
python3 main.py --verbose 1 --simulation-time 10000 --starting-batches 15.
The content of the logs/ folder is not supposed to be run again if the 
starting number of batches remains 10. 
