import meshio
import classes
import numpy as np

mesh = classes.Mesh("meshes/bay.msh")
x = np.array(mesh._cells)
# print(x.dtype)
# print(x[x.dtype == classes.Triangle])
mesh.find_neighbors()
mesh.print_neighbors(4)