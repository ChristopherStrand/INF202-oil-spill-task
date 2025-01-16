import src.Simulation.solver as solve
import numpy as np
from config import readConfig, parseInput
import os
from logger import setup_logger

if __name__ == "__main__":
    os.makedirs("images", exist_ok=True)

    args = parseInput()
    config = readConfig(args.config)
    setting = config["settings"]
    intervals = setting["nSteps"]
    start_time = setting["t_start"]
    end_time = setting["t_end"]
    geometry = config["geometry"]
    mesh_path = geometry["filepath"]
    start_point = geometry["initial_oil_area"]
    IO = config["IO"]
    write_frequency = IO["writeFrequency"]
    logName = IO["logName"]

    logger = setup_logger(logName)

    logger.info("Simulation started")
    logger.info(config)

    solve.find_and_plot(
        mesh_path, start_time, end_time, intervals, write_frequency, start_point
    )

    logger.info("Simulation Ended")
