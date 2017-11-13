from interpreter.lexer import Lexer
from interpreter.parser import Parser
from interpreter.interpreter import Interpreter

def main():
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
        print(result)


if __name__ == '__main__':
    main()
