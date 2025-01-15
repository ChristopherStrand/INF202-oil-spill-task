import numpy.typing as npt
import numpy as np

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