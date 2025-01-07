import meshio
import classes

mesh = classes.Mesh("meshes/bay.msh")
mesh.find_neighbors()
mesh.print_neighbors(4)