import sys
import os
import meshio
import numpy as np

# Add the scripts directory to the system path #This is temporary please remove when importing is fixed
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'scripts')))

from math_function import * 
from classes import Triangle, Point

p1 = Point(20, 2.657, 2.20)
p2 = Point(25, 3.023, 7.39)
p3 = Point(15, 10, 2.01)

my_points = [p1, p2, p3]

example_cell = Triangle(4, my_points) 

"""
Tests use a cell defined in this file to test functions. This makes test more reliable and allows test to function any kind of mesh
"""

tolerance = 0.000001 #Uses tolerance to test whether x and y are about equal only for float numbers
def test_midpoint():
    x = example_cell.midpoint
    y = np.float32([5.22666667, 3.86666667]) #Calculated by hand for example cell
    assert np.all(np.less(x-y, tolerance)), "Midpoint function is not calculating correctly"

def test_velocity():
    x = example_cell._velocity(4)
    y = np.float32([2.8213333333333326 , -5.226666666666667]) #Calculated by hand for example cell
    print(x, y)
    assert np.all(np.less(x-y, tolerance)), "Velocity function is not calculating correctly"

def test_calculate_area():
    x = example_cell.area
    y = 19.089855 #Calculated by hand for example cell
    assert (x-y) < tolerance

if __name__=="__main__":
    test_velocity()