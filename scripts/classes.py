import meshio
import math_function as mf
import numpy as np
import numpy.typing as npt


class Point:
    def __init__(self, index: int, x: float, y: float) -> None:
        """
        Initializes a Point with x and y coordinates
        """
        self._index = index
        self._coordinates = np.array([x, y])

    # Returns the index of the point in the point list from mesh
    @property
    def index(self) -> int:
        return self._index

    # Returns the coordinates of the point
    @property
    def coordinates(self) -> npt.NDArray[np.float32]:
        return self._coordinates

class CellFactory:
    def __init__(self):
        self._cell_types = {"line": LineTypeCell,
                            "triangle": TriangleTypeCell,
                            "vertex": VertexTypeCell
                            }

    def register(self, key: str, cell_class):
        """
        Registers a new cell type with the factory
        """
        self._cell_types[key] = cell_class

    def __call__(self, cell: dict):
        """
        Creates a cell object based on the input dictionary
        """
        key = cell["type"]
        if key not in self._cell_types:
            raise ValueError(f"Unkown cell type: {key}")
        return self._cell_types[key](cell["index"], cell["points"])

class Cell:
    def __init__(self, index: int, points: npt.NDArray[np.float32]) -> None:
        """
        Initiliazes a Cell with ID (its position in the Mesh Cells list)
        and a list of points for the Cell

        Args:
        - index:
        - points:
        """
        self._index = index
        self._points = points
        self._neighbors = []
        self._oil_amount = 0

    @property
    def coordinates(self) -> list:
        return [point.coordinates for point in self._points]

    @property
    def oil_amount(self):
        return self._oil_amount

    @oil_amount.setter
    def oil_amount(self, value):
        self._oil_amount = value

    @property
    def index(self) -> int:
        """
        Returns the index of the cell from the cell list
        """
        return self._index

    # getter for points
    @property
    def points(self) -> list[int]:
        """
        Returns all points contained within this cell with their index in the point list
        """
        return self._points

    @property
    def neighbors(self) -> list[int]:
        """
        Returns neighbors if they have been stored previously
        """
        if len(self._neighbors) == 0:
            print(f"Cell {self._index} does not contain a neighbor currently")

        else:
            return self._neighbors

    @neighbors.setter
    def neighbors(self, neighboring_cells: list[int]) -> None:
        """
        Stores the neighbors found in find_neighbors() from the mesh class in this cell
        """
        self._neighbors = neighboring_cells


class TriangleTypeCell(Cell):
    def __init__(self, index: int, points: npt.NDArray[np.float32]) -> None:
        super().__init__(index, points)
    
    @property
    def type(self) -> str:
        return "triangle"

class LineTypeCell(Cell):
    def __init__(self, index: int, points: npt.NDArray[np.float32]) -> None:
        super().__init__(index, points)
    
    @property
    def type(self) -> str:
        return "line"

class VertexTypeCell(Cell):
    def __init__(self, index: int, points: npt.NDArray[np.float32]) -> None:
        super().__init__(index, points)

    @property
    def type(self) -> str:
        return "vertex"


class Mesh:
    """
    Initializes empty lists for points and cells and reads the mesh file. The initializer then makes Triangle and Line objects from the mesh file,
    each with a index and a list of points.

    Args:
        - msh_file: a Mesh file, denoted by .msh

    Returns:
        - Triangle and Line objects.
    """

    def __init__(self, msh_file: str) -> None:
        self._cell_index = 0
        self._factory = CellFactory()

        msh = meshio.read(msh_file)

        # Generates a list containing point objects
        self._points = [
            Point(index, np.float32(points[0]), np.float32(points[1]))
            for index, points in enumerate(msh.points)
        ]

        # Generates a list containing cell objects of the type line or triangle
        self._cells = []
        for cell_block in msh.cells:
            cell_type = cell_block.type
            for cell_data in cell_block.data:
                cell_info = {
                    "type": cell_type,
                    "index": self._cell_index,
                    "points": [self._points[i] for i in cell_data]
                }
                self._cell_index += 1
                try:
                    self._cells.append(self._factory(cell_info))
                except ValueError as e:
                    print(f"Not able to read cell type {cell_type}: {e}")

    @property
    def cells(self) -> list[object]:
        """
        Returns the list of all point objects
        """
        return self._cells

    def find_neighbors(self, cell_index: int) -> None:
        """
        Finds neighboring cells for the cell specified, neighbors share exactly two elements
        """
        neighboring_cells = []
        points_in_cell = self._cells[cell_index].points

        # Assuming cells with more points than triangles have are neighbors if they share two points. 
        # This function is extendable for any cell type that meets that criteria
        # Makes a list with the indicies of the neighbors for the specified cell
        neighboring_cells = [cells for cells in self._cells if len(set(points_in_cell) & set(cells.points)) == 2]

        # Store neighbors in each cell, stores the neighbors in the cell that was checked
        self._cells[cell_index].neighbors = neighboring_cells

    def print_neighbors(self, cell_index: int, object_output: bool=False) -> None:
        """
        Print the neighbors as indicies or objects depending of what is specified. Does not return anything
        """
        if object_output == True:
            try:
                print(f"The neighbors of {cell_index} is {self._cells[cell_index].neighbors}")
            except IndexError:
                print(f"Cell {cell_index} does not exist in cells")
        else:
            try:
                print(f"The neighbors of {cell_index} is {[ngh.index for ngh in self._cells[cell_index].neighbors]}")
            except IndexError:
                print(f"Cell {cell_index} does not exist in cells")
    
