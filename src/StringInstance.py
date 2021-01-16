#!/usr/bin/python
#-----------------------------------------------------------------------------
# Name:        ClosureInstance.py
#
# Purpose:     This module is used to test change the string representation 
#              of instances.
# Author:      Yuancheng Liu
#
# Created:     2021/01/16
# Copyright:
# License:
#-----------------------------------------------------------------------------

class Pair:
    def __init__(self, x, y):
        self.x = x 
        self.y = y
    
    def __repr__(self):
        #{0.x} specified the x-attribute of argu 0.  {0.x} = self.x
        # !r formatting code indicated that the output of __repr__() should be used.
        return 'Pair({0.x!r}, {0.y!r})'.format(self)

    def __str__(self):
        return '({0.x!r}, {0.y!r})'.format(self)

p = Pair(3,4)
p
print(p)
