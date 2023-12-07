from modules.prepro import *
from modules.node import *
from modules.tokenizer import *

class Parser:
    tokenizer:Tokenizer = None

    @staticmethod
    def assign(tokenizer:Tokenizer) -> Node:
        value = tokenizer.next.value
        node = Identifier(value = value)
        tokenizer.select_next()
        if tokenizer.next.type == "ASSIGN":
            node = Assignment(value=value,children=[node, 
                                        Parser.parse_bool_expression(tokenizer)])
            return node
        raise Exception("Error")

    @staticmethod
    def parse_program(tokenizer:Tokenizer) -> Node:
        tokenizer.select_next()
        node = Block(children=[])
        while tokenizer.next.type != "EOF":
            if tokenizer.next.type not in ["STATEMENT","LINE","IDENTIFIER"]: 
                raise Exception("Error")
            node.children.append(Parser.parse_statement(tokenizer))
            tokenizer.select_next()
        return node
    
    @staticmethod
    def parse_block(tokenizer:Tokenizer) -> Node:
        if tokenizer.next.type == "LEFTC":
            tokenizer.select_next()
            node = Block(children=[])
            while tokenizer.next.type == "LINE":
                tokenizer.select_next()
                node.children.append(Parser.parse_statement(tokenizer))
            if tokenizer.next.type != "RIGHTC":
                raise Exception("Error")
            tokenizer.select_next()
            return node
        raise Exception("Error")
        
    @staticmethod
    def parse_statement(tokenizer:Tokenizer) -> Node:
        if tokenizer.next.type in ["INT"]:
            raise Exception("Error")
        elif tokenizer.next.type == "IDENTIFIER":
            node = Parser.assign(tokenizer)
            if tokenizer.next.type != "LINE":
                raise Exception("Error")
            return node
        elif tokenizer.next.type == "STATEMENT":
            if tokenizer.next.value == "traffic_information":
                value = tokenizer.next.value
                tokenizer.select_next()
                if tokenizer.next.type == "LEFTP":
                    tokenizer.select_next()
                    if tokenizer.next.type == "RIGHTP":
                        node = Traffic(value=value)
                        tokenizer.select_next()
                        return node
                    raise Exception("Error")
                raise Exception("Error")
            elif tokenizer.next.value == "show":
                tokenizer.select_next()
                if tokenizer.next.type == 'LEFTP':
                    node = Parser.parse_bool_expression(tokenizer)
                    if tokenizer.next.type == 'RIGHTP':
                        tokenizer.select_next()
                        return Print(children=[node])
                    raise Exception("Error")
                raise Exception("Error")
            
            elif tokenizer.next.value == "while":
                condition = Parser.parse_bool_expression(tokenizer) 
                block = Parser.parse_block(tokenizer)
                if tokenizer.next.type in ["LINE","EOF"]:
                    return While(children=[condition,block])
                raise Exception("Error")
            
            elif tokenizer.next.value == "rule":
                tokenizer.select_next()
                if tokenizer.next.type == "DECLARE":
                    tokenizer.select_next()
                    if tokenizer.next.type == "IDENTIFIER":
                        rule_iden = Identifier(value = tokenizer.next.value)
                        tokenizer.select_next()
                        if tokenizer.next.type == "LEFTC":
                            tokenizer.select_next()
                            strings = {}
                            while True:
                                tokenizer.select_next()
                                if tokenizer.next.value == "str":
                                    type_definition = tokenizer.next.value
                                    tokenizer.select_next()
                                    if tokenizer.next.type == "DECLARE":
                                        tokenizer.select_next()
                                        if tokenizer.next.type == "IDENTIFIER":
                                            value = tokenizer.next.value
                                            node = Identifier(value = value)
                                            tokenizer.select_next()
                                            if tokenizer.next.type == "ASSIGN":
                                                bexpr = Parser.parse_bool_expression(tokenizer)
                                                strings[value] = bexpr
                                                if tokenizer.next.type == "COMMA":
                                                    tokenizer.select_next() 
                                            else:
                                                raise Exception("Error")
                                        else:
                                            raise Exception("Error")
                                    else:
                                        raise Exception("Error")
                                elif tokenizer.next.type == "RIGHTC":
                                    break
                                else:
                                    raise Exception("Error")               
                            return VarDec(value = strings,
                                          children=[rule_iden])
                raise Exception("Error")
                
            elif tokenizer.next.value == "if":
                condition = Parser.parse_bool_expression(tokenizer) 
                if_block = Parser.parse_block(tokenizer)
                if tokenizer.next.value == "else":
                    tokenizer.select_next()
                    else_block = Parser.parse_block(tokenizer)
                    if tokenizer.next.type == "LINE":
                        return If(children=[condition,if_block,else_block])
                    raise Exception("Error")
                return If(children=[condition,if_block])
            
            elif tokenizer.next.value == "foreach":
                tokenizer.select_next()
                if tokenizer.next.type == "IDENTIFIER":
                    init =  Parser.assign(tokenizer)
                    if tokenizer.next.value == "to":
                            tokenizer.select_next()
                            final = Parser.assign(tokenizer)
                            block = Parser.parse_block(tokenizer)
                            return Foreach(children=[init, final, block])
                    raise Exception("Error") 
                raise Exception("Error") 
            
            elif tokenizer.next.value in ["int","str"]:
                type_definition = tokenizer.next.value
                tokenizer.select_next()
                if tokenizer.next.type == "DECLARE":
                    tokenizer.select_next()
                    if tokenizer.next.type == "IDENTIFIER":
                        value = tokenizer.next.value
                        node = Identifier(value = value)
                        tokenizer.select_next()
                        if tokenizer.next.type == "LINE":
                            return VarDec(value = value,
                                           children=[node,No_op(typedef=type_definition)])
                        if tokenizer.next.type == "ASSIGN":
                            bexpr = Parser.parse_bool_expression(tokenizer) 
                            return VarDec(value = value,
                                           children=[node,bexpr])
                        raise Exception("Error")
                    raise Exception("Error")
                raise Exception("Error")
            raise Exception("Error") 
        return No_op()
    
    @staticmethod
    def parse_bool_expression(tokenizer:Tokenizer) -> Node:
        node =Parser.parse_bool_term(tokenizer)
        while tokenizer.next.type == "OR":
            node =  Bin_op(value = tokenizer.next.value, 
                children=[node,Parser.parse_bool_term(tokenizer)])
        return node
    
    @staticmethod
    def parse_bool_term(tokenizer:Tokenizer) -> Node:
        node =Parser.parse_rel_expression(tokenizer)
        while tokenizer.next.type == "AND":
            node =  Bin_op(value = tokenizer.next.value, 
                children=[node,Parser.parse_rel_expression(tokenizer)])
        return node
    
    @staticmethod
    def parse_rel_expression(tokenizer:Tokenizer) -> Node:
        node =Parser.parse_expression(tokenizer)
        while tokenizer.next.type == "EQUAL" or tokenizer.next.type == "GREATER" or tokenizer.next.type == "LESS":
            node =  Bin_op(value = tokenizer.next.value, 
                children=[node,Parser.parse_expression(tokenizer)])
        return node

    @staticmethod
    def parse_expression(tokenizer:Tokenizer) -> Node:
        node = Parser.parse_term(tokenizer)
        while tokenizer.next.type in ["PLUS","MINUS","CONCAT"]:
            node =  Bin_op(value = tokenizer.next.value, 
                           children=[node,Parser.parse_term(tokenizer)])
        return node
    
    @staticmethod
    def parse_term(tokenizer:Tokenizer) -> Node:
        node = Parser.parse_factor(tokenizer)
        while tokenizer.next.type == "MULT" or tokenizer.next.type == "DIV":
            node =  Bin_op(value = tokenizer.next.value, 
                           children=[node,Parser.parse_factor(tokenizer)])
        return node
        
    @staticmethod
    def parse_factor(tokenizer:Tokenizer)->Node:
        tokenizer.select_next()
        if tokenizer.next.type == 'INT':
            node = Int_val(value = tokenizer.next.value)
            tokenizer.select_next()
            return node
        if tokenizer.next.type == 'STR':
            node = Str_val(value = tokenizer.next.value)
            tokenizer.select_next()
            return node
        elif tokenizer.next.type == 'IDENTIFIER':
            node = Identifier(value = tokenizer.next.value)
            tokenizer.select_next()
            return node
        elif tokenizer.next.type in ['PLUS',"MINUS","NOT"]:
            return Un_op(value=tokenizer.next.value,
                         children=[Parser.parse_factor(tokenizer)])
        elif tokenizer.next.type == "STATEMENT":
            if tokenizer.next.value == "input":
                tokenizer.select_next()
                if tokenizer.next.type == 'LEFTP':
                    tokenizer.select_next()
                    if tokenizer.next.type == 'RIGHTP':
                        tokenizer.select_next()
                        return Input()
                    raise Exception("Error")
                raise Exception("Error")
            elif tokenizer.next.value == "scanhost":
                tokenizer.select_next()
                if tokenizer.next.type == 'LEFTP':
                    tokenizer.select_next()
                    if tokenizer.next.type == 'IDENTIFIER':
                        ip_address = Identifier(value = tokenizer.next.value)
                        tokenizer.select_next()
                        if tokenizer.next.type == 'COMMA':
                            tokenizer.select_next()
                            if tokenizer.next.type == 'IDENTIFIER':
                                port = Identifier(value = tokenizer.next.value)
                                tokenizer.select_next()
                                if tokenizer.next.type == 'RIGHTP':
                                    tokenizer.select_next()
                                    return Scanhost(children=[ip_address,port])
            elif tokenizer.next.value == "match":
                tokenizer.select_next()
                if tokenizer.next.type == 'LEFTP':
                    tokenizer.select_next()
                    if tokenizer.next.type == 'IDENTIFIER':
                        file_name = Identifier(value = tokenizer.next.value)
                        tokenizer.select_next()
                        if tokenizer.next.type == 'COMMA':
                            tokenizer.select_next()
                            if tokenizer.next.type == 'IDENTIFIER':
                                rules = Identifier(value = tokenizer.next.value)
                                tokenizer.select_next()
                                if tokenizer.next.type == 'RIGHTP':
                                    tokenizer.select_next()
                                    return Match(children=[file_name,rules])
            raise Exception("Error")
        elif tokenizer.next.type == 'LEFTP':
            node = Parser.parse_bool_expression(tokenizer)
            if tokenizer.next.type == 'RIGHTP':
                tokenizer.select_next()
                return node
            raise Exception("Error") 
        else:
            raise Exception("Error") 

    @staticmethod
    def run(code:str) -> Node:
        code = Prepro(code).filter()
        tokenizer = Tokenizer(code,0,Token())
        node = Parser.parse_program(tokenizer)
        if tokenizer.next.type != "EOF":
            raise Exception("EOF not found")
        return node