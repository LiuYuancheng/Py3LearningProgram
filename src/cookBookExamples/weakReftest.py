# this module is use for testing the section 8.23 week reference secttion

import weakref

class Node:
    def __init__(self, value):
        self.val = value
        self._parent = None
        self.children = []

    def __repr__(self) -> str:
        return 'Node({!r:})'.format(self.val)

    def parent(self):
        return self._parent
        #return self._parent if self._parent is None else self._parent

    def addParent(self, node):
        self._parent = weakref.ref(node)
    
    def addChildren(self, child):
        self.children.append(child)
        child.addParent(self)
        

root = Node('parent')
c1 = Node('child1')
root.addChildren(c1)
print('Before remove the parent, c1\'s parent is:')
print(c1.parent)
del root
print('After remove the parent, c1\'s week ref parent is:')
print(c1.parent)


