"""
This file contains the mathmatical functions used in main.py
"""

import numpy as np
import numpy.typing as npt

# x_star = np.array((0.35, 0.45))  # Intial start position


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
        midpoint_cell = midpoint(cell)
        u = np.exp(-np.sum((midpoint_cell - start_point) ** 2) / 0.01)
        cell._oil_amount = u


def checking_direction_normal_vector(point1, point2, midpoint):
    # check if the normal vector is pointing outwards
    mid_cor_vector = point1 - midpoint
    normal_vector = unit_normal_vector(point1, point2)
    angle = angle_between(mid_cor_vector, normal_vector)
    if angle > 90:
        return -normal_vector
    return normal_vector


def angle_between(v1: npt.NDArray[np.float32], v2: npt.NDArray[np.float32]) -> float:
    dot_product = np.dot(v1, v2)
    v1_norm = np.linalg.norm(v1)
    v2_norm = np.linalg.norm(v2)

    if v1_norm == 0 or v2_norm == 0:
        raise ValueError("Input vectors must have non-zero length.")
    cos_angle = dot_product / (v1_norm * v2_norm)
    angle = np.arccos(cos_angle)
    return angle


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
        mid_cell = midpoint(cell_object)
        mid_neighbor = midpoint(neighbor)
        scaled_normal_vector = checking_direction_normal_vector(mid_cell, mid_neighbor)
        v_mid = (velocity(mid_cell) + velocity(mid_neighbor)) / 2
        flux = g(
            cell_object.oil_amount, neighbor.oil_amount, scaled_normal_vector, v_mid
        )
        total_flux += flux
    return -dt / area * total_flux


""" 
def calculate_flux(oil_amount, neighbours_oil_amount, v_mid, nv, A, dt):
    return -dt / A * g(oil_amount, neighbours_oil_amount, v_mid, nv) """
