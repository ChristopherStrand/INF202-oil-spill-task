import classes as cls
import time

mesh = cls.Mesh("meshes/bay.msh")
# for cells_with_oil in oil_cells:
#     if cells_with_oil.oil_amount == 0:
#         continue
#     else:
#         pass


def calculate_time(func):   
    # added arguments inside the inner1,
    # if function takes any arguments,
    # can be added like this.
    def inner1(*args, **kwargs):

        # storing time before function execution
        begin = time.time()
        
        func(*args, **kwargs)

        # storing time after function execution
        end = time.time()
        print(f"Total time taken in : {func.__name__} {end - begin:.6f}")
    return inner1

@calculate_time
def mjau():
    for cell in mesh.cells[4:5]:
        mesh.calculate(cell.index)
        print(cell)

mjau()