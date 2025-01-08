import meshio
import classes
import numpy as np

#temp function
def indexify(point_list):
    return [i.index for i in point_list]

mesh = classes.Mesh("meshes/bay.msh")
# x = np.array(mesh._cells)
# print(x.dtype)
# print(x[x.dtype == classes.Triangle])
cells = mesh._cells
print(f"2056: {indexify(cells[2056].points)}, 45: {indexify(cells[45].points)}, 46: {indexify(cells[46].points)}")
mesh.find_neighbors(4)
mesh.print_neighbors(4)

mesh.find_neighbors(5)
mesh.print_neighbors(5)

