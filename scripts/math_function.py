"""
This file contains the mathmatical functions used in main.py
"""
import numpy as np
import numpy.typing as npt

x_star = (0.35, 0.45) #Should we transpose? Always this value??? Intial start position

#Index 0 represents x value in the position vector x, and index 1 represents the y value in the position vector x

#Same as function u from task description. Should not return a vector
def oil_distro(t: float, x_n: npt.NDArray[np.float32]) -> np.float32: 
    return np.e**(-(((x_n[0]-x_star[0])**2+(x_n[1]-x_star[1])**2)/(0.01)))

#Same as function v from task description. Should return a vector
def velocity(x_n: npt.NDArray[np.float32]) -> npt.NDArray[np.float32]: 
    return (x_n[1]-0.2*[x_n[0]], -x_n[0])

#Same as X_mid from task description. Should return a vector
def midpoint(coordinates: npt.NDArray[np.float32]) -> npt.NDArray[np.float32]:
    return (1/3)*(coordinates[0]+coordinates[1]+coordinates[2])

def unit_normal_vector(coordinates: npt.NDArray[np.float32]) -> npt.NDArray[np.float32]:

""" def area() -> np.float32:
    return 0.5*abs(()) """

def calculate_area(points: list) -> float:
    x0, y0 = points[0]
    x1, y1 = points[1]
    x2, y2 = points[2]
    
    return 0.5 * abs((x0 - x2)*(y1 - y0) - (x0 - x1)*(y2 - y0))

def g(a , b , v, w):
    dot_product = np.dot(v, w)
    
    if dot_product > 0 :
        return a * dot_product
    else:
        return b * dot_product


# calculating the change of oil in cell
def calculate_change(cell: object, neighbors: list[int]) -> int: 
    #kan bli et problem å hente ut punktene, sjekke getter for celle og str metode for point
    area = calculate_area( cell.points)
    sum = 0
    for neighbor in cell.neighbors:
        mid = midpoint(cell.points)
        v_mid = velocity(mid)
    
    
    
    
def calculate_flux(oil_amount, neighbours_oil_amount , A):
    nv = unit_normal_vector(cell.points)
    v
    F = -dt/A * g(oil_amount, neighbours_oil_amount, v_mid, nv)
    

    
    

    
    
    

