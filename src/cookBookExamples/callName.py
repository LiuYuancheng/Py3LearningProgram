# this module is used for test call a method in an object give the name as a string

import math

# 1 use function getattr()
class Point:

    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return 'Point({!r:}, {!r:})'.format(self.x, self.y)

    def distance(self, x, y):
        return math.hypot(self.x-x, self.y-y)


p = Point(2, 3)
d = getattr(p, 'distance')(0, 0)
print(d)

# 2 use function operator
import operator

d = operator.methodcaller('distance', 0, 0)(p)
print(d)

points = [
    Point(1,2), 
    Point(2,3),
    Point(5,6)
]

points.sort(key=operator.methodcaller('distance', 0, 0))

print(points)