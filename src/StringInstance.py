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

import io
from abc import ABCMeta, abstractmethod
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

# read a yaml file
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

# Write a yaml file
dict_file = [{'sports' : ['soccer', 'football', 'basketball', 'cricket', 'hockey', 'table tennis']},
{'countries' : ['Pakistan', 'USA', 'India', 'China', 'Germany', 'France', 'Spain']}]

with open('write.yaml', 'w') as file:
    documents = yaml.dump(dict_file, file)


#-----------------------------------------------------------------------------
# python Abstract Base Class : abc
print("python Abstract Base Class : abc ")


class IStream(metaclass=ABCMeta):
    @abstractmethod
    def read(self, maxbytes=-1):
        pass

    @abstractmethod
    def write(self, data):
        pass
# Register the built-in I/O ckass as supporting a interface


IStream.register(io.IOBase)

f = open('write.yaml')
print(isinstance(f, IStream))

#-----------------------------------------------------------------------------
# Implement a data model or Type system


class Descriptor:
    def __init__(self, name=None, **opts):
        self.name = name
        for key, value in opts.items():
            setattr(self, key, value)

    def __set__(self, instance, value):
        instance.__dict__[self.name] = value


class Typed(Descriptor):
    expect_type = type(None)

    def __set__(self, instance, value):
        if not isinstance(value, self.expect_type):
            raise TypeError('Expected %s' % str(self.expect_type))
        super().__set__(instance, value)


class Unsigned(Descriptor):
    def __set__(self, instance, value):
        if value < 0:
            raise ValueError('Expect >= 0')
        super().__set__(instance, value)


class MaxSized(Descriptor):
    def __init__(self, name=None, **opts):
        if not 'size' in opts:
            raise TypeError('Missing the expected size option.')
        super().__init__(name, **opts)

    def __set__(self, instance, value):
        if len(value) >= self.size:
            raise ValueError('size must be < %s' % str(self.size))
        super().__set__(instance, value)


class IntegerI(Typed):
    expect_type = int


class UnsignedInteger(IntegerI, Unsigned):
    pass


class Float(Typed):
    expect_type = float


class UnsignedFloat(Float, Unsigned):
    pass


class String(Typed):
    expect_type = str


class SizedString(String, MaxSized):
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

def check_attibutes(** kwargs):
    def decorate(cls):
        for key, value in kwargs.items():
            if isinstance(value, Descriptor):
                value.name = key
                setattr(cls, key, value)
            else:
                setattr(cls, key, value(key))
        return cls
    return decorate

# use a class dacorator
@check_attibutes(   name = SizedString(size=8),
                    shares= UnsignedInteger,
                    price = UnsignedFloat )

class Stock3:
    def __init__(self, name, shares, price):
        self.name = name
        self.shares = shares
        self.price = price 

s = Stock3('ACME3', 50, 91.1)
print(s.name)
print(s.shares)
print(s.price)

# use a meta class 
class checkmeta(type):
    def __new__(cls, clsname, bases, methods):
        for key, value in methods.items():
            if isinstance(value, Descriptor):
                value.name = key
        return type.__new__(cls, clsname, bases, methods)

class Stock4(metaclass = checkmeta):
    name = SizedString(size=8)
    shares= UnsignedInteger,
    price = UnsignedFloat
    def __init__(self, name, shares, price):
        self.name = name
        self.shares = shares
        self.price = price 

s = Stock4('ACME4', 50, 91.1)
print(s.name)
print(s.shares)
print(s.price)

#-----------------------------------------------------------------------------
# define more than on constructor in a class 
import time 
class Data:
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day
    
    @classmethod # the method will return the class
    def today(cls):
        t =time.localtime()
        return cls(t.tm_year, t.tm_mon, t.tm_mday)

a = Data(2021, 4, 22)
print(a.__dict__.items())
b = Data.today()
print(b.__dict__.items())

#-----------------------------------------------------------------------------
# Create an instance without call the __init__ funciton.
c = Date.__new__(Date)
for key, val in b.__dict__.items():
    setattr(c, key, val)
print(c.__dict__.items())

#-----------------------------------------------------------------------------
# Implementing stateful objects or state machine. 
class ConnectionState:
    @staticmethod
    def read(conn):
        raise NotImplementedError()
    
    @staticmethod
    def write(conn):
        raise NotImplementedError()

    @staticmethod
    def open(conn):
        raise NotImplementedError()

    @staticmethod
    def close(conn):
        raise NotImplementedError()

class ClosedConnectionState(ConnectionState):
    @staticmethod
    def read(conn):
        raise RuntimeError('Closed')

    @staticmethod
    def write(conn):
        raise RuntimeError('Closed')

    @staticmethod
    def open(conn):
        conn.new_state(OpenConnectionState)

    @staticmethod
    def close(conn):
        raise RuntimeError('Already Closed')
    
class OpenConnectionState(ConnectionState):
    
    @staticmethod
    def read(conn):
        print('read')

    @staticmethod
    def write(conn):
        print('Closed')

    @staticmethod
    def open(conn):
        raise RuntimeError('Already Opened')
   
    @staticmethod
    def close(conn):
        conn.new_state(ClosedConnectionState)

class Connection:
    def __init__(self):
        self.new_state(ClosedConnectionState)

    def new_state(self, newState):
        self._state = newState

    def read(self):
        return self._state.read(self)

    def write(self):
        return self._state.write(self)
    
    def open(self):
        return self._state.open(self)

    def close(self):
        return self._state.close(self)

conn = Connection()
print(conn._state)

conn.open()
print(conn._state)

conn.read()
print(conn._state)

conn.write()
print(conn._state)

conn.close()
print(conn._state)    

#-----------------------------------------------------------------------------
#
