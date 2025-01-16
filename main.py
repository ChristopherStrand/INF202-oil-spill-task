import src.Simulation.solver as solve
import numpy as np
import src.Simulation.mesh as msh
from src.Simulation.cells import *

if __name__ == "__main__":
    start_time = 0.0
    end_time = 1
    intervals = 100
    write_frequency = 5
    mesh_path = "./meshes/bay.msh"
    start_point = np.array([0.35, 0.45])

    factory = msh.CellFactory()
    #-------Register Cells----------
    factory.register(1, Vertex)
    factory.register(2, Line)
    factory.register(3, Triangle)
    #-------Register End------------
    
    solve.find_and_plot(mesh_path, start_time, end_time, intervals, write_frequency, start_point, factory)

