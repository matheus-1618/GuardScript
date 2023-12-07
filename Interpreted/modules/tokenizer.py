from modules.token_ import Token
import re

class Tokenizer:
    def __init__(self, source:str, position:int, next:Token) -> None:
        self.source:str = source
        self.position:int = position
        self.next:Token = next
        self.reserved:list = ["show","scanhost","traffic_information","match",
                              "foreach","input","while","rule","to","if","else",
                              "int","str"]
    
    def select_next(self) -> None:
        if self.position == len(self.source):
            self.next.type = "EOF"
            self.next.value = "'"
            return
        elif self.source[self.position] == "\n":
            self.next.type = "LINE"
            self.next.value = self.source[self.position]
            self.position+=1
        elif self.source[self.position].isspace():
            self.position+=1
            self.select_next()
        elif self.source[self.position] == ",":
            self.next.type = "COMMA"
            self.next.value = self.source[self.position]
            self.position+=1
        elif self.source[self.position] == "+":
            self.next.type = "PLUS"
            self.next.value = self.source[self.position]
            self.position+=1
        elif self.source[self.position] == ":":
            self.next.type = "DECLARE"
            self.next.value = self.source[self.position]
            self.position+=1
        elif self.source[self.position] == "-":
            self.next.type = "MINUS"
            self.next.value = self.source[self.position]
            self.position+=1
        elif self.source[self.position] == "*":
            self.next.type = "MULT"
            self.next.value = self.source[self.position]
            self.position+=1
        elif self.source[self.position] == "/":
            self.next.type = "DIV"
            self.next.value = self.source[self.position]
            self.position+=1
        elif self.source[self.position] == "(":
            self.next.type = "LEFTP"
            self.next.value = self.source[self.position]
            self.position+=1
        elif self.source[self.position] == ")":
            self.next.type = "RIGHTP"
            self.next.value = self.source[self.position]
            self.position+=1
        elif self.source[self.position:self.position+2] == "==":
            self.next.type = "EQUAL"
            self.next.value = self.source[self.position:self.position+2]
            self.position+=2
        elif self.source[self.position:self.position+2] == "||":
            self.next.type = "OR"
            self.next.value = self.source[self.position:self.position+2]
            self.position+=2
        elif self.source[self.position:self.position+2] == "&&":
            self.next.type = "AND"
            self.next.value = self.source[self.position:self.position+2]
            self.position+=2
        elif self.source[self.position] == ">":
            self.next.type = "GREATER"
            self.next.value = self.source[self.position]
            self.position+=1
        elif self.source[self.position] == "<":
            self.next.type = "LESS"
            self.next.value = self.source[self.position]
            self.position+=1
        elif self.source[self.position] == "!":
            self.next.type = "NOT"
            self.next.value = self.source[self.position]
            self.position+=1
        elif self.source[self.position] == "{":
            self.next.type = "LEFTC"
            self.next.value = self.source[self.position]
            self.position+=1
        elif self.source[self.position] == "}":
            self.next.type = "RIGHTC"
            self.next.value = self.source[self.position]
            self.position+=1
        elif self.source[self.position] == "=":
            self.next.type = "ASSIGN"
            self.next.value = self.source[self.position]
            self.position+=1
        elif self.source[self.position] == '"':
            tmp = ''
            self.next.type = "STR"
            self.position+=1
            while self.position < len(self.source):
                if self.source[self.position] == "\n":
                    raise Exception("Tokenizer error")
                if self.source[self.position] == '"':
                    self.position+=1
                    break
                tmp += self.source[self.position]
                self.position+=1
            self.next.value = (tmp)
        elif re.search(r'\b[a-zA-Z_]\w*\b|\b\w*[a-zA-Z_]\b', self.source[self.position]):
            self.next.value = ''
            while self.position < len(self.source) and re.search(r'\b\w+\b', 
                                                                 self.source[self.position]):
                self.next.value += self.source[self.position]
                self.position+=1
            if self.next.value not in self.reserved:
                self.next.type = "IDENTIFIER"
            else:
                self.next.type = "STATEMENT"
        else:
            tmp = ''
            self.next.type = "INT"
            while self.position < len(self.source) and re.search(r'[0-9]',self.source[self.position]):
                tmp += self.source[self.position]
                self.position+=1
            self.next.value = int(tmp)
        