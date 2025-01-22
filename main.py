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
import src.Simulation.cells as cls
import numpy as np
from config import readConfig, parseInput, process_all_configs
import os
from logger import setup_logger

if __name__ == "__main__":

    args = parseInput()

    def run(toml_file=None, fast=0):
        config = readConfig(args.config)
        setting = config["settings"]
        intervals = setting["nSteps"]
        start_time = setting.get("t_start")
        end_time = setting["t_end"]
        geometry = config["geometry"]
        fish_area = geometry["fish_area"]
        mesh_path = geometry["filepath"]
        start_point = geometry["initial_oil_area"]
        IO = config["IO"]
        write_frequency = IO.get("writeFrequency")
        logName = IO.get("logName")
        restartFile = IO.get("restartFile")

        logger = setup_logger(logName)

        logger.info("Simulation started")
        logger.info(config)
        x_area = np.float64(fish_area[0])
        y_area = np.float64(fish_area[1])

        factory = msh.CellFactory()
        # -------Register Cells----------
        factory.register(1, cls.Vertex)
        factory.register(2, cls.Line)
        factory.register(3, cls.Triangle)
        # -------Register End------------

        oil_area_time = solve.find_and_plot(
            mesh_path,
            start_time,
            end_time,
            intervals,
            write_frequency,
            start_point,
            factory,
            x_area,
            y_area,
            restartFile,
            toml_file,
            fast,
        )

        logger.info("Oil distribution over time:")
        for time_step, oil_value in oil_area_time.items():
            logger.info(f"  Time step {time_step}: Oil amount {oil_value}")
        logger.info("Simulation Ended")

    if args.fast:
        fast = 1
    else:
        fast = 0

    if args.find_all and args.folder:
        toml_files = process_all_configs(args.folder)
        for toml_file in toml_files:
            run(toml_file, fast=fast)
    else:
        run(None, fast=fast)
