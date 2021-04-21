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
import bisect
import collections
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
#-----------------------------------------------------------------------------
# Another decorator test from the StringInstance.py file

# Base class, use a descriptor to set a val


class Descriptor:
    def __init__(self, name=None, **opts):
        self.name = name
        for key, value in opts.items():
            setattr(self, key, value)

    def __set__(self, instance, value):
        instance.__dict__[self.name] = value


def Typed(expected_type, cls=None):
    if cls is None:
        return lambda cls: Typed(expected_type, cls)

    super_set = cls.__set__

    def __set__(self, instance, value):
        if not isinstance(value, expected_type):
            raise TypeError('Expect %s' % str(expected_type))
        super_set(self, instance, value)

    cls.__set__ = __set__

    return cls


def Unsigned(cls):
    super_set = cls.__set__

    def __set__(self, instance, value):
        if value < 0:
            raise ValueError('Expect > 0')
        super_set(self, instance, value)

    cls.__set__ = __set__
    return cls


def MaxSized(cls):
    super_init = cls.__init__

    def __init__(self, name=None, **opts):
        if 'size' not in opts:
            raise ValueError('Expect > 0')
        super_init(self, name, **opts)
    cls.__init__ = __init__

    super_set = cls.__set__

    def __set__(self, instance, value):
        if len(value) > self.size:
            raise ValueError('Expect > 0')
        super_set(self, instance, value)

    cls.__set__ = __set__
    return cls


@Typed(int)
class Integer(Descriptor):
    pass


@Unsigned
class UnsignedInteger(Integer):
    pass


@Typed(float)
class Float(Descriptor):
    pass


@Unsigned
class UnsignedFloat(Float):
    pass


@Typed(str)
class String(Descriptor):
    pass


@MaxSized
class SizedString(String):
    pass


class Stock2:
    name = SizedString('name', size=8)
    shares = UnsignedInteger('shares')
    price = UnsignedFloat('price')

    def __init__(self, name, shares, price):
        self.name = name
        self.shares = shares
        self.price = price


print('Run:')
s = Stock2('ACME2', 50, 91.1)
print(s.name)
print(s.shares)
print(s.price)

#-----------------------------------------------------------------------------
# implement ineration by using the


class SortedItem(collections.Sequence):
    def __init__(self, initial=None):
        self._item = sorted(initial)

    def __getitem__(self, idx):
        return self._item[idx]

    def __len__(self):
        return len(self._item)

    def add(self, item):
        bisect.insort(self._item, item)


items = SortedItem([5, 1, 3])
print(list(items))
items.add(2)
print(list(items))
print(len(items))
print(items[-1])


class Items(collections.MutableSequence):
    def __init__(self, initial=None):
        self._items = list(initial)

    def __getitem__(self, idx):
        print('Geting:', idx)
        return self._items[idx]

    def __setitem__(self, idx, val):
        print('Setting:', idx, val)
        self._items[idx] = val

    def __delitem__(self, idx):
        print('Deleting:', idx)
        del self._items[idx]

    def insert(self, idx, val):
        print('Inserting:', idx, val)
        self._items.insert(idx, val)

    def __len__(self):
        print('Len:')
        return len(self._items)

a = Items([1, 2, 3])
print(len(a))
a.append(4)
a.count(2)
a.remove(3)
