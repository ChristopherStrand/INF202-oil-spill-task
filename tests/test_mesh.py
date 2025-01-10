import sys
import os
import meshio

# Add the scripts directory to the system path #This is temporary please remove when importing is fixed
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'scripts')))

from classes import Mesh


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
    assert len(test.points) == len(mesh.points)

def test_find_neighbors():
    """
    Tests cell 4 for already known neighbors
    """
    mesh.find_neighbors(4)
    assert mesh.cells[4].neighbors == [45, 46, 2056]

if __name__=="__main__":
    test_find_neighbors()