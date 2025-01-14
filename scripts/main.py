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

    for i in range(0,10):
        dt = i / 10
        timestep()
        plotting.plotting_mesh(cells, i)

def timestep():
    flux_per_cell = [0] * len(mesh.cells)
    for cell in mesh.cells:
        if cell.type == "triangle":
            total_flux = 0
            mesh.find_neighbors(cell.index)
            for ngh in cell.neighbors:
                change = math_function.calculate_change(mesh, cell, ngh, dt)
                total_flux += change

            flux_per_cell[cell.index] -= total_flux

    for i, flux in enumerate(flux_per_cell):
        if mesh.cells[i].type == "triangle":
            mesh.cells[i].oil_amount += flux

solve(cells, start_point)
print(mesh.cells[1500].oil_amount)

