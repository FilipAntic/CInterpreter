from .lexer import  PLUS, MINUS, MUL, DIV,EQ,GT,GTE,LTE,LT,SIN,COS,CTG,TAN,LG,LB,SQRT,POW,LOG
import json
from math import *

###############################################################################
#                                                                             #
#  INTERPRETER                                                                #
#                                                                             #
###############################################################################

class NodeVisitor(object):
    def visit(self, node):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception('No visit_{} method'.format(type(node).__name__))


class Interpreter(NodeVisitor):
    def __init__(self, parser):
        self.parser = parser
        self.variables = {}

    def visit_BinOp(self, node):
        if node.op.type == PLUS:
            return self.visit(node.left) + self.visit(node.right)
        elif node.op.type == MINUS:
            return self.visit(node.left) - self.visit(node.right)
        elif node.op.type == MUL:
            return self.visit(node.left) * self.visit(node.right)
        elif node.op.type == DIV:
            return self.visit(node.left) / self.visit(node.right)
        elif node.op.type == EQ:
            self.readFromFile()
            self.variables[node.left] = self.visit(node.right)
            self.writeToFile()
            return ""
        elif node.op.type == GT:
            return self.visit(node.left) > self.visit(node.right)
        elif node.op.type == GTE:
            return self.visit(node.left) >= self.visit(node.right)
        elif node.op.type == LT:
            return self.visit(node.left) < self.visit(node.right)
        elif node.op.type == LTE:
            return self.visit(node.left) <= self.visit(node.right)
        elif node.op.value == SIN:
            return sin(self.visit(node.left))
        elif node.op.value == COS:
            return cos(self.visit(node.left))
        elif node.op.value == CTG:
            return 1/tan(self.visit(node.left))
        elif node.op.value == TAN:
            return tan(self.visit(node.left))
        elif node.op.value == LG:
            return log10(self.visit(node.left))
        elif node.op.value == LB:
            return log2(self.visit(node.left))
        elif node.op.value == SQRT:
            return sqrt(self.visit(node.left))
        elif node.op.value == POW:
            return pow(self.visit(node.left),self.visit(node.right))
        elif node.op.value == POW:
            return log(self.visit(node.left),self.visit(node.right))
        else:
            print(node.op)
    def visit_Num(self, node):
        return node.value

    def interpret(self):
        tree = self.parser.parse()
        return self.visit(tree)

    def readFromFile(self):
        with open('vars.json', 'r') as f:
            try:
                self.variables = json.load(f)
            # if the file is empty the ValueError will be thrown
            except ValueError:
                self.variables = {}

    def writeToFile(self):
        with open('vars.json', 'w') as f:
            json.dump(self.variables, f)
