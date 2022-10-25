# this module is use for testing the section 8.21 implement the visitor pattern

class Node: 
    pass

class UnaryOpertor(Node):
    def __init__(self, operand) -> None:
        super().__init__()
        self.operand = operand

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

class Negate(UnaryOpertor):
    pass 

class Number(Node):
    def __init__(self, value) -> None:
        super().__init__()
        self.value = value

class NodeVisitor:
    def visit(self, node):
        methname = 'visit_' + type(node).__name__
        meth = getattr(self, methname, None)
        if meth is None:
            meth = self.generic_visit
        return meth(node)

    def generic_visit(self, node):
        raise RuntimeError('No {} method'.format('visit'+ type(node).__name__))

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
        return self.visit(self.left) / self.visit(node.right)

    def visitNegate(self, node):
        return -node.operand

t1 = Sub(Number(3), Number(4))
t2 = Mul(Number(2), t1)
t3 = Div(t2, Number(5))
t4 = Add(Number(1), t3)

e = Evaluator()
e.visit(t4)