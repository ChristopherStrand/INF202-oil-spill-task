# The Art of the Spill

**Ludvik Høibjerg Aslaksen**  
**Christopher Ljosland Strand**  
**Frederic Ljosland Strand**  

Project Task in INF202 at the University of Life Sciences  
January 2025

---

## Introduction

Simulations have become an essential tool for solving complex problems in physics, engineering, and chemistry, where traditional experiments are either too expensive or insufficient. For example, simulating airflow for different airplane designs is often more practical than building multiple prototypes. Computer simulations address these limitations by creating a virtual representation of the physical system, such as the laws of aerodynamics. This allows researchers to accurately predict real-world outcomes.

This project focuses on a fictional scenario involving an oil spill in “Bay City,” a coastal town concerned about the potential impact of the spill on its fishing grounds. The simulation models the spread and movement of the oil over time, considering ocean currents. By using a computational mesh, the project predicts the oil spill’s movement and its environmental impact on the fishing grounds. These insights are crucial in determining whether drastic countermeasures are needed to protect the marine ecosystem.

---

## Main Idea
This simulation models the movement of an oil spill outside Bay City. Using a computational mesh and a dynamic velocity field, it predicts how oil spreads over time, helping to assess its impact on fishing areas and the environment. Results are visualized to aid decision-making.

---

## Folder Structure
- **meshes/**: Contains computational mesh files used for simulations.
- **src/**: Source code for the simulation, including:
  - `cells.py`: Handles cells, points, and oil distribution.
  - `mesh.py`: Reads mesh files and calculates geometric properties.
  - `solver.py`: Core simulation logic.
  - `plotting.py`: Generates visualizations using Cairo.
- **tests/**: Unit and integration tests to ensure functionality.
- **main.py**: Main entry point for running simulations.
- **config.py**: Handles configuration file parsing.
- **input.toml**: Example configuration file for the simulation setup.



---

## User Guide

This package offers the user a way to configure and run the oil spill simulation with customizable settings. The program uses a configuration file to control its behavior.

Below is an example configuration file:

```python
[settings]
nSteps = 100
t_start = 0.1
t_end = 1.0

[geometry]
filepath = "meshes/bay.msh"
fish_area = [[0.0, 0.45], [0.0, 0.2]]
initial_oil_area = [0.35, 0.45]

[IO]
logName = "logfile"
writeFrequency = 5
restartFile = "input/solution.txt"
```

Replace `example.toml` with the path to your custom configuration file.
To run the program, use the following command in the terminal
`python main.py -c example.toml`
