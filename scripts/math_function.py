"""
This file contains the mathmatical functions used in main.py
"""

import numpy as np
import numpy.typing as npt
import classes as cls


def point_in_triangle(check_point: npt.NDArray[np.float32], cell: object) -> bool:
    """
    Returns True if point lies in cell

    Uses a Barycentric coordinate system to determine if a point is within the area of a cell (Epsilon is a small error constant)
    """
    def _calculate_area(coordinates: list[npt.NDArray[np.float32], npt.NDArray[np.float32], npt.NDArray[np.float32]]) -> float:
        """
        Calculates the area of triangle cells. Should only be used in point in triangle
        """
        x0, y0 = coordinates[0]
        x1, y1 = coordinates[1]
        x2, y2 = coordinates[2]

        return 0.5 * abs((x0 - x2) * (y1 - y0) - (x0 - x1) * (y2 - y0))

    assert len(cell.points) == 3, "Cell passed as argument in point_in_triangle() dosen't have 3 points "
    A = cell.area
    a, b, c = cell.coordinates #The coordinates in the cell who is being checked if it contains check_point

    A1 = _calculate_area([check_point, a, b])
    A2 = _calculate_area([check_point, b, c])
    A3 = _calculate_area([check_point, c, a])

    epsilon = 1e-10

    return abs(A - (A1 + A2 + A3)) < epsilon


def find_initial_cell(cells: object, start_point: npt.NDArray[np.float32]) -> int:
    """
    Finds the cell containing the start point, and returns the index of that cell.
    """
    for cell in cells:
        if point_in_triangle(start_point, cell):
            return cell.index
    raise Exception(f"Point {start_point} was not found in the mesh")


def initial_oil_distribution(cells: list[object], start_point: npt.NDArray[np.float32]):
    """
    Gives intial distribution of oil around start point
    """
    for cell in cells:
        u = np.exp(-np.sum((cell.midpoint - start_point) ** 2) / 0.01)
        cell.oil_amount = u


def g(a: float, b: float, v, w):
    """
    Required part of calculate_area
    """
    dot_product = np.dot(v, w)

    if dot_product > 0:
        return a * dot_product
    else:
        return b * dot_product


def calculate_change(cell: object, cell_index: int, dt: float):
    """
    Calculates how much oil moves from a cell to it's neighbors
    """
    cell_object = [cell_index]
    area = cell_object.area
    neighbors = cell_object.neighbors
    total_flux = 0
    for index, neighbor in enumerate(neighbors):
        normal_vector = cell_object.normal[index] 
        v_mid = (cell_object.velocity + neighbor.velocity) / 2
        flux = g(cell_object.oil_amount, neighbor.oil_amount, normal_vector, v_mid)
        total_flux += flux
    return -dt / area * total_flux