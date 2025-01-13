import meshio
import classes
import numpy as np
import time
import math_function
import plotting

mesh = classes.Mesh("../meshes/bay.msh")
cells = mesh.cells
dt = 0.1
start_point = [0.35, 0.45]

math_function.initial_oil_distribution(cells, start_point)
initial_cell = math_function.find_initial_cell(cells, start_point)

# prints to check if reading and checking neighbors works
print(initial_cell)
print(mesh.find_neighbors(initial_cell))

mesh.find_neighbors(4)
mesh.print_neighbors(4)


print(mesh.cells[initial_cell].oil_amount)
for i in range(1, 20):
    dt = i / 10
    math_function.calculate_change(mesh, initial_cell, dt)


""" plotting functions needs two arguments: cells and time step, this is for naming the plots images """
plotting.plotting_mesh(cells, 1)
