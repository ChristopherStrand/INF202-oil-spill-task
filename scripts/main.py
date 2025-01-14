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
intervals = 10
dt = (end_time-start_time)/intervals
start_point = np.array([0.35, 0.45])


# def calculate_time(func):   
#     # added arguments inside the inner1,
#     # if function takes any arguments,
#     # can be added like this.
#     def inner1(*args, **kwargs):

#         # storing time before function execution
#         begin = time.time()
        
#         func(*args, **kwargs)

#         # storing time after function execution
#         end = time.time()
#         print(f"Total time taken in : {func.__name__} {end - begin:.6f}")
#     return inner1


#Finds all midpoints, areas, velocities,  and neighbors
print("Calculating...")
for cell in cells:
    mesh.calculate(cell.index)

current_time = start_time
mf.initial_oil_distribution(cells, start_point)
initial_cell = mf.find_initial_cell(cells, start_point)

for steps in range(intervals):
    plot.plotting_mesh(cells, steps)
    print(f"plotting number {steps}...")
    print(f"dt: {dt}")
    for cell in cells:
        mf.calculate_change(cell, current_time)
    for cell in cells:
        cell.oil_amount += cell.oil_change
        cell.oil_change = 0
    current_time += dt
    
