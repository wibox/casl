This is a simulation about a pvp game organized in 2 teams.
#####
Run "run_simulation.sh" to start the simulation. The script handles everything, from parameters' combinations generation to generating graphs.
Alternatively, to simulate a game session, run the following scripts in the specified order:
1) config_manager.py -> sets all the possible combinations of the chosen parameters
2) execute.sh -> runs game sessions with objects initialized according to the current testing configuration of parameters. This could have been handled with PyGame scenes and session engine but time was too short to implement that.
3) warhol.py -> just generates graphs using log file output from execute.sh. Please consider that due to the strong time constraint these graphs are really bad since not enough simulations were provided to generated log files.
#####
To simulate a game session with default parameters just run main.py, it starts a game session with a 400x400 area, five players per team and no obstacles. 
#####
Please note that game speed has been held constant with value T=0.01 (i.e. a move is chosen for each player every T) and the player velocity is set fixed to 1 (i.e. each players moves just one block in each direction, randomly. Increasing player's velocity results in strange behaviours which couldn't be addressed in time; planning to do that if this specific lab continues evolving during the course.)

Hope you enjoy
Cheers
Francesco Pagano
