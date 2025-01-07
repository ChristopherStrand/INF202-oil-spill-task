import meshio
import math_function
import math_function

class Point:
    def __init__(self, index: int, x: float, y: float) -> None:
        """
        Initializes a Point with x and y coordinates
        """
        self._index = index
        self.x = x
        self.y = y

class Cell:
    def __init__(self, index: int, points: list[Point]) -> None:
        """
        Initiliazes a Cell with ID (its position in the Mesh Cells list)
        and a list of points for the Cell

        Args:
        - index: 
        - points: 
        """
        self.index = index
        self._points = points
        self._points = points
        self._neighbors = []
        self.oil_amount = 0
        

    @property
    def points(self):
        return self._points

    def __str__(self) -> str:
        """
        Checks if Cell is Boundary and returns a string with its neighbors
        """
        is_boundary = len(self._neighbors) < 2
        neighbor_indices = [neighbor.index for neighbor in self._neighbors]
        boundary_status = "Boundary" if is_boundary else "Internal"
        
        return f"Cell {self.index} ({boundary_status}): Neighbors -> {neighbor_indices}"


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
        self._cell_index = 0
        msh = meshio.read(msh_file)
        self._points = [Point(index, *points[:2]) for index, points in enumerate(msh.points)]
        self._cells = []
        for cell_block in msh.cells:
            if cell_block.type in ["triangle", "line"]:
                self._cells.extend([self.cell_factory(cell, cell_block.type) for cell in cell_block.data])

    def cell_factory(self, cell_data: list[int], cell_type: str) -> Cell:
        points = [self._points[idx] for idx in cell_data]
        self._cell_index += 1
        if cell_type == "triangle":
            return Triangle(self._cell_index, points)
        elif cell_type == "line":
            return Line(self._cell_index, points)
            
    def find_neighbors(self) -> None:
        """
        Finds neighboring cells for each cell in the mesh.

        First checks if it is a Triangle or a Line by how many points they contain. 
        """
        for cell in self._cells:
            neighbors = []
            if len(cell.points) == 3:
                for other_cell in self._cells:
                    if other_cell != cell:
                        # Check if they share exactly two points
                        shared_points = set(cell._points).intersection(set(other_cell._points))
                        if len(shared_points) == 2:
                            neighbors.append(other_cell)

            elif len(cell.points) == 2:
                for other_cell in self._cells:
                    if other_cell != cell:
                        # Check if they share 1 point if other_cell is a Line og 2 points if other_cell is a Triangle
                        shared_points = set(cell._points).intersection(set(other_cell._points))
                        if len(shared_points) == 1 and len(other_cell.points) == 2 or len(shared_points) == 2 and len(other_cell.points) == 3:
                            neighbors.append(other_cell)
                    
            # Store the neighboring cells for this cell
            cell._neighbors = neighbors
 
 

    def print_neighbors(self, cell_index: int) -> None:
        cell = next((cell for cell in self.cells if cell.index == cell_index), None)
        if cell:
            print(cell)
        else:
            print(f"Cell {cell_index} does not exist in the mesh.")
            print(f"Cell {cell_index} does not exist in the mesh.")
