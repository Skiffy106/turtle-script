from parser import *


if __name__ == "__main__":
    parser = Parser();

    while True:
        inp = input("> ")
        if (inp == 'q'):
            exit(1)

        program = parser.produceAST(inp);
        print(program)