import numpy as np
import time  # remove
import src.Simulation.math_function as mf
import src.Simulation.plotting as plot
import src.Simulation.mesh as msh
import src.Simulation.cells as cls


def calculate_time(func):
    # added arguments inside the inner1,
    # if function takes any arguments,
    # can be added like this.
    def inner1(*args, **kwargs):

        # storing time before function execution
        begin = time.time()

        func(*args, **kwargs)

        # storing time after function execution
        end = time.time()
        print(f"Total time taken in : {func.__name__} {end - begin:.6f}")

    return inner1


@calculate_time
def find_and_plot(
    mesh_path: str,
    start_time: int,
    end_time: int,
    intervals: int,
    write_frequency: int,
    start_point,
) -> None:
    """
    Plots and finds the change over the specified time
    """
    mesh = msh.Mesh(mesh_path)
    cells = mesh.cells

    dt = (end_time - start_time) / intervals
    print(f"dt is {dt}")

    print("Calculating...")
    for cell in cells:
        if type(cell) == cls.Triangle:
            mesh.calculate(cell)

    current_time = start_time
    mf.initial_oil_distribution(cells, start_point)
    for steps in range(intervals):
        if steps % write_frequency == 0:
            plot.plotting_mesh(cells, current_time)
            print(f"plotting number {steps}...")
        for cell in cells:
            if type(cell) == cls.Triangle:
                mf.calculate_change(cell, dt)

        for cell in cells:
            if type(cell) == cls.Triangle:
                cell.oil_amount += cell.oil_change
                cell.oil_change = 0
        current_time = round(current_time + dt, 4)
    if write_frequency != -1000:
        plot.plotting_mesh(cells, current_time)
    print(f"plotting number {intervals}...")
