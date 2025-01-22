import src.Simulation.cells as cls
import src.Simulation.mesh as msh
import numpy as np
import pytest
import meshio


@pytest.fixture
def factory():
    factory = msh.CellFactory()
    factory.register(1, cls.Vertex)
    factory.register(2, cls.Line)
    factory.register(3, cls.Triangle)
    return factory


@pytest.fixture
def mesh_meshio():
    return meshio.read("meshes\simple.msh")


@pytest.fixture
def mesh_class(factory):
    return msh.Mesh("meshes\simple.msh", factory)


@pytest.fixture
def cells_in_raw_mesh(mesh_meshio):
    raw_cells = []
    for cell_types in mesh_meshio.cells:    
        raw_cells.extend([cell for cell in cell_types.data])
    return raw_cells


# Tests for cell factory
@pytest.mark.parametrize("amount_of_points, class_type",
                         [(1, cls.Vertex),
                          (2, cls.Line),
                          (3, cls.Triangle)])
def test_register_class_type_CellFactory(amount_of_points, class_type):
    test_factory = msh.CellFactory()
    test_factory.register(amount_of_points, class_type)
    assert list(test_factory._cell_types.values())[0] == class_type


@pytest.mark.parametrize("amount_of_points, class_type",
                         [(1, cls.Vertex),
                          (2, cls.Line),
                          (3, cls.Triangle)])
def test_register_amount_of_points_CellFactory(amount_of_points, class_type):
    test_factory = msh.CellFactory()
    test_factory.register(amount_of_points, class_type)
    assert list(test_factory._cell_types.keys())[0] == amount_of_points


@pytest.mark.parametrize("cell",
                         [np.array([0]),
                          np.array([2, 11, 12]),
                          np.array([76, 90])])
def test_cellFactory_call(mesh_class, cell, factory):
    initalized_cell = factory(cell, mesh_class.points)
    assert len(initalized_cell.points) == len(cell)


# Tests for intializing of cells
def test_amount_cells_initalized(mesh_class, cells_in_raw_mesh):   
    assert len(mesh_class.cells) == len(cells_in_raw_mesh), "The amount of cells initalized is different from the amount in the mesh"


def test_type_cells_initalized(cells_in_raw_mesh, mesh_class):
    for index, element in enumerate(cells_in_raw_mesh):
        if len(cells_in_raw_mesh[index]) == len(mesh_class.cells[index].points):
            continue
        else:
            assert False, "The types of the cells intialized dosen't match with the mesh"
    assert True


# Tests for mathematical functions
@pytest.mark.parametrize("midpoint, cell_index",
                         [([-0.24662323, 0.3080236], 300),
                          ([0.42458427, -0.11909357], 487)
                          ])
def test_midpoint(mesh_class, midpoint, cell_index):
    current_cell = mesh_class.cells[cell_index]
    mesh_class.calculate(current_cell)
    assert np.all(np.less(midpoint - current_cell.midpoint, 0.00001))


@pytest.mark.parametrize("velocity, cell_index",
                         [([0.35734824, 0.24662323], 300),
                          ([-0.20401043, -0.42458427], 487)
                          ])
def test_velocity(mesh_class, velocity, cell_index):
    current_cell = mesh_class.cells[cell_index]
    mesh_class.calculate(current_cell)
    assert np.all(np.less(velocity - current_cell.velocity, 0.00001)), "The velocity is incorrect"


@pytest.mark.parametrize("scaled_normal, cell_index, iteration",
                         [([0.11379205, -0.00164448], 300, 0),
                          ([-0.07882403, -0.08290938], 300, 1),
                          ([-0.03496802,  0.08455385], 300, 2),
                          ([-0.0589084, 0.04355666], 487, 0),
                          ([-0.01001778, -0.0749698], 487, 1),
                          ([0.06892618, 0.03141314], 487, 2)
                          ])
def test_scaled_normal(mesh_class, scaled_normal, cell_index, iteration):
    current_cell = mesh_class.cells[cell_index]
    mesh_class.calculate(current_cell)
    assert np.all(np.less(scaled_normal - current_cell.scaled_normal[iteration], 0.00001)), "The scaled normals are incorrect"


@pytest.mark.parametrize("area, cell_index",
                         [(0.0047820257022976875, 300),
                          (0.002426345832645893, 487)
                          ])
def test_area(mesh_class, area, cell_index):
    current_cell = mesh_class.cells[cell_index]
    mesh_class.calculate(current_cell)
    assert np.all(np.less(area - current_cell.area, 0.00001)), "The area is incorrect"


@pytest.mark.parametrize("ngh, cell_index",
                         [([279, 384, 451], 300),
                          ([383, 407, 486], 487)
                          ])
def test_neighbors(mesh_class, ngh, cell_index):
    current_cell = mesh_class.cells[cell_index]
    mesh_class.calculate(current_cell)
    assert [ngh.index for ngh in current_cell.neighbors] == ngh, "The area is incorrect"


# Tests for callable functions in mesh
@pytest.mark.parametrize("intial_oil, cell_index",
                         [(0.006737946999085461, 300),
                          (0.006737946999085461, 487)
                          ])
def test_intial_oil(mesh_class, intial_oil,cell_index):
    mesh_class.initial_oil_distribution(np.array([0.1, 0.2]))
    current_cell = mesh_class.cells[cell_index]
    assert np.all(np.less(intial_oil - current_cell.oil_amount, 0.00001))


@pytest.mark.parametrize("oil_change, cell_index",
                         [(0.0, 300),
                          (0.0, 487)
                          ])
def test_calculate_change(mesh_class, oil_change, cell_index):
    mesh_class.initial_oil_distribution(np.array([0, 0]))
    current_cell = mesh_class.cells[cell_index]
    mesh_class.calculate_change(current_cell, 0.1)
    assert np.all(np.less(oil_change - current_cell.oil_change, 0.00001))