import meshio
import classes
import numpy as np
import time
import math_function
import plotting

mesh = classes.Mesh("./meshes/bay.msh")
cells = mesh.cells
dt = 0.1
start_point = [0.35, 0.45]

def solve(cells, start_point):
    math_function.initial_oil_distribution(cells, start_point)
    initial_cell = math_function.find_initial_cell(cells, start_point)

    for i in range(1,20):
        dt = i / 10
        timestep()

def timestep():
    for cell in mesh.cells:
        cell_index = cell.index
        mesh.find_neighbors(cell_index)
        for ngh in cell.neighbors:
            math_function.calculate_change(mesh, cell_index, dt)

solve(cells, start_point)