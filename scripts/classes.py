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
    
    def store_neighbors(self, neighboring_cells: list[object]):
        self._neighbors = neighboring_cells

    def __str__(self) -> str:
        """
        Checks if Cell is Boundary and returns a string with its neighbors
        """
        is_boundary = len(self._neighbors) < 2
        neighbor_indices = [neighbor.index for neighbor in self._neighbors]
        boundary_status = "Boundary" if is_boundary else "Internal"
        
        return f"Cell {self._index} ({boundary_status}): Neighbors -> {neighbor_indices}"


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
            if cell_types.type != "vertex":
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
            

    def find_neighbors(self) -> None:
        """
        Finds neighboring cells for each cell in the mesh.
        First checks if it is a Triangle or a Line by how many points they contain. 
        """
        for cell in self._cells:
            neighbors = []
            if len(cell.points()) == 3:
                for other_cell in self._cells:
                    if other_cell != cell:
                        # Check if they share exactly two points
                        shared_points = set(cell._points).intersection(set(other_cell._points))
                        if len(shared_points) == 2:
                            neighbors.append(other_cell)

            #Store neighbors in each cell
            cell.store_neighbors(neighbors)

    def print_neighbors(self, cell_index: int) -> None:
        for c in self._cells:
            if c.index == cell_index:
                print(c)
                break
        else:
            print(f"Cell {cell_index} does not exist in the mesh.")
