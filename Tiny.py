import sys
import enum
from Lexer import *
from Parser import *
from emmit import *

def main():
    print("Tiny Complier")

    if len(sys.argv) != 2:
        sys.exit("Error: Compiler needs source file as argument.")
    with (open(sys.argv[1],'r') as inputFile):
        source = inputFile.read()


    lexer = Lexer(source)
    emitter = Emitter("OutputFile")
    parser = Parser(lexer,emitter)

    parser.program()
    emitter.writeFile()
    print("Parsing completed.")

main()
