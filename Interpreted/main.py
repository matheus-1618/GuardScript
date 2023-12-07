import sys
from modules.parser_ import Parser
from modules.symboltable import Symbol_table

if __name__ == "__main__":
    root = Parser.run(sys.argv[1])
    root.evaluate()