#-----------------------------------------------------------------------------
# Calling a method on an Object Given the Name as a String

import math

class Point:
    def __init__(self, x, y):
        self.x = x 
        self.y = y

    def __repr__(self):
        return 'Point({!r}, {!r})'.format(self.x, self.y)

    def distance(self, x, y):
        return math.hypot(self.x-x, self.y-y)

pt = Point(2,3)
dist = getattr(pt, 'distance')(0, 0)
print(dist)

import operator
print(operator.methodcaller('distance', 0, 0)(pt))

points = [
    Point(1,2),
    Point(3,4),
    Point(5,6),
    Point(7,8),
]

points.sort(key=operator.methodcaller('distance', 0, 0))
print(points)



