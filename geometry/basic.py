from math import *

# vec-mult of two vectors
# The area of the parallelogram
# negative for clockwise turn, and zero if the points are collinear.
def cross(a, b):
    return a[0]*b[1] - a[1]*b[0]

# equals |a|*|b|*cos(alf)
def dot(a, b):
    return a[0]*b[1] + a[1]*b[0]

def angle(a, b):
    return acos(dot(a, b)/hypot(*a)/hypot(*b))

# perpendicular vector of unit length
def normal(a):
    h = hypot(*a)
    return [-a[1]/h, a[0]/h]

def area_regular_polygon(n, s):
    return 0.25 * n * s**2 / tan(pi/n)

def area_polygon(vx):
    return abs(sum(cross(vx[i-1], vx[i]) for i in range(len(vx)))) / 2
