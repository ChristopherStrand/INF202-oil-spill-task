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

# if oil != 0


math_function.calculate_change(cell)
