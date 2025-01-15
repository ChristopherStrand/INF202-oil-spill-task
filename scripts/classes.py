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


class Triangle(Cell):
    def __init__(self, index: int, points: npt.NDArray[np.float32]) -> None:
        super().__init__(index, points)


class Line(Cell):
    def __init__(self, index: int, points: npt.NDArray[np.float32]) -> None:
        super().__init__(index, points)

class Vertex(Cell):
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
        self._points = [Point(index, np.float32(points[0]), np.float32(points[1])) for index, points in enumerate(msh.points)]
        # Generates a list containing cell objects of the type line or triangle
        self._cells = []
        for cell_types in msh.cells:
            types = cell_types.type
            # Ignores lines since they aren't relevant for the task
            self._cells.extend([self._cell_factory(cell) for cell in cell_types.data])

    def _cell_factory(self, cell: list[int]) -> object:  # Mainly used for extendability
        cell_check = len(cell)
        cell_map = {1:Vertex, 2: Line, 3: Triangle}

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
        return neighboring_cells

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
        if len(point_coordinates) == 3:
            x0, y0 = point_coordinates[0]
            x1, y1 = point_coordinates[1]
            x2, y2 = point_coordinates[2]

            return 0.5 * abs((x0 - x2) * (y1 - y0) - (x0 - x1) * (y2 - y0))
        else:
            return None
    

    def _unit_and_scaled_normal_vector(self, cell_index: int) -> list[npt.NDArray[np.float32]]:
        """
        Finds the unit normal vector based on two points. The points must must be on the same facet
        """

        cell = self._cells[cell_index]
        cell_ngh = cell.neighbors
        
        scaled_normal_vectors = [0 for i in cell_ngh]
        for index, ngh in enumerate(cell_ngh):
            #Finds the normal vector
            point2, point1 = set(ngh.points) & set(cell.points)
            edge_vector = point2.coordinates - point1.coordinates
            normal_vector = np.array([-edge_vector[1], edge_vector[0]]) 

            #Finds unit normal and scaled normal
            unit_normal_vector = normal_vector / np.linalg.norm(normal_vector)
            scaled_normal = unit_normal_vector * np.linalg.norm(edge_vector) #Multiplies by the length of a side
            
            midpoint_edge = (point1.coordinates + point2.coordinates)/2
            middle = midpoint_edge - cell.midpoint

            if np.dot(middle, scaled_normal) < 0:
                scaled_normal_vectors[index] = -scaled_normal
            else:
                scaled_normal_vectors[index] = scaled_normal
        return scaled_normal_vectors
        
    
    def _velocity(self, cell_index: int) -> npt.NDArray[np.float32]:
        """
        Finds the velocity of the oil in the midpoint of a cell. Returns a vector
        """
        cell_midpoint = self._cells[cell_index].midpoint
        return np.array([cell_midpoint[1] - 0.2 * cell_midpoint[0], -cell_midpoint[0]])

    def calculate(self, cell_index: int) -> npt.NDArray[np.float32]:
        current_cell = self._cells[cell_index]
        current_cell.neighbors = self._find_neighbors(cell_index)
        current_cell.midpoint = self._midpoint(cell_index)
        current_cell.area = self._calculate_area(cell_index)
        current_cell.velocity = self._velocity(cell_index)
        current_cell.scaled_normal = self._unit_and_scaled_normal_vector(cell_index)
        

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
                print(f"""The neighbors of {cell_index} is {[ngh.index for ngh in self._cells[cell_index].neighbors]}""")
            except IndexError:
                print(f"Cell {cell_index} does not exist in cells")