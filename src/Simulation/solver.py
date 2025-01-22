"""
Simulates and visualizes oil distribution over time in a mesh.

This function performs a simulation of oil flow in a mesh structure, calculating changes at each time step and 
plotting the state of the mesh at specified intervals. It supports handling different cell types, initializing 
oil distribution, and computing the oil flow between neighboring cells.

Args:
    mesh_path (str): Path to the mesh file used for the simulation.
    start_time (int): Starting time of the simulation.
    end_time (int): Ending time of the simulation.
    intervals (int): Number of simulation time steps.
    write_frequency (int): Frequency (in steps) at which the state of the mesh is plotted.
    start_point (npt.NDArray[np.float32]): Coordinates of the initial oil distribution area.
    cell_factory (msh.CellFactory): Factory for creating cell objects from the mesh data.

Key Steps:
1. Load the mesh and initialize cell objects using the provided `mesh_path` and `cell_factory`.
2. Compute the time step (`dt`) based on the simulation duration and number of intervals.
3. Initialize the oil distribution based on the `start_point`.
4. Perform the simulation:
   - At each time step, compute changes in oil distribution for triangular cells.
   - Update the oil amounts in cells based on computed changes.
5. Plot the mesh at intervals specified by `write_frequency`.
6. Generate a final plot at the end of the simulation.

Outputs:
- Generates plots of the mesh at specified time intervals and saves them as images.

Example:
    find_and_plot(
        mesh_path="path/to/mesh.msh",
        start_time=0,
        end_time=10,
        intervals=100,
        write_frequency=10,
        start_point=np.array([0.5, 0.5]),
        cell_factory=factory_instance
    )
"""

import numpy as np
import numpy.typing as npt
import time  # remove
import os
import src.Simulation.plotting as plot
import src.Simulation.mesh as msh
import src.Simulation.cells as cls
from .create_video import make_video


# Remove this func
def calculate_time(func):
    def inner1(*args, **kwargs):
        begin = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"Total time taken in : {func.__name__} {end - begin:.6f}")
        return result

    return inner1


@calculate_time  # Remove this deco
def find_and_plot(
    mesh_path: str,
    start_time: float,
    end_time: float,
    intervals: int,
    write_frequency: int,
    start_point: npt.NDArray[np.float64],
    cell_factory: msh.CellFactory,
    x_area: npt.NDArray[np.float64],
    y_area: npt.NDArray[np.float64],
    restartFile=None,
    toml_file=None,
    fast=None,
) -> dict[str, float]:
    """
    Plots and finds the change over the specified time
    """
    root_folder = "results"
    os.makedirs(root_folder, exist_ok=True)

    if toml_file:
        base_name = os.path.splitext(os.path.basename(toml_file))[0]
    else:
        base_name = "default_experiment"

    experiment_folder = os.path.join(root_folder, f"{base_name}_results")
    os.makedirs(experiment_folder, exist_ok=True)
    os.makedirs(os.path.join(experiment_folder, "input"), exist_ok=True)
    images_folder = os.path.join(experiment_folder, "images")
    os.makedirs(images_folder, exist_ok=True)

    mesh = msh.Mesh(mesh_path, cell_factory)
    cells = mesh.cells

    dt = round((end_time - start_time) / intervals, 6)
    print(f"dt is {dt}")

    # Calculates area, midpoint, neighbors etc
    print("Calculating...")
    for cell in cells:
        if not isinstance(cell, cls.Vertex) and not isinstance(cell, cls.Line):
            mesh.calculate(cell)

    # Runs if the simulation is suppose to start from a different time
    if restartFile:
        print("inside")
        with open(restartFile, "r") as file:
            print("inside2")
            lines = file.readlines()
            print("inside3")
            header = lines[0]
            for line in lines[1:]:
                index, oil_amount = line.split(";")
                cells[int(index)].oil_amount = float(oil_amount)
            print(f"Restarting from {header}")

    # Calculates change and plots
    current_time = start_time
    mesh.initial_oil_distribution(start_point)
    cells_in_area = set(mesh.cells_within_area(x_area, y_area))
    oil_area_time = {}
    for steps in range(intervals):
        if steps % write_frequency == 0:
            if fast:
                plot.plotting_mesh_cairo(cells, steps, cells_in_area, images_folder)
                print(f"fast: plotting number {steps}...")
            else:
                plot.plotting_mesh(cells, steps, cells_in_area, images_folder)
                print(f"plotting number {steps}...")

        for cell in cells:
            if not isinstance(cell, cls.Vertex) and not isinstance(cell, cls.Line):
                mesh.calculate_change(cell, dt)

        for cell in cells:
            if not isinstance(cell, cls.Vertex) and not isinstance(cell, cls.Line):
                cell.oil_amount += cell.oil_change
                cell.oil_change = 0

        current_time = round(current_time + dt, 4)

        oil_in_area = 0
        for cell in cells_in_area:
            oil_in_area += cell.oil_amount
        oil_area_time[current_time] = oil_in_area

    if fast:
        plot.plotting_mesh_cairo(cells, steps, cells_in_area, images_folder)
        print(f"fast: plotting number {steps}...")
    else:
        plot.plotting_mesh(cells, steps, cells_in_area, images_folder)
        print(f"plotting number {steps}...")

    if toml_file:
        base_name = os.path.splitext(os.path.basename(toml_file))[0]
        restart_filename = f"{base_name}_restartFile.csv"
    else:
        restart_filename = "restartFile.csv"

    # Stores the oil amount values such that the simulation can be started from a different time
    with open(os.path.join(experiment_folder, "input/", restart_filename), "w") as file:
        file.write(f"{end_time}\n")
        for cell in cells:
            file.write(f"{cell.index};{cell.oil_amount}\n")

    if write_frequency:
        make_video(f"{experiment_folder}/images", write_frequency, intervals)

    return oil_area_time
