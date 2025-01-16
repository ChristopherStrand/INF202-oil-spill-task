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
        return self._cell_types[key](self._cell_index, points)


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
        self._points = [cls.Point(index, np.float32(points[0]), np.float32(points[1])) for index, points in enumerate(msh.points)]
        self._cells = []
        for cell_types in msh.cells:
            self._cells.extend([cell_factory(cell, self._points) for cell in cell_types.data])
    
    @property
    def cells(self) -> list[cls.Cell]:
        return self._cells

    @property
    def points(self) -> list[cls.Point]:
        return self._points
    
    def _cells_within_area(self, x_area: npt.NDArray[np.float32], y_area: npt.NDArray[np.float32]) -> list[cls.Cell]:
        g = [cell for cell in self._cells if np.array(cell.coordinates).any(axis=0)]
        print(len(g))

    def _find_neighbors(self, cell: cls.Cell) -> list[cls.Cell]:
        """
        Finds the neighboring cells for a given cell. Neighbors share exactly two points.

        Args:
            cell (cls.Cell): The cell for which neighbors are to be determined.

        Returns:
            list[cls.Cell]: List of neighboring cells.
        """
        neighboring_cells = []
        points_in_cell = cell.points
        neighboring_cells = [cells for cells in self._cells if len(set(points_in_cell) & set(cells.points)) == 2]
        return neighboring_cells

    def _midpoint(self, cell: cls.Cell) -> npt.NDArray[np.float32]:
        """
        Computes the midpoint of a cell based on its points.

        Args:
            cell (cls.Cell): The cell for which the midpoint is calculated.

        Returns:
            npt.NDArray[np.float32]: Coordinates of the cell's midpoint.
        """
        point_coordinates = cell.coordinates
        number_of_points = len(point_coordinates)
        sum_coordinates = np.array([0, 0])
        for coordinates in point_coordinates:
            sum_coordinates = sum_coordinates + coordinates
        return (1 / number_of_points) * (sum_coordinates)
        # return np.mean(cell.coordinates)

    def _calculate_area(self, cell: cls.Triangle) -> float:
        """
        Calculates the area of a triangular cell.

        Args:
            cell (cls.Triangle): The triangular cell.

        Returns:
            float: Area of the triangle, or None if the cell is not triangular.
        """
        point_coordinates = cell.coordinates
        if len(point_coordinates) == 3:
            x0, y0 = point_coordinates[0]
            x1, y1 = point_coordinates[1]
            x2, y2 = point_coordinates[2]

            return 0.5 * abs((x0 - x2) * (y1 - y0) - (x0 - x1) * (y2 - y0))
        else:
            return None
  
    def _unit_and_scaled_normal_vector(self, cell: cls.Cell) -> list[npt.NDArray[np.float32]]:
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
            normal_vector = np.array([-edge_vector[1], edge_vector[0]]) 

            # Finds unit normal and scaled normal
            unit_normal_vector = normal_vector / np.linalg.norm(normal_vector)
            scaled_normal = unit_normal_vector * np.linalg.norm(edge_vector)
            midpoint_edge = (point1.coordinates + point2.coordinates)/2
            middle = midpoint_edge - cell.midpoint

            # Check if the normal is pointing outwards or inwards, flips it if it points inwards.
            if np.dot(middle, scaled_normal) < 0:
                scaled_normal_vectors[index] = -scaled_normal
            else:
                scaled_normal_vectors[index] = scaled_normal
        return scaled_normal_vectors
    
    def _velocity(self, cell: cls.Cell) -> npt.NDArray[np.float32]:
        """
        Computes the velocity at the midpoint of a cell.

        Args:
            cell (cls.Cell): The cell for which velocity is calculated.

        Returns:
            npt.NDArray[np.float32]: Velocity vector at the cell's midpoint.
        """
        cell_midpoint = cell.midpoint
        return np.array([cell_midpoint[1] - 0.2 * cell_midpoint[0], -cell_midpoint[0]])

    def calculate(self, cell: cls.Cell) -> npt.NDArray[np.float32]:
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

    def initial_oil_distribution(self, start_point: npt.NDArray[np.float32]):
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

        def _g(a: float, b: float, v: npt.NDArray[np.float32], w: npt.NDArray[np.float32]):
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
            v_mid = 0.5*(cell.velocity + neighbor.velocity)
            flux = flux + (-(dt / cell.area) * _g(cell.oil_amount, neighbor.oil_amount, scaled_normal, v_mid))
        cell.oil_change += flux
        
    def print_neighbors(self, cell: cls.Cell, object_output: bool = False) -> None:
        """
        Prints the neighbors of a given cell, either as objects or indices.

        Args:
            cell (cls.Cell): The cell whose neighbors are printed.
            object_output (bool): Whether to print neighbors as objects (default: False).
        """
        if object_output is True:
            try:
                print(f"The neighbors of {cell.index} is {cell.neighbors}")
            except IndexError:
                print(f"Cell {cell} does not exist in cells")
        else:
            try:
                print(f"""The neighbors of {cell.index} is {[ngh.index for ngh in cell.neighbors]}""")
            except IndexError:
                print(f"Cell {cell.index} does not exist in cells")