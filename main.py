import src.Simulation.solver as solve
import src.Simulation.mesh as msh
from src.Simulation.cells import *
from config import readConfig, parseInput
import os

if __name__ == "__main__":
    os.makedirs("images", exist_ok=True)
    args = parseInput()
    config = readConfig(args.config)
    setting = config["settings"]
    intervals = setting["nSteps"]
    start_time = setting["t_start"]
    end_time = setting["t_end"]
    geometry = config["geometry"]
    mesh_path = geometry.get("filepath")
    start_point = geometry.get("initial_oil_area")
    IO = config["IO"]
    write_frequency = IO.get("writeFrequency")

    factory = msh.CellFactory()
    #-------Register Cells----------
    factory.register(1, Vertex)
    factory.register(2, Line)
    factory.register(3, Triangle)
    #-------Register End------------

    solve.find_and_plot(
        mesh_path, 
        start_time, 
        end_time, 
        intervals, 
        write_frequency, 
        start_point,
        factory
    )
