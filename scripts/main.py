import meshio

msh = meshio.read("../meshes/bay.msh")

points = msh.points
cells = msh.cells
print(points)
print(cells)
