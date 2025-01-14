import sys
import os
import meshio

# Add the scripts directory to the system path #This is temporary please remove when importing is fixed
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'scripts')))

from classes import Mesh, Cell, Point


mesh_path = "meshes/bay.msh"


mesh = Mesh(mesh_path)
test = meshio.read(mesh_path)  # Reads the meshfile
def test_cells_init():
    """
    Checks if Mesh object has the same amount of cells as the mesh
    """
    cells_in_mesh = sum([len(cell_types) for cell_types in test.cells if cell_types.type != "vertex" and cell_types.type != "line"])
    assert cells_in_mesh == len(mesh.cells), "Amount of cells in intialized is not equal to amount cells in mesh"

def test_points_init():
    """
    Checks if Mesh object has the same amount of points as the mesh
    """
    assert len(test.points) == len(mesh.points), "The amount of points in the Mesh class differs from the amount in mesh file"

def test_find_neighbors():
    """
    Tests cell 4 for already known neighbors
    """
    mesh.calculate(4)    
    assert [ngh.index for ngh in mesh.cells[4].neighbors] == [45, 46, 2056], "The neighbors aren't correct"

def test_getter_cells():
    """
    Tests the getter for the list of cells from mesh
    """
    cells_in_mesh = sum([len(cell_types) for cell_types in test.cells if cell_types.type != "vertex" and cell_types.type != "line"])
    assert [isinstance(cell, Cell) for cell in mesh.cells] and cells_in_mesh == len(mesh.cells), "The cells getter from the mesh class is not functioning correctly"

def test_getter_points():
    """
    Tests the getter for the list of points from mesh
    """
    assert [isinstance(point, Point) for point in mesh.points] and len(test.points) == len(mesh.points), "The points getter from the mesh class is not functioning correctly"

if __name__=="__main__":
    test_find_neighbors()