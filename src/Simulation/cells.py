import numpy as np
import numpy.typing as npt


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
        self._oil_amount = 0.0 
        self._oil_change = 0.0
        self._midpoint = np.float32([0, 0]) 
        self._area = 0.0 
        self._velocity = np.float32([0, 0]) 
        self._scaled_normal = []

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
    def oil_change(self):
        return self._oil_change

    @oil_change.setter
    def oil_change(self, value):
        self._oil_change = value

    @property
    def index(self) -> int:
        """
        Returns the index of the cell from the cell list
        """
        return self._index
    
    @property
    def midpoint(self):
        return self._midpoint
    
    @midpoint.setter
    def midpoint(self, mid_coordinates: npt.NDArray[np.float32]):
        self._midpoint = mid_coordinates
    
    @property
    def area(self):
        return self._area
    
    @area.setter
    def area(self, area_of_cell: float):
        self._area = area_of_cell
    
    @property
    def scaled_normal(self):
        return self._scaled_normal

    @scaled_normal.setter
    def scaled_normal(self, scaled_vector: npt.NDArray[np.float32]):
        self._scaled_normal = scaled_vector

    @property
    def velocity(self):
        return self._velocity
    
    @velocity.setter
    def velocity(self, velocity_vector: npt.NDArray[np.float32]):
        self._velocity = velocity_vector

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

    def __str__(self):
        return f"""Current cell is {self._index}: 
                  midpoint: {self._midpoint}, 
                  area: {self._area}, 
                  normal: {self._scaled_normal}, 
                  velocity: {self._velocity}
                  neighbors: {[ngh.index for ngh in self._neighbors]}"""
    

#------------------------------cells end---------------------------------------
class Point:
    def __init__(self, index: int, x: float, y: float) -> None:
        """
        Initializes a Point with x and y coordinates
        """
        self._index = index
        self._coordinates = np.array([x, y])

    @property
    def index(self) -> int:
        return self._index

    @property
    def coordinates(self) -> npt.NDArray[np.float32]:
        return self._coordinates

class Vertex(Cell):
    def __init__(self, index: int, points: npt.NDArray[np.float32]) -> None:
        super().__init__(index, points)

class Line(Cell):
    def __init__(self, index: int, points: npt.NDArray[np.float32]) -> None:
        super().__init__(index, points)

class Triangle(Cell):
    def __init__(self, index: int, points: npt.NDArray[np.float32]) -> None:
        super().__init__(index, points)

