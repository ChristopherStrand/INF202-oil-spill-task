import src.Simulation.cells as cls
import src.Simulation.mesh as msh
import numpy as np
import pytest

@pytest.fixture
def mesh():
    factory = msh.CellFactory()
    factory.register(1, cls.Vertex)
    factory.register(2, cls.Line)
    factory.register(3, cls.Triangle)
    return msh.Mesh("tests\simple.msh", factory)

@pytest.fixture
def cells(mesh):
    return mesh.cells


# Tests for mesh getters/setters
def test_get_cells(mesh):
    assert np.all(np.array([issubclass(type(cell), cls.Cell) for cell in mesh.cells])), "Mesh cells getter is not returning the correct values"

def test_get_points(mesh):
    assert np.all(np.array([issubclass(type(point), cls.Point) for point in mesh.points])), "Mesh points getter is not returning the correct values"

# Tests for cell getters/setters
def test_get_points(cells):
    for cell in cells:
        if np.all(np.array([issubclass(type(point), cls.Point) for point in cell.points])) == True:
            continue
        else:
            assert False, "Cell points getter is not returning the correct values"
    assert True

def test_get_coordinates(cells):
    for cell in cells:
        if np.all(np.array([True for coordinates in cell.coordinates if coordinates.size == 2])) == True:
            continue
        else:
            assert False, "Cell coordinates getter is not returning the correct values"
    assert True

def test_get_index(cells):
    for index, cell in enumerate(cells):
        if cell.index == index:
            continue
        else:
            assert False, "Cell index getter is not returning the correct values"
    assert True

def test_get_and_set_neighbors(cells):
    cells[0].neighbors = [cells[1], cells[2], cells[3]]
    assert cells[0].neighbors == [cells[1], cells[2], cells[3]], "Cell getter and setter for neighbors is not working correctly"

def test_get_and_set_velocity(cells):
    cells[0].velocity = np.array([0.2, 0.2])
    assert np.all(np.equal(np.array([0.2, 0.2]), cells[0].velocity)), "Cell getter and setter for velocity is not working correctly"

def test_get_and_set_midpoint(cells):
    cells[0].midpoint = np.array([0.2, 0.2])
    assert np.all(np.equal(np.array([0.2, 0.2]), cells[0].midpoint)), "Cell getter and setter for midpoint is not working correctly"

def test_get_and_set_scaled_normal(cells):
    cells[0].scaled_normal = np.array([0.2, 0.2])
    assert np.all(np.equal(np.array([0.2, 0.2]), cells[0].scaled_normal)), "Cell getter and setter for scaled normal is not working correctly"

def test_get_and_set_area(cells):
    cells[0].area = 0.2
    assert cells[0].area - 0.2 < 0.0001, "Cell getter and setter for area is not working correctly"

def test_get_and_set_oil_amount(cells):
    cells[0].oil_amount = 0.2
    assert cells[0].oil_amount - 0.2 < 0.0001, "Cell getter and setter for oil amount is not working correctly"

def test_get_and_set_oil_change(cells):
    cells[0].oil_change = 0.2
    assert cells[0].oil_change - 0.2 < 0.0001, "Cell getter and setter for oil change is not working correctly"