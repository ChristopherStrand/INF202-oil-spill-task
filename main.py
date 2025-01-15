from src.Simulation.solver import Solver

start_point = [0.35, 0.45]
filename = "meshes/bay.msh"

if __name__ == "__main__":
    s = Solver(filename, start_point)
    s.solve()