#!/usr/bin/python
#-----------------------------------------------------------------------------
# Name:        ClosureInstance.py
#
# Purpose:     This module is used to test accessing variables defined inside
#              a closure
# Author:      Yuancheng Liu
#
# Created:     2020/10/2
# Copyright:
# License:
#-----------------------------------------------------------------------------
import sys
from timeit import timeit

class ClosureInstance:
    def __init__(self, locals=None):
        if locals is None:
            locals = sys._getframe(1).f_locals

        self.__dict__.update((key, value)
                             for key, value in locals.items() if callable(value))

    def __len__(self):
        return self.__dict__['__len__']()


def Stack1():
    items = []

    def push(item):
        items.append(item)

    def pop():
        return items.pop()

    def __len__():
        return len(items)

    return ClosureInstance()

class Stack2:

    def __init__(self):
        self.items = []
    
    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def __len__(self):
        return len(self.items)


s1 = Stack1()
print(timeit('s1.push(1);s1.pop()', 'from __main__ import s1'))
s2 = Stack2()
print(timeit('s2.push(1);s2.pop()', 'from __main__ import s2'))
