import meshio

class Point:
    def __init__(self, x: float, y: float) -> None:
        """
        Initializes a Point with x and y coordinates
        """
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
        self.points = points
        self._neighbors = []
        self.oil_amount = oil_amount

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
    def __init__(self, msh_file: str) -> None:
        """
        Initializes empty lists for points and cells and reads the mesh file. The initializer then makes Triangle and Line objects from the mesh file,
        each with a index and a list of points. 

        Args:
        - msh_file: a Mesh file, denoted by .msh

        Returns:
        - Triangle and Line objects.
        """

        self.points = []
        self.cells = []

        msh = meshio.read(msh_file)

        # Add points to the mesh
        for i, point in enumerate(msh.points):
            self.points.append(Point(point[0], point[1]))

        # Add cells to the mesh based on their type
        cell_index = 0
        for cell_block in msh.cells:
            if cell_block.type == "triangle":
                for cell in cell_block.data:
                    self.cells.append(Triangle(cell_index, [self.points[p] for p in cell]))
                    cell_index += 1
            elif cell_block.type == "line":
                for cell in cell_block.data:
                    self.cells.append(Line(cell_index, [self.points[p] for p in cell]))
                    cell_index += 1
            

    def find_neighbors(self) -> None:
        """
        Finds neighboring cells for each cell in the mesh.

        First checks if it is a Triangle or a Line by how many points they contain. 
        """
        for cell in self.cells:
            neighbors = []
            if len(cell.points) == 3:
                for other_cell in self.cells:
                    if other_cell != cell:
                        # Check if they share exactly two points
                        shared_points = set(cell._points).intersection(set(other_cell._points))
                        if len(shared_points) == 2:
                            neighbors.append(other_cell)

            elif len(cell.points) == 2:
                for other_cell in self.cells:
                    if other_cell != cell:
                        # Check if they share 1 point if other_cell is a Line og 2 points if other_cell is a Triangle
                        shared_points = set(cell._points).intersection(set(other_cell._points))
                        if len(shared_points) == 1 and len(other_cell.points) == 2 or len(shared_points) == 2 and len(other_cell.points) == 3:
                            neighbors.append(other_cell)
                    
            # Store the neighboring cells for this cell
            cell._neighbors = neighbors



"""    def print_neighbors(self, cell_index: int) -> None:
        cell = next((cell for cell in self.cells if cell.index == cell_index), None)
        if cell:
            print(cell)
        else:
            print(f"Cell {cell_index} does not exist in the mesh.")"""
