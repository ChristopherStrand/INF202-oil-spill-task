import meshio
import classes
import numpy as np
import time
import math_function
import plotting

mesh = classes.Mesh("./meshes/bay.msh")
cells = [cell for cell in mesh.cells if cell.type == "triangle"]
dt = 0.1
start_point = [0.35, 0.45]

def solve(cells, start_point):
    math_function.initial_oil_distribution(cells, start_point)
    initial_cell = math_function.find_initial_cell(cells, start_point)

    for i in range(0,2):
        dt = i / 10
        timestep()

def timestep():
    for cell in mesh.cells:
        if cell.type == "triangle":
            mesh.find_neighbors(cell.index)
            for ngh in cell.neighbors:
                change = math_function.calculate_change(mesh, cell, ngh, dt)
                cell.oil_amount -= change
                ngh.oil_amount += change

solve(cells, start_point)
print(mesh.cells[309].oil_amount)
