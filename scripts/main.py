import meshio
import classes
import numpy as np
import time
import math_function

mesh = classes.Mesh("../meshes/bay.msh")

dt = 0.1

math_function.initial_oil_amount(mesh._cells)
# finding starting cell
# find neighbors
# calculate_change

# if oil != 0 in neighbor
# find neighbors for each neighbor of original cell
# calculate change

# if oil != 0 in neighbor
# find neighbors for each neighbor of original cell
# calculate change


initialneighbors = mesh.find_neighbors(first_cell)

math_function.calculate_change(5)
