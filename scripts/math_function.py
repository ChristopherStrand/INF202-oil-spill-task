"""
This file contains the mathmatical functions used in main.py
"""

import numpy as np
import numpy.typing as npt

x_star = np.array((0.35, 0.45))  # Intial start position

# Index 0 represents x value in the position vector x, and index 1 represents the y value in the position vector x


# Same as function u from task description. Should not return a vector
def oil_distro(t: float, x_n: npt.NDArray[np.float32]) -> np.float32:
    numerator = np.sum(((x_n-x_star)**2))
    denominator = -0.01
    return np.e**(numerator/denominator)


# Same as function v from task description. Should return a vector
def velocity(x_n: npt.NDArray[np.float32]) -> npt.NDArray[np.float32]:
    return (x_n[1] - 0.2 * [x_n[0]], -x_n[0])


# Same as X_mid from task description. Should return a vector
def midpoint(coordinates: npt.NDArray[np.float32]) -> npt.NDArray[np.float32]:
    return (1 / 3) * (coordinates[0] + coordinates[1] + coordinates[2])


# takes in two point(sharing with neighbour) and returns a numpy array/vector
def unit_normal_vector(point1, point2) -> npt.NDArray[np.float32]:
    vector = point2 - point1
    normal_vector = np.array([-vector[1], vector[0]])
    return normal_vector / np.linalg.norm(normal_vector)

# calculating the area of the cell
def calculate_area(points: list) -> float:
    x0, y0 = points[0]
    x1, y1 = points[1]
    x2, y2 = points[2]

    return 0.5 * abs((x0 - x2) * (y1 - y0) - (x0 - x1) * (y2 - y0))


def g(a, b, v, w):
    dot_product = np.dot(v, w)

    if dot_product > 0:
        return a * dot_product
    else:
        return b * dot_product


# calculating the change of oil in cell
def calculate_change(cell: object, neighbors: list[int]) -> int:
    # kan bli et problem å hente ut punktene, sjekke getter for celle og str metode for point
    area = calculate_area(cell.points)
    sum = 0
    for neighbour in cell.neighbors:
        mid_cell = midpoint(cell.points)
        mid_ngh = midpoint(neighbour.points)
        scaled_normal_vector = unit_normal_vector(""" points """)
        v_mid = (velocity(mid_cell) + velocity(mid_ngh)) / 2
        sum = sum + calculate_flux(
            cell.oil_amount, neighbour.oil_amount, scaled_normal_vector, v_mid
        )
    return sum


def calculate_flux(oil_amount, neighbours_oil_amount, v_mid, nv):
    return -dt / A * g(oil_amount, neighbours_oil_amount, v_mid, nv)
