from src.Simulation.cells import Cell, Point
from src.Simulation.cells import CellFactory

import meshio
import numpy as np

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
        Finds neighboring cells for the cell specified, neighbors share exactly two points. This also makes it extendable for other
        shapes, since they will always have exactly two sharing points if neighbors.

        Args: cell_index for the cell you want to check

        Returns: A list of neighboring cells
        """
        neighboring_cells = []
        points_in_cell = self._cells[cell_index].points

        # Assuming cells with more points than triangles have are neighbors if they share two points. 
        # This function is extendable for any cell type that meets that criteria
        # Makes a list with the indicies of the neighbors for the specified cell
        neighboring_cells = [cell for cell in self._cells if len(set(points_in_cell) & set(cell.points))]

        # Store neighbors in each cell, stores the neighbors in the cell that was checked
        self._cells[cell_index].neighbors = neighboring_cells