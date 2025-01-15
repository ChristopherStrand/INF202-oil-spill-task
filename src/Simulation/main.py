import meshio
import classes
import numpy as np
import time
import math_function as mf
import plotting as plot

mesh = classes.Mesh("./meshes/bay.msh")
cells = mesh.cells

start_time = 0.0
end_time = 1
intervals = 100
write_frequency = 5
dt = (end_time-start_time)/intervals
start_point = np.array([0.35, 0.45])
print(f"dt is {dt}")


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
def mjau():
    #Finds all midpoints, areas, velocities,  and neighbors
    print("Calculating...")
    for cell in cells:
        if type(cell) == classes.Triangle:
            mesh.calculate(cell.index)

    current_time = start_time
    mf.initial_oil_distribution(cells, start_point)

    for steps in range(intervals):
        if steps % write_frequency == 0:
            plot.plotting_mesh(cells, current_time)
            print(f"plotting number {steps}...")
        for cell in cells:
            if type(cell) == classes.Triangle:
                mf.calculate_change(cell, dt)
                
        for cell in cells:
            if type(cell) == classes.Triangle:
                cell.oil_amount += cell.oil_change
                cell.oil_change = 0
        current_time = round(current_time+dt, 4)
    plot.plotting_mesh(cells, current_time)
    print(f"plotting number {intervals}...")
    
mjau()