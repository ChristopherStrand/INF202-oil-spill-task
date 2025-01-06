import numpy as np
import numpy.typing as npt

x_star = (0.35, 0.45) #Should we transpose? Always this value??? Intial start position

#Index 0 represents x value in the position vector x, and index 1 represents the y value in the position vector x
def oil_distro(t: float, x_n: npt.NDArray[np.float32]) -> np.float32:
    return np.e**(-(((x_n[0]-x_star[0])**2+(x_n[1]-x_star[1])**2)/(0.01)))

def velocity(x_n: npt.NDArray[np.float32]) -> npt.NDArray[np.float32]:
    return (x_n[1]-0.2*[x_n[0]], -x_n[0])

def midpoint(coordinates: npt.NDArray[np.float32]) -> npt.NDArray[np.float32]:
    return (1/3)*(coordinates[0]+coordinates[1]+coordinates[2])

""" def area() -> np.float32:
    return 0.5*abs(()) """

def calculate_area(points: list) -> float:
    x0, y0 = points[0].x, points[0].y
    x1, y1 = points[1].x, points[1].y
    x2, y2 = points[2].x, points[2].y
    
    return 0.5 * abs((x0 - x2)*(y1 - y0) - (x0 - x1)*(y2 - y0))


# calculating the change of oil in cell
def calculate_change(cell: object, neighbors: list[int]) -> int: 
    #kan bli et problem å hente ut punktene, sjekke getter for celle og str metode for point
    points = cell.points
    print(points)
    area = calculate_area(points)
    
    sum = 0
    for neighbor in neighbors:
        sum += 
    
    
    
    
def calculate_flux( , A):
    F = -dt/A 
    
def g(a , b , v, w):
    if 
    
    

    
    
    
    
  
