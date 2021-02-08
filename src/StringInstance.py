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

from functools import partial
from socket import socket, AF_INET, SOCK_STREAM
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
p = Pair(3, 4)
print(p)

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









