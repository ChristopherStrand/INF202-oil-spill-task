import meshio
import classes
import numpy as np
import time
import math_function

mesh = classes.Mesh("../meshes/bay.msh")


def initial_oil_amount():
    for cell in mesh._cells:
        cell_midpoint = math_function.midpoint(cell.points)
        print(cell_midpoint)
        """ cell._oil_amount = initial_oil_distrobution(cell_midpoint)
        print(cell._oil_amount) """


def initial_oil_distrobution(midpoint, x=0.35, y=0.45):
    x_mid, y_mid = midpoint
    u = -((x_mid - x) ** 2 + (y_mid - y) ** 2) / 0.01
    return u


print(initial_oil_amount())
