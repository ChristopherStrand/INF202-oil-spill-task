import numpy as np
import numpy.typing as npt

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


def calculate_change(cell: object, dt: float):
    """
    Calculates how much oil moves from a cell to it's neighbors
    """
    flux = 0
    neighbors = cell.neighbors

    for index, neighbor in enumerate(neighbors):
        scaled_normal = cell.scaled_normal[index]
        v_mid = 0.5*(cell.velocity + neighbor.velocity)
        flux = flux + (-(dt / cell.area) * g(cell.oil_amount, neighbor.oil_amount, scaled_normal, v_mid))
    cell.oil_change += flux