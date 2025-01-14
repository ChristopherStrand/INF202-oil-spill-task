import meshio
import classes
import numpy as np
import time
import math_function
import plotting

mesh = classes.Mesh("meshes/bay.msh")
cells = mesh.cells
dt = 0.1
start_point = [0.35, 0.45]


for cell in mesh.cells:
    mesh.calculate(cell.index)
math_function.initial_oil_distribution(cells, start_point)
initial_cell = math_function.find_initial_cell(cells, start_point)

print(mesh.cells[initial_cell].oil_amount)
for i in range(1, 20):
    dt = i / 10
    math_function.calculate_change(mesh, initial_cell, dt)
    """ print(mesh.cells[initial_cell].oil_amount) """

plotting.plotting_mesh(cells)

# finding starting cell
# find neighbors
# calculate_change

# if oil != 0 in neighbor
# find neighbors for each neighbor of original cell
# calculate change

# if oil != 0 in neighbor
# find neighbors for each neighbor of original cell
# calculate change


""" initialneighbors = mesh.find_neighbors(first_cell) """

""" math_function.calculate_change(5) """
