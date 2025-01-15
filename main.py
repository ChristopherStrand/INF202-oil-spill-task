from src.Simulation.solver import Solver
from config import readConfig, parseInput
import os


if __name__ == "__main__":
    os.makedirs("images", exist_ok=True)
    args = parseInput()
    config = readConfig(args.config)
    geometry = config["geometry"]
    filename = geometry.get("filepath")
    start_point = geometry.get("initial_oil_area")
    s = Solver(filename, start_point)
    s.solve()
