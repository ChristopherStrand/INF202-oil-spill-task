"""
A module for creating and simulating 2D meshes, including functionality for geometric calculations, oil distribution, and cell interaction.

This module defines a `Mesh` class to represent 2D meshes with cells and points, a `CellFactory` for creating various types of cells, 
and functions for simulation-related tasks such as calculating velocity, oil distribution, and neighbor relationships.

Typical usage example:

    from mesh import Mesh, CellFactory
    from src.Simulation.cells import Triangle, Line

    # Create a cell factory and register cell types
    factory = CellFactory()
    factory.register(3, Triangle)
    factory.register(2, Line)

    # Load a mesh file and initialize the mesh
    mesh = Mesh("example.msh", factory)

    # Access cells and points
    cells = mesh.cells
    points = mesh.points

    # Perform calculations on a specific cell
    mesh.calculate(cell)
    print(cell.midpoint)
"""

import meshio
import numpy as np
import numpy.typing as npt
import src.Simulation.cells as cls


class CellFactory:
    """
    A factory class for creating cell objects based on the number of points they contain.

    This class allows for the registration of different cell types, each corresponding
    to a specific number of points. Once registered, the factory can create instances
    of these cell types dynamically based on input data.
    """

    def __init__(self):
        self._cell_types = {}
        self._cell_index = -1  # Minus -1 such that the index starts at 0

    def register(self, amount_of_points: int, cell_class: object):
        """
        Registers a new cell type with the factory.
        """
        self._cell_types[amount_of_points] = cell_class

    def __call__(self, cell: list[int], points_list: list[cls.Point]):
        """
        Creates a cell object based on the input data.

        Args:
            cell (list[int]): A list of integers representing point indices in the mesh.
            index (int): The index of the cell being created in the mesh.
            points_list (list[cls.Point]): A list of Point objects representing the points
                                           in the mesh.

        Returns:
            object: An instance of the registered cell class for the given number of points.

        Raises:
            Exception: If the number of points in the cell does not match any registered type.
        """
        self._cell_index += 1
        key = len(cell)
        if key not in self._cell_types:
            raise Exception(f"Unkown cell type: {key}")
        points = [points_list[i] for i in cell]
        return self._cell_types[key](self._cell_index, points, key)


class Mesh:
    """
    Represents a computational mesh, containing points and cells, initialized from a mesh file.

    The Mesh class processes mesh files (e.g., `.msh`) to create point and cell objects and
    provides methods for performing calculations and simulations, such as determining neighbors,
    computing areas, calculating velocities, and simulating oil distribution and flow.

    Args:
        msh_file (str): Path to the mesh file to be read.
        cell_factory (CellFactory): Factory object for creating cell instances.

    Attributes:
        _cell_index (int): Tracks the current index of a cell in the mesh.
        _points (list[cls.Point]): List of Point objects representing points in a mesh.
        _cells (list[cls.Cell]): List of Cell objects representing cells in a mesh.
    """

    def __init__(self, msh_file: str, cell_factory: CellFactory) -> None:
        msh = meshio.read(msh_file)
        # Makes a list of points objects
        self._points = [
            cls.Point(index, points[0], points[1])
            for index, points in enumerate(msh.points)
        ]
        self._cells = []
        for cell_types in msh.cells:
            self._cells.extend(
                [cell_factory(cell, self._points) for cell in cell_types.data]
            )

    @property
    def cells(self) -> list[cls.Cell]:
        return self._cells

    @property
    def points(self) -> list[cls.Point]:
        return self._points

    def cells_within_area(
        self, x_area: npt.NDArray[np.float64], y_area: npt.NDArray[np.float64]
    ) -> list[cls.Cell]:
        """
        Finds and returns a list of cells that have at least one point within a specified rectangular area.

        Args:
            x_area (npt.NDArray[np.float32]): A 2-element array specifying the [min, max] range of the area along the x-axis.
            y_area (npt.NDArray[np.float32]): A 2-element array specifying the [min, max] range of the area along the y-axis.

        Returns:
            list[cls.Cell]: A list of cells that intersect with the specified area. A cell is included if at least one of its points lies within the area.
        """
        cells_within = []
        for cell in self._cells:
            for coordinates in cell.coordinates:
                if (coordinates[0] > x_area[0] and coordinates[0] < x_area[1]) and (
                    coordinates[1] > y_area[0] and coordinates[1] < y_area[1]
                ):
                    cells_within.append(cell)
                    break
        return cells_within

    def _find_neighbors(self, cell: cls.Cell) -> list[cls.Cell]:
        """
        Finds the neighboring cells for a given cell. Neighbors share exactly two points.

        Args:
            cell (cls.Cell): The cell for which neighbors are to be determined.

        Returns:
            list[cls.Cell]: List of neighboring cells.
        """
        points_in_cell = set(cell.points)
        return [
            internal_cell
            for internal_cell in self._cells
            if len(points_in_cell & set(internal_cell.points)) == 2
        ]

    def _midpoint(self, cell: cls.Cell) -> npt.NDArray[np.float64]:
        """
        Computes the midpoint of a cell based on its points.

        Args:
            cell (cls.Cell): The cell for which the midpoint is calculated.

        Returns:
            npt.NDArray[np.float32]: Coordinates of the cell's midpoint.
        """
        return (1 / cell.type) * (np.sum(cell.coordinates, axis=0))

    def _calculate_area(self, cell: cls.Triangle) -> float:
        """
        Calculates the area of a triangular cell.

        Args:
            cell (cls.Triangle): The triangular cell.

        Returns:
            float: Area of the triangle, or None if the cell is not triangular.
        """
        if cell.type == 3:
            point_coordinates = cell.coordinates
            x0, y0 = point_coordinates[0]
            x1, y1 = point_coordinates[1]
            x2, y2 = point_coordinates[2]

            return 0.5 * abs((x0 - x2) * (y1 - y0) - (x0 - x1) * (y2 - y0))
        else:
            raise Exception(f"Calculate area for cell type with amount of points {cell.type} has not been implemented")

    def _unit_and_scaled_normal_vector(
        self, cell: cls.Cell
    ) -> list[npt.NDArray[np.float64]]:
        """
        Computes unit and scaled normal vectors for the edges of a cell.

        Args:
            cell (cls.Cell): The cell for which normal vectors are calculated.

        Returns:
            list[npt.NDArray[np.float32]]: List of scaled normal vectors for the cell's edges.
        """

        cell_ngh = cell.neighbors
        scaled_normal_vectors = [0 for i in cell_ngh]
        for index, ngh in enumerate(cell_ngh):
            # Finds the normal vector
            point2, point1 = set(ngh.points) & set(cell.points)
            edge_vector = point2.coordinates - point1.coordinates
            normal_vector = np.flip(edge_vector.copy())
            normal_vector[0] = -normal_vector[0]

            # Finds unit normal and scaled normal
            unit_normal_vector = normal_vector / np.linalg.norm(normal_vector)
            scaled_normal = unit_normal_vector * np.linalg.norm(edge_vector)
            midpoint_edge = (point1.coordinates + point2.coordinates) / 2
            middle = midpoint_edge - cell.midpoint

            # Check if the normal is pointing outwards or inwards, flips it if it points inwards.
            if np.dot(middle, scaled_normal) < 0:
                scaled_normal_vectors[index] = -scaled_normal
            else:
                scaled_normal_vectors[index] = scaled_normal
        return scaled_normal_vectors

    def _velocity(self, cell: cls.Cell) -> npt.NDArray[np.float64]:
        """
        Computes the velocity at the midpoint of a cell.

        Args:
            cell (cls.Cell): The cell for which velocity is calculated.

        Returns:
            npt.NDArray[np.float32]: Velocity vector at the cell's midpoint.
        """
        cell_midpoint = cell.midpoint
        return np.array([cell_midpoint[1] - 0.2 * cell_midpoint[0], -cell_midpoint[0]])

    def calculate(self, cell: cls.Cell) -> npt.NDArray[np.float64]:
        """
        Computes and assigns properties (neighbors, midpoint, area, velocity, normals) for a cell.

        Args:
            cell (cls.Cell): The cell to calculate properties for.
        """

        cell.neighbors = self._find_neighbors(cell)
        cell.midpoint = self._midpoint(cell)
        cell.area = self._calculate_area(cell)
        cell.velocity = self._velocity(cell)
        cell.scaled_normal = self._unit_and_scaled_normal_vector(cell)

    def initial_oil_distribution(self, start_point: npt.NDArray[np.float64]):
        """
        Initializes the oil distribution across the mesh, centered around a given start point.

        Args:
            start_point (npt.NDArray[np.float32]): The starting point for oil distribution.
        """
        cells = self._cells
        for cell in cells:
            u = np.exp(-np.sum((cell.midpoint - start_point) ** 2) / 0.01)
            cell.oil_amount = u

    def calculate_change(self, cell: cls.Cell, dt: float):
        """
        Calculates the change in oil distribution for a cell over a given time step.

        Args:
            cell (cls.Cell): The cell for which the oil change is calculated.
            dt (float): Time step for the calculation.
        """
        flux = 0
        neighbors = cell.neighbors

        def _g(
            a: float, b: float, v: npt.NDArray[np.float64], w: npt.NDArray[np.float64]
        ):
            """
            Required part of calculate_area
            """
            dot_product = np.dot(v, w)

            if dot_product > 0:
                return a * dot_product
            else:
                return b * dot_product

        for index, neighbor in enumerate(neighbors):
            scaled_normal = cell.scaled_normal[index]
            v_mid = 0.5 * (cell.velocity + neighbor.velocity)
            flux += -(dt / cell.area) * _g(
                cell.oil_amount, neighbor.oil_amount, scaled_normal, v_mid
            )
        cell.oil_change += flux