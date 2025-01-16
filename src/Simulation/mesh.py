import meshio
import numpy.typing as npt
from src.Simulation.cells import *

class CellFactory:
    def __init__(self):
        self._cell_types = {}

    def register(self, amount_of_points: int, cell_class: object):
        """
        Registers a new cell type with the factory
        """
        self._cell_types[amount_of_points] = cell_class

    def __call__(self, cell: list[int], index: int, points_list: list[Point]):
        """
        Creates a cell object based on the input dictionary
        """
        key = len(cell)
        if key not in self._cell_types:
            raise Exception(f"Unkown cell type: {key}")
        
        points = [points_list[i] for i in cell]
        return self._cell_types[key](index, points)

class Mesh:
    """
    Initializes empty lists for points and cells and reads the mesh file. The initializer then makes Triangle and Line objects from the mesh file,
    each with a index and a list of points.

    Args:
        - msh_file: a Mesh file, denoted by .msh

    Returns:
        - Triangle and Line objects.
    """

    def __init__(self, msh_file: str, cell_factory: CellFactory) -> None:
        self._cell_index = -1  # The index of a cell in _cells
        msh = meshio.read(msh_file)  # Reads the meshfile
        # Generates a list containing point objects
        self._points = [Point(index, np.float32(points[0]), np.float32(points[1])) for index, points in enumerate(msh.points)]
        # Generates a list containing cell objects
        self._cells = []
        for cell_types in msh.cells:
            self._cells.extend([cell_factory(cell, self._cell_index, self._points) for cell in cell_types.data])
    
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

    def _find_neighbors(self, cell: Cell) -> list[Cell]:
        """
        Finds neighboring cells for the cell specified, neighbors share exactly two elements
        """
        neighboring_cells = []
        points_in_cell = cell.points

        # Assuming cells with more points than triangles have are neighbors if they share two points. 
        # This function is extendable for any cell type that meets that criteria
        # Makes a list with the indicies of the neighbors for the specified cell
        neighboring_cells = [cells for cells in self._cells if len(set(points_in_cell) & set(cells.points)) == 2]

        # Store neighbors in each cell, stores the neighbors in the cell that was checked
        return neighboring_cells

    def _midpoint(self, cell: Cell) -> npt.NDArray[np.float32]:
        """
        Same as X_mid from task description. Takes a cell of any shape and finds the midpoint
        """
        point_coordinates = cell.coordinates
        number_of_points = len(point_coordinates)
        sum_coordinates = np.array([0, 0])
        for coordinates in point_coordinates:
            sum_coordinates = sum_coordinates + coordinates
        return (1 / number_of_points) * (sum_coordinates)
        # return np.mean(cell.coordinates)

    def _calculate_area(self, cell: Triangle) -> float:
        """
        Calculates the area of triangle cells
        """
        point_coordinates = cell.coordinates
        if len(point_coordinates) == 3:
            x0, y0 = point_coordinates[0]
            x1, y1 = point_coordinates[1]
            x2, y2 = point_coordinates[2]

            return 0.5 * abs((x0 - x2) * (y1 - y0) - (x0 - x1) * (y2 - y0))
        else:
            return None
    

    def _unit_and_scaled_normal_vector(self, cell: Cell) -> list[npt.NDArray[np.float32]]:
        """
        Finds the unit normal vector based on two points. The points must must be on the same facet
        """

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
        
    
    def _velocity(self, cell: Cell) -> npt.NDArray[np.float32]:
        """
        Finds the velocity of the oil in the midpoint of a cell. Returns a vector
        """
        cell_midpoint = cell.midpoint
        return np.array([cell_midpoint[1] - 0.2 * cell_midpoint[0], -cell_midpoint[0]])

    def calculate(self, cell: Cell) -> npt.NDArray[np.float32]:
        cell.neighbors = self._find_neighbors(cell)
        cell.midpoint = self._midpoint(cell)
        cell.area = self._calculate_area(cell)
        cell.velocity = self._velocity(cell)
        cell.scaled_normal = self._unit_and_scaled_normal_vector(cell)
        

    def print_neighbors(self, cell: Cell, object_output: bool=False) -> None:
        """
        Print the neighbors as indicies or objects depending of what is specified. Does not return anything
        """
        if object_output == True:
            try:
                print(f"The neighbors of {cell.index} is {cell.neighbors}")
            except IndexError:
                print(f"Cell {cell} does not exist in cells")
        else:
            try:
                print(f"""The neighbors of {cell.index} is {[ngh.index for ngh in cell.neighbors]}""")
            except IndexError:
                print(f"Cell {cell.index} does not exist in cells")