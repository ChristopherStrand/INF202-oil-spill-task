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


# remember to not update oil amount before updating or all cells

print(mesh.cells[initial_cell].oil_amount)
for i in range(1, 2):
    dt = i / 10
    new_oil_amount = math_function.calculate_change(mesh, initial_cell, dt)
    """ print(new_oil_amount) """
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
