import sys
import os
import meshio
import numpy as np

# Add the scripts directory to the system path #This is temporary please remove when importing is fixed
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'scripts')))

from math_function import * 

#Uses cell for testing
def test_velocity():
    x = velocity()
    y = "calculated_by_hand"
    assert x == y

test_velocity()