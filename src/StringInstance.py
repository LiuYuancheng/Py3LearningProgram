#!/usr/bin/python
#-----------------------------------------------------------------------------
# Name:        ClosureInstance.py
#
# Purpose:     This module is used to test change the string representation 
#              of instances.
# Author:      Yuancheng Liu
#
# Created:     2021/01/16
# Copyright:    n.a    
# License:      n.a
#-----------------------------------------------------------------------------

import math
from functools import partial
from socket import socket, AF_INET, SOCK_STREAM

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
print(Pair(3, 4))

# Customizing String format:
_formates = {
    'ymd': '{d.year}-{d.month}-{d.day}',
    'mdy': '{d.month}/{d.day}/{d.year}',
    'dmy': '{d.day}\{d.month}\{d.year}'
}

class Date:
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day

    def __format__(self, code):
        fmt = _formates[code] if code in _formates.keys() else _formates['ymd']
        return fmt.format(d=self)

# test Case:
d = Date(2021, 2, 1)
print(format(d))
print(format(d, 'mdy'))
print('The date is {:ymd}'.format(d))
print('The date is {:mdy}'.format(d))

#-----------------------------------------------------------------------------
# Make Obejct support the Context-management protocol

class LazyConnection:
    def __init__(self, addr, family=AF_INET, type=SOCK_STREAM, nestedComm = True):
        self.address = addr
        self.family = family
        self.type = type
        self.nestedComm = nestedComm
        if not self.nestedComm: self.sock = None
        self.connections = [] # used to support nested use of connection.

    def __enter__(self):
        if self.nestedComm:
            sock = socket(self.family, self.type)
            sock.connect(self.address)
            self.connections.append(sock)
            return sock
        else:
            if self.sock is not None:
                raise RuntimeError('Already connected.')
            self.sock = socket(self.family, self.type)
            self.sock.connect(self.address)
            return self.sock
        
    def __exit__(self, exc_ty, exc_val, tb):
        if self.nestedComm:
            self.connections.pop().close()
        else:
            self.sock.close()
            self.sock = None

conn0 = LazyConnection(('www.python.org', 80), nestedComm=False)
with conn0 as s:
    s.send(b'GET /index.html HTTP/1.0\r\n')
    s.send(b'Host: www.python.org\r\n')
    s.send(b'\r\n')
    resp = b''.join(iter(partial(s.recv, 8192), b''))
    print(resp)

conn1 = LazyConnection(('www.python.org', 80), nestedComm=True)
with conn1 as s0:
    s0.send(b'GET /index.html HTTP/1.0\r\n')
    with conn1 as s1:
        s1.send(b'Host: www.python.org\r\n')
        s1.send(b'\r\n')
        resp = b''.join(iter(partial(s1.recv, 8192), b''))
        print(resp)

#-----------------------------------------------------------------------------
# Test add the properity attribute to a class 
class Person:
    def __init__(self, fName):
        self.fName = fName

    @property
    def firstName(self):
        return self.fName

    @firstName.setter
    def firstName(self, val):
        if not isinstance(val, str):
            raise TypeError("Name must be a string")
        self.fName = val

    @firstName.deleter
    def firstName(self):
        raise AttributeError("Can not delete the attribute")

a = Person("Guido")
print(a.firstName)
try:
    a.firstName = 42
except Exception as e:
    print(e)

try:
    del a.firstName
except Exception as e:
    print(e)   

class Circle:
    def __init__(self, radius):
        self.radius = radius

    @property
    def area(self):
        return math.pi * self.radius ** 2
    
    @property
    def perimeter(self):
        return math.pi * self.radius *2

c = Circle(4.0)
print("Area: %s" %str(c.area))
print("Perimeter: %s" %str(c.perimeter))

#-----------------------------------------------------------------------------
# Call a method in on a Parent class

class Base:
    def __init__(self):
        print('Base.__init__ called.')

class Base_A(Base):
    def __init__(self):
        super().__init__()
        print('Base_A.__init__ called.')

class Base_B(Base):
    def __init__(self):
        super().__init__()
        print('Base_B.__init__ called.')

class Base_C(Base_A, Base_B):
    def __init__(self):
        super().__init__()
        print('Base_c.__init__ called.')

print('Test: init the Base_c object: ')
c = Base_C()
print(Base_C.__mro__)

# Call a not exist function in class B from an unrelated class A.
class Spam_A:
    def spam(self):
        print('A.spam called.')
        super().spam()

class Spam_B:
    def spam(self):
        print('B.spam called.')

class Spam_C(Spam_A, Spam_B):
    pass

print('Test: init the Spam_C object: ')
try:
    a = Spam_A()
    a.spam()
except Exception as err: 
    print("Init Spam A got exception: %s" %str(err))

c = Spam_C()
c.spam()

#-----------------------------------------------------------------------------
# extend property in a subclass
class Person_A:
    def __init__(self, name):
        self.name = name
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, val):
        if not isinstance(val, str):
            raise TypeError("Expected a string.")
        self._name = val

    @name.deleter
    def name(self):
        raise AttributeError("Can not deleted the name.")

class SubPerson_A(Person_A):
    @property
    def name(self):
        print('Getting name.')
        return super().name

    @name.setter
    def name(self, val):
        print('Setting name to', val)
        super(SubPerson_A, SubPerson_A).name.__set__(self, val)
    
    @name.deleter
    def name(self):
        print('Delete name')
        super(SubPerson_A, SubPerson_A).name.__delete(self)

s = SubPerson_A("Guido")
print(s.name)
try:
    s.name = 42
except Exception as e:
    print(e)

#-----------------------------------------------------------------------------
# Create a new kind of class or instance attribute
class Integer:
    def __init__(self, name):
        self.name = name
    
    def __get__(self, instance, cls):
        val = self if instance is None else instance.__dict__[self.name]
        return val
    
    def __set__(self, instance, val):
        if not isinstance(val, int):
            raise TypeError("Input must be an int.")
        instance.__dict__[self.name] = val
    
    def __delete__(self, instance):
        del instance.__dict__[self.name]


class Point:
    x = Integer('x')
    y = Integer('y')
    def __init__(self,x, y):
        self.x = x 
        self.y = y

p = Point(2,3)
print("p.x = ", p.x)
print('p.y =', p.y)

p.y = 5 
try:
    p.y = 2.3
except Exception as e:
    print(e)
#-----------------------------------------------------------------------------
class lazyproperty:
    def __init__(self, func):
        self.func = func

    def __get__(self, instance, cls):
        if instance is None:
            return self
        else:
            value = self.func(instance)
            setattr(instance, self.func.__name__, value)
            return value


class CircleL:
    def __init__(self, radius):
        self.radius = radius

    @lazyproperty
    def area(self):
        print("Computing area")
        return math.pi * self.radius ** 2

    @lazyproperty
    def perimeter(self):
        print("Computing the perimeter")
        return 2*math.pi * self.radius

c = CircleL(4.0)
print(c.radius)
print(c.area)
print(c.perimeter)

#-----------------------------------------------------------------------------
# Simplifying the initialization of data structure
class Structure:
    _fields = []
    def __init__(self, *args, **kwargs):
        if len(args) > len(self._fields):
            raise TypeError('Expected {} arguments'.format(len(self._fields)))

        # set all of the positional arguments
        for name, value in zip(self._fields, args):
            setattr(self, name, value)

        # set the remaining keyword arguments
        for name in self._fields[len(args):]:
            setattr(self, name, kwargs.pop(name))
        
        # Check for any remaining unknown arguments
        if kwargs:
            raise TypeError('Invalid argumens(s):{}'.format(','.join(kwargs)))

class Stock(Structure):
    _fields = ['name', 'shares', 'price']

s1 = Stock('ACME', 50, 91.1)
s2 = Stock('ACME', 50, price=91.1)
s3 = Stock('ACME', shares=50, price=91.1)
#help(Stock)

#-----------------------------------------------------------------------------
# YAML file test
# pip install pyyaml 
import yaml

#stream = open("yamlTest.yaml", 'r')
#dictionary = yaml.load(stream)
#for key, value in dictionary.items():
#    print (key + " : " + str(value))

stream = open("yamlTest.yaml", 'r')
dictionary = yaml.load_all(stream)

for doc in dictionary:
    print("New document:")
    for key, value in doc.items():
        print(key + " : " + str(value))
        if type(value) is list:
            print(str(len(value)))















    










