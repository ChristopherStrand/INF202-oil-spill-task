import toml
import argparse


def parseInput():
    parser = argparse.ArgumentParser(
        description=" input config file name with -f or --file"
    )
    parser.add_argument("-f", "--file", type=str, help="input config file name")
    args = parser.parse_args()
    return args.file


def readConfig(name):
    with open("name", "r") as file:
        config = toml.load(file)
        geometry = config.get("geometry")
        fish_area = [geometry.get("fish_area")]
        start_point = geometry.get("initial_oil_area")

        settings = config.get("settings")
        steps = settings.get("nSteps")
        t_start = settings.get("t_start")
        t_end = settings.get("t_end")
        dt = (t_end - t_start) / steps
    return fish_area, start_point, steps, t_start, t_end, dt
