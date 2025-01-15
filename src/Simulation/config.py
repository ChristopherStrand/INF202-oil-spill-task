import toml
import argparse
import os


def parseInput():
    parser = argparse.ArgumentParser(
        description=" input config file name with -f or --file"
    )
    parser.add_argument(
        "-c", "--config", default="input.toml", type=str, help="input config file name"
    )
    parser.add_argument(
        "-f", "--file", type=str, help="folder including the config file"
    )
    parser.add_argument("--find-all", action="store_true", help="find all files")
    args = parser.parse_args()
    return args.file


def readConfig(name):
    with open("name", "r") as file:
        config = toml.load(file)
        geometry = config.get("geometry")
        fish_area = geometry.get("fish_area")
        start_point = geometry.get("initial_oil_area")
        filepath = geometry.get("filepath")

        settings = config.get("settings")
        steps = settings.get("nSteps")
        t_start = settings.get("t_start")
        t_end = settings.get("t_end")
        dt = (t_end - t_start) / steps

    if not os.path.exists(filepath):
        raise FileNotFoundError(f"The file {filepath} does not exist.")

    if not geometry:
        raise ValueError("Missing geometry section in config file.")

    if not settings:
        raise ValueError("Missing settings section in config file.")

    if not fish_area:
        raise ValueError("Missing fish_area in geometry section.")

    if not start_point:
        raise ValueError("Missing initial_oil_area in geometry section.")

    if not filepath:
        raise ValueError("Missing filepath in geometry section.")

    if not steps:
        raise ValueError("Missing nSteps in settings section.")

    if not t_start:
        raise ValueError("Missing t_start in settings section.")

    if not t_end and t_end > t_start:
        raise ValueError("Missing t_end in settings section.")

    return config
