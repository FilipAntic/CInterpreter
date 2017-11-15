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
                    self.eat(RPAREN)
                    return BinOp(left=node, op=token, right=node2)
                elif token.value == 'SIN':
                    self.eat(RPAREN)
                    return BinOp(left=node,op=token,right=7)
                elif token.value == 'COS':
                    self.eat(RPAREN)
                    return BinOp(left=node, op=token, right=7)
                elif token.value == 'TAN':
                    self.eat(RPAREN)
                    return BinOp(left=node, op=token, right=7)
                elif token.value == 'CTG':
                    self.eat(RPAREN)
                    return BinOp(left=node, op=token, right=7)
                elif token.value == 'SQRT':
                    self.eat(RPAREN)
                    return BinOp(left=node, op=token, right=7)
                elif token.value == 'LG':
                    self.eat(RPAREN)
                    return BinOp(left=node, op=token, right=7)
                elif token.value == 'LB':
                    self.eat(RPAREN)
                    return BinOp(left=node, op=token, right=7)
                elif token.value == 'LOG':
                    self.eat(COMMA)
                    node2 = self.raf_math()
                    self.eat(RPAREN)
                    return BinOp(left=node,op=token,right=node2)
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

