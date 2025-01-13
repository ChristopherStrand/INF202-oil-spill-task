import classes as cls

mesh = cls.Mesh("meshes/bay.msh")
for cells_with_oil in oil_cells:
    if cells_with_oil.oil_amount == 0:
        continue
    else:
        pass