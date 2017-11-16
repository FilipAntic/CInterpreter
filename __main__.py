from interpreter.lexer import Lexer
from interpreter.parser import Parser
from interpreter.interpreter import Interpreter
import json

def emptyJSON():
    with open('vars.json', 'w') as f:
        f.write("")

def main():
    emptyJSON()
    # with open('test.txt', 'r') as file:
    #     for line in file:
    #         text = line
    #         lexer = Lexer(text)
    #         parser = Parser(lexer)
    #         interpreter = Interpreter(parser)
    #         result = interpreter.interpret()
    #         print(result)
    #

    while True:
        try:
            text = input('>>> ')
        except (EOFError, KeyboardInterrupt):
            break
        if not text:
            continue

        if text == 'EXIT':
            return
        lexer = Lexer(text)
        parser = Parser(lexer)
        interpreter = Interpreter(parser)
        result = interpreter.interpret()
        if result == '':
            continue
        if float(result).is_integer():
            print("%.0f" % result)
        else:
            print("%.3f" % result)
        # print(result)


if __name__ == '__main__':
    main()

