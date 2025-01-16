import src.Simulation.solver as solve
import numpy as np

if __name__ == "__main__":
    start_time = 0.0
    end_time = 1
    intervals = 100
    write_frequency = 5
    mesh_path = "./meshes/bay.msh"
    start_point = np.array([0.35, 0.45])

    solve.find_and_plot(mesh_path, start_time, end_time, intervals, write_frequency, start_point)

