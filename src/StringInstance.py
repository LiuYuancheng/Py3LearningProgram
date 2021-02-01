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

# test case:
p = Pair(3,4)
print(p)


# Customizing String format:
_formates = {
    'ymd':'{d.year}-{d.month}-{d.day}',
    'mdy':'{d.month}/{d.day}/{d.year}',
    'dmy':'{d.day}\{d.month}\{d.year}'
}

class Date:
    def __init__(self, year , month, day):
        self.year = year
        self.month = month
        self.day = day

    def __format__(self, code):
        fmt = _formates[code] if code in _formates.keys() else _formates['ymd']
        return fmt.format(d = self)

# test Case: 
d = Date(2021, 2, 1)
print(format(d))
print(format(d, 'mdy'))
print('The date is {:ymd}'.format(d))
print('The date is {:mdy}'.format(d))




