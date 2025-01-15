from src.Simulation.mesh import Mesh
from src.Simulation import math_function
from src.Simulation.plotting import plotting_mesh

class Solver:
    def __init__(self, filename, start_point):
        self._mesh = Mesh(filename)
        self._cells = [cell for cell in self._mesh.cells if cell.type == "triangle"]
        self._dt = 0.01
        self._start_point = start_point

    def timestep(self):
        flux_per_cell = [0] * len(self._mesh.cells)
        for cell in self._mesh.cells:
            if cell.type == "triangle":
                total_flux = 0
                self._mesh.find_neighbors(cell.index)
                for ngh in cell.neighbors:
                    change = math_function.calculate_change(self._mesh, cell, ngh, self._dt)
                    total_flux += change

                flux_per_cell[cell.index] += total_flux

        for i, flux in enumerate(flux_per_cell):
            if self._mesh.cells[i].type == "triangle":
                self._mesh.cells[i].oil_amount += flux

    def solve(self):
        math_function.initial_oil_distribution(self._cells, self._start_point)

        for i in range(0, 100):
            self.timestep()
            if i % 5 == 0:
                plotting_mesh(self._cells, i)