# Example configuration file
[settings]
nSteps = 500 # number of timesteps
tStart = 0.1 # start time
tEnd = 0.2 # end time

[geometry]
meshName = "meshes/bay.msh"
borders = [[0.0, 0.45], [0.0, 0.2]] # define where the fish are located

[IO]
logName = "log" # name for the log file created
restartFile = "input/solution.txt" # Restart file must be provided if start time is provided