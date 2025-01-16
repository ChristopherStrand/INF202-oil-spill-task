import logging
import os


def setup_logger(logname):
    os.makedirs("logs", exist_ok=True)

    logging.basicConfig(
        filename=f"logs/{logname}.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        filemode="w",
    )
    return logging.getLogger("SimulationLogger")
