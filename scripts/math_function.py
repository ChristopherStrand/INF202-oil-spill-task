"""
This file contains the mathmatical functions used in main.py
"""
import math

def oil_amount(x:float, y:float):
    x = list(x, y)
    x_star = x.T
    return math.exp ** (-abs(x - x_star)**2 / 0.01)

def oil_velocity(x:float, y:float):
    x = list(x, y)
    v = list(y - 0.2*x, -x)
    return v


    