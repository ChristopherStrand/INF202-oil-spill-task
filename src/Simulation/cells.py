"""
A module defining geometric for a 2D mesh, including Points, Cells, and specialized cell types.

This module provides classes to represent Points and Cells in a 2D mesh, including properties and methods for managing their geometry and interactions. 
It also includes specialized cell types such as Vertex, Line, and Triangle, which inherit from the base `Cell` class. Genrating objects is handled by the mesh.py module.

Typical usage example:

    print(triangle.index)
    print(triangle.coordinates)
    triangle.neighbors = [neighboring_cell1, neighboring_cell2]
"""


import numpy as np
import numpy.typing as npt
from typing import Self


class Point:
    def __init__(self, index: int, x: float, y: float) -> None:
        self._index = index
        self._coordinates = np.array([x, y])

    @property
    def index(self) -> int:
        return self._index

    @property
    def coordinates(self) -> npt.NDArray[np.float32]:
        return self._coordinates


class Cell:
    def __init__(self, index: int, points: npt.NDArray[np.float32], type: int) -> None:
        """
        Represents a single cell in a mesh, defined by an index and a list of points.

        A Cell holds properties such as midpoint, area, velocity,
        and oil distribution, and maintains references to its neighboring cells.
        """
        self._index = index
        self._points = points
        self._neighbors = []
        self._oil_amount = 0.0 
        self._oil_change = 0.0
        self._midpoint = np.float32([0, 0]) 
        self._area = 0.0 
        self._velocity = np.float32([0, 0]) 
        self._scaled_normal = []
        self._type = type

    @property
    def type(self) -> float:
        return self._type

    @property
    def coordinates(self) -> list[npt.NDArray[np.float32]]:
        return [point.coordinates for point in self._points]

    @property
    def oil_amount(self) -> float:
        return self._oil_amount

    @oil_amount.setter
    def oil_amount(self, value) -> None:
        self._oil_amount = value

    @property
    def oil_change(self) -> float:
        return self._oil_change

    @oil_change.setter
    def oil_change(self, value) -> None:
        self._oil_change = value

    @property
    def index(self) -> int:
        return self._index
    
    @property
    def midpoint(self) -> npt.NDArray[np.float32]:
        return self._midpoint
    
    @midpoint.setter
    def midpoint(self, mid_coordinates: npt.NDArray[np.float32]) -> None:
        self._midpoint = mid_coordinates
    
    @property
    def area(self) -> float:
        return self._area
    
    @area.setter
    def area(self, area_of_cell: float) -> None:
        self._area = area_of_cell
    
    @property
    def scaled_normal(self) -> npt.NDArray[np.float32]:
        return self._scaled_normal

    @scaled_normal.setter
    def scaled_normal(self, scaled_vector: npt.NDArray[np.float32]) -> None:
        self._scaled_normal = scaled_vector

    @property
    def velocity(self) -> npt.NDArray[np.float32]:
        return self._velocity
    
    @velocity.setter
    def velocity(self, velocity_vector: npt.NDArray[np.float32]) -> None:
        self._velocity = velocity_vector

    @property
    def points(self) -> list[Point]:
        return self._points

    @property
    def neighbors(self) -> list[Self]:
        return self._neighbors

    @neighbors.setter
    def neighbors(self, neighboring_cells: list[int]) -> None:
        self._neighbors = neighboring_cells

    def __str__(self):
        return f"""Current cell is {self._index}:
                  midpoint: {self._midpoint},
                  area: {self._area},
                  normal: {self._scaled_normal},
                  velocity: {self._velocity}
                  neighbors: {[ngh.index for ngh in self._neighbors]}
                  type: {self._type}
                    """

# ------------------------------cells end--------------------------------------


class Vertex(Cell):
    pass


class Line(Cell):
    pass


class Triangle(Cell):
    pass
