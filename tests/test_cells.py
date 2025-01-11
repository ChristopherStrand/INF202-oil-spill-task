import sys
import os
import meshio
import numpy as np

# Add the scripts directory to the system path #This is temporary please remove when importing is fixed
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'scripts')))

from classes import Triangle, Point

p1 = Point(20, 2.657, 2.20)
p2 = Point(25, 3.023, 7.39)
p3 = Point(15, 10, 2.01)

my_points = [p1, p2, p3]

example_cell = Triangle(4, my_points) 
tolerance = 0.000001 #Uses tolerance to test whether x and y are about equal only for float numbers

def test_getter_index():
    assert example_cell.index == 4, "The assignment of indices in cells is off"

def test_getter_coordinates():
    x = np.array(example_cell.coordinates)-np.array([[2.657, 2.2], [3.023, 7.39 ], [10.  ,  2.01]])
    assert np.all(np.less(x, tolerance))

def test_getter_points():
    assert len(example_cell.points) == 3 and [isinstance(point, Point) for point in example_cell.points]

def test_oil_amount():
    example_cell.oil_amount = 20
    assert example_cell.oil_amount == 20

def test_neighbors():
    example_cell.neighbors = [23, 31, 2] #Randomly choosen numbers
    assert example_cell.neighbors == [23, 31, 2]

if __name__=="__main__":
    print(example_cell.coordinates)