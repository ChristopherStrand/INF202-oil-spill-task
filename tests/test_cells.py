import sys
import os
import meshio
import numpy as np

# Add the scripts directory to the system path #This is temporary please remove when importing is fixed
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'scripts')))

from classes import Mesh


mesh_path = "meshes/bay.msh"


mesh = Mesh(mesh_path)
test = meshio.read(mesh_path)  # Reads the meshfile

def test_attribute_index():
    assert mesh.cells[4].index == 4, "The assignment of indices in cells is off"

if __name__=="__main__":
    pass