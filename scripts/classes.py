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
        self._coordinates = np.array(x, y)

    #Returns the index of the point in the point list from mesh
    def index(self) -> int:
        return self._index
    
    #Returns the coordinates of the point
    def coordinates(self) -> npt.NDArray[np.float32]:
        return self._coordinates

class Cell:
    def __init__(self, index: int, points: list[Point]) -> None:
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

    #Returns the index of the cell from the cell list
    def index(self) -> int:
        return self._index
    
    #Returns all points contained within this cell with their index in the point list
    def points(self) -> list[np.float32]:
        return self._points 
    
    def neighbors(self) -> list[object]:
        return self._neighbors
    
    def store_neighbors(self, neighboring_cells: list[object]):
        self._neighbors = neighboring_cells

    # def __str__(self) -> str:
    #     """
    #     Checks if Cell is Boundary and returns a string with its neighbors
    #     """
    #     is_boundary = len(self._neighbors) < 2
    #     neighbor_indices = [neighbor.index for neighbor in self._neighbors]
    #     boundary_status = "Boundary" if is_boundary else "Internal"
        
    #     return f"Cell {self._index} ({boundary_status}): Neighbors -> {neighbor_indices}"


class Triangle(Cell):
    def __init__(self, index: int, points: list[Point]) -> None:
        super().__init__(index, points)


class Line(Cell):
    def __init__(self, index: int, points: list[Point]) -> None:
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
        self._cell_index = -1 #The index of a cell in _cells
        msh = meshio.read(msh_file) #Reads the meshfile 
        #Generates a list containing point objects
        self._points = [Point(index, np.float32(points[0]), np.float32(points[1])) for index, points in enumerate(msh.points)]
        #Generates a list containing cell objects of the type line or triangle
        self._cells = []
        for cell_types in msh.cells:
            types = cell_types.type
            if types != "vertex" and types != "line": #Ignores lines since they aren't relevant for the task
                self._cells.extend([self.cell_factory(cell) for cell in cell_types.data])

    def cell_factory(self, cell: list[int]) -> object:
        cell_check = len(cell)
        cell_map = {
            2: Line,
            3: Triangle
            }

        points = [self._points[i] for i in cell]
        self._cell_index += 1
        
        return cell_map[cell_check](self._cell_index, points)
            

    def find_neighbors(self, cell_index: int) -> None:
        """
        Finds neighboring cells for the cell specified.
        First checks if it is a Triangle or a Line by how many points they contain. 
        """
        neighboring_cells = []
        points_in_cell = self._cells[cell_index].points()
        
        #Checks triangles for neighbors
        if len(points_in_cell) == 3:
            #The points of the current cell, avoiding using a for loop to save performance
            point_0 = points_in_cell[0].index()
            point_1 = points_in_cell[1].index()
            point_2 = points_in_cell[2].index()
            for cells in self._cells:
                point_indices = [points.index() for points in cells.points()]
                #Checks if two different cells has exactly two points equal eachother. 
                #This is done by taking the sum of three boolean statements that are true if the cell, 
                #whose neighbors are being checked, have a point that is equal in the cell being checked.
                if sum((point_0 in point_indices, point_1 in point_indices, point_2 in point_indices)) == 2:
                    neighboring_cells.append(cells.index())

            #Store neighbors in each cell
            self._cells[cell_index].store_neighbors(neighboring_cells)

    def print_neighbors(self, cell_index: int) -> None:
        try:
            print(f"The neighbors of {cell_index} is {self._cells[cell_index].neighbors()}")
        except IndexError:
            print(f"Cell {cell_index} does not exist in cells")
