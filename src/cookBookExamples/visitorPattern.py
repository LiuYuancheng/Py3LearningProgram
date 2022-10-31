# this module is use for testing the section 8.21 and 8.22 implement 
# the visitor pattern
import types

from numpy import isin

class Node:
    pass

class Number(Node):
    def __init__(self, value) -> None:
        super().__init__()
        self.value = value

class BinaryOperator(Node):
    def __init__(self, left, right) -> None:
        super().__init__()
        self.left = left
        self.right = right

class Add(BinaryOperator):
    pass


class Sub(BinaryOperator):
    pass


class Mul(BinaryOperator):
    pass


class Div(BinaryOperator):
    pass

class UnaryOpertor(Node):

    def __init__(self, operand) -> None:
        super().__init__()
        self.operand = operand

class Negate(UnaryOpertor):
    pass

class NodeVisitor:
    
    def _visit(self, node):
        methname = 'visit' + type(node).__name__
        meth = getattr(self, methname, None) # use this to ge the method name.
        if meth is None:
            meth = self.generic_visit
        return meth(node)

    def visit(self, node):
        stack = [node]
        lastRst = None
        while stack:
            try:
                last = stack[-1]
                if isinstance(last, types.GeneratorType):
                    stack.append(last.send(lastRst))
                    lastRst = None
                elif isinstance(last, Node):
                    stack.append(self._visit(stack.pop()))
                else:
                    lastRst = stack.pop()
            except StopIteration:
                stack.pop()
        return lastRst

    def generic_visit(self, node):
        raise RuntimeError('No {} method'.format('visit' + type(node).__name__))

class Evaluator(NodeVisitor):

    def visitNumber(self, node):
        return node.value

    def visitAdd(self, node):
        return self.visit(node.left) + self.visit(node.right)

    def visitSub(self, node):
        return self.visit(node.left) - self.visit(node.right)

    def visitMul(self, node):
        return self.visit(node.left) * self.visit(node.right)

    def visitDiv(self, node):
        return self.visit(node.left) / self.visit(node.right)

    def visitNegate(self, node):
        return -node.operand

t1 = Sub(Number(3), Number(4))
t2 = Mul(Number(2), t1)
t3 = Div(t2, Number(5))
t4 = Add(Number(1), t3)

e = Evaluator()
print(e.visit(t4))

class StackCode(NodeVisitor):
    def generate_code(self, node):
        self.instructions = []
        self.visit(node)
        return self.instructions

    def visitNumber(self, node):
        self.instructions.append(('PUSH', node.value))

    def binop(self, node, instructions):
        self.visit(node.left)
        self.visit(node.right)
        self.instructions.append((instructions,))

    def visitAdd(self, node):
        self.binop(node, 'ADD')

    def visitSub(self, node):
        self.binop(node, 'SUB')

    def visitMul(self, node):
        self.binop(node, 'MUL')

    def visitDiv(self, node):
        self.binop(node, 'DIV')

    def unaryop(self, node, instructions):
        self.visit(node.operand)
        self.instructions.append((instructions,))

    def visitNegate(self, node):
        self.unaryop(node, 'NEG')

s = StackCode()
print(s.generate_code(t4))
print(s.visit(t4))

a = Number(0)

for n in range(1, 100000):
    a = Add(a, Number(n))

e = Evaluator()
try:
    rst = e.visit(a)
    print(rst)
except Exception as e:
    print(f'Exception:{e}')

class Evaluator2(NodeVisitor):

    def visitNumber(self, node):
        return node.value

    def visitAdd(self, node):
        yield (yield node.left) + (yield node.right)

    def visitSub(self, node):
        yield (yield node.left) - (yield node.right)

    def visitMul(self, node):
        yield (yield node.left) * (yield node.right)

    def visitDiv(self, node):
        yield (yield node.left) / (yield node.right)

    def visitNegate(self, node):
        return -node.operand 

a = Number(0)

for n in range(1, 100000):
    a = Add(a, Number(n))

e = Evaluator2()
try:
    rst = e.visit(a)
    print(rst)
except Exception as e:
    print(f'Exception:{e}')


