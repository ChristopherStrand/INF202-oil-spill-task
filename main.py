"""
Main script to simulate and visualize oil distribution using a custom mesh and solver.

This script initializes a mesh based on the provided configuration file, sets up the simulation environment, 
registers cell types for the mesh, and calls the solver to perform the simulation. The results are written 
and optionally visualized as images.

Key Steps:
1. Create an output directory (`images`) if it doesn't already exist.
2. Parse command-line arguments and load simulation settings from the configuration file.
3. Extract key parameters such as the number of steps, time range, mesh filepath, and initial conditions.
4. Register different cell types (Vertex, Line, Triangle) using a `CellFactory`.
5. Pass all configurations and the `CellFactory` to the solver to run the simulation and generate results.

Modules Used:
- `src.Simulation.solver`: Handles the core simulation logic.
- `src.Simulation.mesh`: Manages mesh and cell-related functionalities.
- `src.Simulation.cells`: Defines different cell types like Vertex, Line, and Triangle.
- `config`: Contains functions for reading and parsing configuration files.

Args:
    - `mesh_path` (str): Path to the mesh file.
    - `start_time` (float): Start time of the simulation.
    - `end_time` (float): End time of the simulation.
    - `intervals` (int): Number of time steps in the simulation.
    - `write_frequency` (int): Frequency at which results are written to disk.
    - `start_point` (list or array): Coordinates of the initial oil area.
    - `factory` (CellFactory): Factory for creating cell objects based on mesh data.

Output:
- Generates simulation images in the `images` directory.
- Executes the main function `find_and_plot` from the solver, which handles the core simulation and visualization tasks.
"""


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
