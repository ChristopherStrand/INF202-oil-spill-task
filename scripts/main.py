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
dt = (end_time-start_time)/intervals
start_point = np.array([0.35, 0.45])
print(f"dt is {dt}")
#Finds all midpoints, areas, velocities,  and neighbors
print("Calculating...")
for cell in cells:
    mesh.calculate(cell.index)


current_time = start_time
mf.initial_oil_distribution(cells, start_point)

for steps in range(intervals):
    plot.plotting_mesh(cells, current_time)
    print(f"plotting number {steps}...")
    for cell in cells:
        mf.calculate_change(cell, current_time)
    for cell in cells:
        cell.oil_amount += cell.oil_change
        cell.oil_change = 0
    current_time = round(current_time+dt, 4)
plot.plotting_mesh(cells, current_time)
print(f"plotting number {intervals}...")
    
