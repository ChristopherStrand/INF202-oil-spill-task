# The Art of the Spill

## Modeling the Movement of Oil Spills Outside Bay City

![mesh_plot2](mesh_plot2.png)

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

## Simulation Process

1. **Creating a Computational Mesh**  
   The domain is divided into a computational mesh consisting of small triangles and lines at the edges. This mesh is read from the file `bay.msh`. Each triangle is defined by its vertices and edges.

2. **Modeling Initial Distribution**  
   The oil concentration at time \( t=0 \) is modeled as a Gaussian function, centered around the point \(\mathbf{x}^\ast = (x^\ast, y^\ast) = (0.35, 0.45)\):

   $$
   u(t=0, \mathbf{x}) = \exp\!\Bigl(-\frac{\|\mathbf{x} - \mathbf{x}^\ast\|^2}{0.01}\Bigr).
   $$

   The oil’s movement is governed by the velocity field:

   $$
   \mathbf{v}(\mathbf{x}) = \begin{pmatrix}
       y - 0.2x \\
       -x
   \end{pmatrix}.
   $$

3. **Simulating Oil Movement**  
   Over time, the oil flows according to the velocity field. The simulation computes the flux of oil across each cell edge \( e\_\ell \) using the formula:

   $$
   F^{(n)}_i = -\frac{\Delta t}{A_i}\,g\bigl(u_i^n,\,u_{\text{ngh}}^n,\,\mathbf{\nu}_{i,\ell},\,\tfrac{1}{2}(\mathbf{v}_i + \mathbf{v}_{\text{ngh}})\bigr),
   $$

   where the flux function \( g \) is defined as:

   $$
   g(a, b, \mathbf{\nu}, \mathbf{v}) =
   \begin{cases}
       a \cdot \langle \mathbf{v}, \mathbf{\nu}\rangle & \text{if } \langle \mathbf{v}, \mathbf{\nu}\rangle > 0, \\
       b \cdot \langle \mathbf{v}, \mathbf{\nu}\rangle & \text{otherwise}.
   \end{cases}
   $$

4. **Direction of Flux**  
   To compute the flow direction of the oil across the edges of each triangular cell, we utilize the velocity field \(\mathbf{v}(\mathbf{x})\) and the outward-pointing normal vector \(\mathbf{n}_\ell\) associated with each edge \(e_\ell\) of the triangle. The normal vector is orthogonal to the edge and points outward from the cell, ensuring consistency in the flux computations.

   The flow direction is determined by calculating the dot product between the velocity vector at the midpoint of the edge, \(\mathbf{v}\), and the scaled normal vector, \(\mathbf{\nu}\_\ell\), given by:

   $$
   \mathbf{\nu}_\ell = \mathbf{n}_\ell \,\cdot\, \|e_\ell\|,
   $$

   where \(\|e*\ell\|\) is the length of the edge \(e*\ell\). The scaled normal accounts for both the magnitude and direction of the edge.

   The sign of the dot product \(\langle \mathbf{v}, \mathbf{\nu}\_\ell\rangle\) determines the flow direction:

   - If \(\langle \mathbf{v}, \mathbf{\nu}\_\ell\rangle > 0\), the flow is outward from the current cell, and the flux is computed based on the oil concentration within the cell.
   - If \(\langle \mathbf{v}, \mathbf{\nu}\_\ell\rangle \le 0\), the flow is inward to the current cell, and the flux depends on the oil concentration in the neighboring cell.

5. **Updating Oil Distribution**  
   The total oil concentration in a triangular cell \(i\) at the next time step \(t\_{n+1}\) is computed as:

   $$
   u_i^{n+1} = u_i^n + \sum_{\ell=1}^3 F^{(n)}_{\text{ngh}, i, \ell}.
   $$

6. **Visualizing Results**  
   The simulation generates plots at regular intervals (specified in the configuration file) to show the oil spill’s movement over time.

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
