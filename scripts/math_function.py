"""
This file contains the mathmatical functions used in main.py
"""

import numpy as np
import numpy.typing as npt

#x_star = np.array((0.35, 0.45))  # Intial start position

def point_in_triangle(pt: npt.NDArray, tri_points: list) -> bool:
    """
    Returns True if point lies in cell

    Uses Barycentric coordinate system to determine if triangles with point and edges in triangle equal the full area (with small error constant epsilon)
    """

    A = calculate_area(tri_points)

    A1 = calculate_area([pt, tri_points[0], tri_points[1]])
    A2 = calculate_area([pt, tri_points[1], tri_points[2]])
    A3 = calculate_area([pt, tri_points[2], tri_points[0]])

    epsilon = 1e-10

    return abs(A - (A1 + A2 + A3)) < epsilon


def find_initial_cell(cells: list[object], start_point: npt.NDArray[np.float32]) -> int:
    """
    Finds the cell containing the start point, and returns the index of that cell.
    """
    for cell in cells:
        if point_in_triangle(start_point, cell.coordinates):
            return cell.index
    raise Exception(f"Point {start_point} was not found in the mesh")


def initial_oil_distribution(cells: list[object], start_point: npt.NDArray[np.float32]):
    """
    Gives intial distribution of oil around start point
    """
    for cell in cells:
        midpoint = midpoint(cell.points)
        u = np.e**(-np.sum((midpoint-start_point)** 2) / 0.01)
        cell._oil_amount = u


def velocity(cell_midpoint: npt.NDArray[np.float32]) -> npt.NDArray[np.float32]:
    """
    Finds the velocity of the oil in the midpoint of a cell. Returns a vector
    """
    return np.array([cell_midpoint[1] - 0.2 * cell_midpoint[0], -cell_midpoint[0]])


def midpoint(cell: object) -> npt.NDArray[np.float32]:
    """
    Same as X_mid from task description. Takes a cell of any shape and finds the midpoint
    """
    point_coordinates = cell.coordinates
    number_of_points = len(point_coordinates)
    
    sum_coordinates = np.array([0, 0])
    for coordinates in point_coordinates:
        sum_coordinates = sum_coordinates + coordinates
    return (1/number_of_points) * (sum_coordinates)


def unit_normal_vector(point1: npt.NDArray[np.float32], point2: npt.NDArray[np.float32]) -> npt.NDArray[np.float32]:
    """
    Finds the unit normal vector based on two points. The points must must be on the same facet
    """
    vector = point2 - point1
    normal_vector = np.array([-vector[1], vector[0]])
    return normal_vector / np.linalg.norm(normal_vector)


def calculate_area(coordinates: list[npt.NDArray[np.float32], npt.NDArray[np.float32], npt.NDArray[np.float32]]) -> float:
    """
    Calculates the area of triangle cells
    """
    if len(coordinates) != 3:
        raise Exception("Invalid cell, must be a triangle")
    x0, y0 = coordinates[0]
    x1, y1 = coordinates[1]
    x2, y2 = coordinates[2]

    return 0.5 * abs((x0 - x2) * (y1 - y0) - (x0 - x1) * (y2 - y0))


def g(a: float, b: float, v, w):
    """
    Required part of calculate_area
    """
    dot_product = np.dot(v, w)

    if dot_product > 0:
        return a * dot_product
    else:
        return b * dot_product


def calculate_change(mesh: object, cell_index: int, dt: float):
    """
    Calculates how much oil moves from a cell to it's neighbors
    """
    cell_object = mesh.cells[cell_index]
    area = calculate_area(cell_object.coordinates)
    neighbors = cell_object.neighbors
    total_flux = 0
    for neighbor in neighbors:
        mid_cell = midpoint(cell_object.points)
        mid_neighbor = midpoint(neighbor.points)
        scaled_normal_vector = unit_normal_vector(mid_cell, mid_neighbor)
        v_mid = (velocity(mid_cell) + velocity(mid_neighbor)) / 2
        flux = g(cell_object.oil_amount, neighbor.oil_amount, scaled_normal_vector, v_mid)
        total_flux += flux
    return -dt / area * total_flux


""" 
def calculate_flux(oil_amount, neighbours_oil_amount, v_mid, nv, A, dt):
    return -dt / A * g(oil_amount, neighbours_oil_amount, v_mid, nv) """
