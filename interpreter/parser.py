from .lexer import *
from math import *
import json


###############################################################################
#                                                                             #
#  PARSER                                                                     #
#                                                                             #
###############################################################################

class AST(object):
    pass


class BinOp(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right

class Num(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value

class Parser(object):
    def __init__(self, lexer):
        self.lexer = lexer
        # set current token to the first token taken from the input
        self.current_token = self.lexer.get_next_token()
        self.variables = {}

    def error(self):
        raise Exception('Invalid syntax')

    def eat(self, token_type):
        # compare the current token type with the passed token
        # type and if they match then "eat" the current token
        # and assign the next token to the self.current_token,
        # otherwise raise an exception.
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def factor(self):
        """factor : INTEGER | LPAREN expr RPAREN"""
        token = self.current_token
        if token.type == INTEGER:
            self.eat(INTEGER)
            return Num(token)
        elif token.type == LPAREN:
            self.eat(LPAREN)
            node = self.raf_math()
            self.eat(RPAREN)
            return node
        elif token.type == STRING:
            self.eat(STRING)
            stringVal = token.value
            if self.current_token.type == EQ:
                tok = self.current_token
                self.eat(EQ)
                node = self.raf_math()
                return BinOp(left=stringVal, op=tok, right=node)
            elif self.current_token.type == LPAREN:
                self.eat(LPAREN)
                node = self.raf_math()
                if token.value == 'POW':
                    self.eat(COMMA)
                    node2 = self.raf_math()
                    result = pow(node.value, node2.value)
                elif token.value == 'SIN':
                    result = sin(node.value)
                elif token.value == 'COS':
                    result = cos(node.value)
                elif token.value == 'TAN':
                    result = tan(node.value)
                elif token.value == 'CTG':
                    result = 1 / tan(node.value)
                elif token.value == 'SQRT':
                    result = sqrt(self.visit(node))
                elif token.value == 'LG':
                    result = log10(node.value)
                elif token.value == 'LB':
                    result = log2(node.value)
                elif token.value == 'LOG':
                    self.eat(COMMA)
                    node2 = self.raf_math()
                    result = log(node.value, node2.value)
                self.eat(RPAREN)
                return Num(Token(token.value, result))
            self.readFromFile()
            if token.value in self.variables:
                return Num(Token(token.value, self.variables.get(token.value)))
    def term(self):
        """term : factor ((MUL | DIV) factor)*"""
        node = self.factor()

        while self.current_token.type in (MUL, DIV):
            token = self.current_token
            if token.type == MUL:
                self.eat(MUL)
            elif token.type == DIV:
                self.eat(DIV)
            node = BinOp(left=node, op=token, right=self.factor())
        return node

    def expr(self):
        """
        expr   : term ((PLUS | MINUS) term)*
        term   : factor ((MUL | DIV) factor)*
        factor : INTEGER | LPAREN expr RPAREN
        """
        node = self.term()

        while self.current_token.type in (PLUS, MINUS):
            token = self.current_token
            if token.type == PLUS:
                self.eat(PLUS)
            elif token.type == MINUS:
                self.eat(MINUS)
            node = BinOp(left=node, op=token, right=self.term())

        return node

    def raf_math(self):
        node = self.expr()
        while self.current_token.type in (GT,GTE,LT,LTE):
            token = self.current_token
            if token.type == GT:
                self.eat(GT)
            elif token.type == GTE:
                self.eat(GTE)
            elif token.type == LT:
                self.eat(LT)
            elif token.type == LTE:
                self.eat(LTE)
            node = BinOp(left=node,op = token, right=self.expr())
        return node

    def parse(self):
        node = self.raf_math()
        if self.current_token.type != EOF:
            self.error()
        return node


    def readFromFile(self):
        with open('vars.json', 'r') as f:
            try:
                self.variables = json.load(f)
            # if the file is empty the ValueError will be thrown
            except ValueError:
                self.variables = {}

    def visit(self, node):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception('No visit_{} method'.format(type(node).__name__))

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

    def visit_Num(self, node):
        return node.value