import meshio
import classes
import numpy as np
import time
import math_function
import plotting

mesh = classes.Mesh("../meshes/bay.msh")

dt = 0.1

math_function.initial_oil_amount(mesh._cells)
plotting.plotting_mesh(mesh._cells)

# finding starting cell
# find neighbors
# calculate_change

# if oil != 0 in neighbor
# find neighbors for each neighbor of original cell
# calculate change

# if oil != 0 in neighbor
# find neighbors for each neighbor of original cell
# calculate change
initial_cell = math_function.find_initial_cell([0.35, 0.45], mesh._cells)
print(initial_cell)
print(mesh.find_neighbors(initial_cell))


""" initialneighbors = mesh.find_neighbors(first_cell) """

""" math_function.calculate_change(5) """
