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
        self._midpoint = 0
        self._area = 0
        self._normal = 0
        self._velocity = 0
        #midpoint, area, normal vector, velocity

    @property
    def coordinates(self) -> list:
        return [point.coordinates for point in self._points]

    @property
    def oil_amount(self):
        return self._oil_amount

    @oil_amount.setter
    def oil_amount(self, value):
        if value < 0:
            raise ("Oil amount cannot be negative!")
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
    def normal(self):
        return self._normal
    
    @normal.setter
    def area(self, normal_vector: npt.NDArray[np.float32]):
        self._normal = normal_vector

    @property
    def velocity(self):
        return self._velocity
    
    @velocity.setter
    def velocity(self, velocity_vector: npt.NDArray[np.float32]):
        self._velocity = velocity_vector


class Triangle(Cell):
    def __init__(self, index: int, points: npt.NDArray[np.float32]) -> None:
        super().__init__(index, points)


class Line(Cell):
    def __init__(self, index: int, points: npt.NDArray[np.float32]) -> None:
        super().__init__(index, points)


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
        self._cell_index = -1  # The index of a cell in _cells
        msh = meshio.read(msh_file)  # Reads the meshfile
        # Generates a list containing point objects
        self._points = [
            Point(index, np.float32(points[0]), np.float32(points[1]))
            for index, points in enumerate(msh.points)
        ]
        # Generates a list containing cell objects of the type line or triangle
        self._cells = []
        for cell_types in msh.cells:
            types = cell_types.type
            if (
                types != "vertex" and types != "line"
            ):  # Ignores lines since they aren't relevant for the task
                self._cells.extend(
                    [self._cell_factory(cell) for cell in cell_types.data]
                )

    def _cell_factory(self, cell: list[int]) -> object:  # Mainly used for extendability
        cell_check = len(cell)
        cell_map = {2: Line, 3: Triangle}

        points = [self._points[i] for i in cell]
        self._cell_index += 1

        return cell_map[cell_check](self._cell_index, points)
    
    @property
    def cells(self) -> list[object]:
        """
        Returns the list of all point objects
        """
        return self._cells

    @property
    def points(self) -> list[object]:
        """
        Returns the list of all point objects
        """
        return self._points

    def _find_neighbors(self, cell_index: int) -> None:
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


        # self._midpoint = 0
        # self._area = 0
        # self._normal_vector = 0
        # self._velocity = 0
    
    def _midpoint(self, cell_index: int) -> npt.NDArray[np.float32]:
        """
        Same as X_mid from task description. Takes a cell of any shape and finds the midpoint
        """
        point_coordinates = self._cells[cell_index].coordinates
        number_of_points = len(point_coordinates)
        sum_coordinates = np.array([0, 0])
        for coordinates in point_coordinates:
            sum_coordinates = sum_coordinates + coordinates
        return (1 / number_of_points) * (sum_coordinates)

    def _calculate_area(self, cell_index: int) -> float:
        """
        Calculates the area of triangle cells
        """
        point_coordinates = self._cells[cell_index].coordinates
        if len(point_coordinates) != 3:
            raise Exception("Invalid cell, must be a triangle")
        x0, y0 = point_coordinates[0]
        x1, y1 = point_coordinates[1]
        x2, y2 = point_coordinates[2]

        return 0.5 * abs((x0 - x2) * (y1 - y0) - (x0 - x1) * (y2 - y0))
    

    def _unit_normal_vector(self, cell_index: int) -> npt.NDArray[np.float32]:
        """
        Finds the unit normal vector based on two points. The points must must be on the same facet
        """
        for ngh in self._cells[cell_index].neighbors:
            point1, point2 = set(self._cells[cell_index].points) & set(ngh.points)
            vector = point2 - point1
            normal_vector = np.array([-vector[1], vector[0]])
            return normal_vector / np.linalg.norm(normal_vector)
    
    
    def _velocity(self, cell_index: int) -> npt.NDArray[np.float32]:
        """
        Finds the velocity of the oil in the midpoint of a cell. Returns a vector
        """
        cell_midpoint = self._cells[cell_index].midpoint
        return np.array([cell_midpoint[1] - 0.2 * cell_midpoint[0], -cell_midpoint[0]])

    def calculate(self, cell_index: int) -> npt.NDArray[np.float32]:
        current_cell = self._cells[cell_index] 
        current_cell.midpoint = self._midpoint(cell_index)
        current_cell.area = self._midpoint(cell_index)
        current_cell.normal = self._midpoint(cell_index)
        current_cell.velocity = self._velocity(cell_index)

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

if __name__ == "__main__":
    mesh = Mesh("meshes/bay.msh")
    print(mesh.cells[4].coordinates)
    mesh.find_neighbors(4)
    mesh.print_neighbors(4)
    #[45, 46, 2056]
    # x = mesh.cells[45].coordinates
    # print(x)
