import meshio
import classes
import numpy as np
import time

#temp function
def indexify(point_list):
    return [i.index for i in point_list]

mesh = classes.Mesh("meshes/bay.msh")
# x = np.array(mesh._cells)
# print(x.dtype)
# print(x[x.dtype == classes.Triangle])
# cells = mesh._cells
#print(f"2056: {indexify(cells[2056].points)}, 45: {indexify(cells[45].points)}, 46: {indexify(cells[46].points)}")

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
def løk():
    for i in range(0, 500):
        mesh.find_neighbors(i)
        #mesh.print_neighbors(i)

løk()


