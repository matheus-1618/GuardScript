from modules.symboltable import Symbol_table
import socket
import struct
import datetime
try:
    import yara
except:
    pass

symbol_table = Symbol_table()
class Node:
    def __init__(self, value, children:list) -> None:
        self.value = value
        self.children:list = children
    def evaluate(self):
        return None,"int"

class Bin_op(Node):
    def __init__(self, value, children:list): #Aqui 
        super().__init__(value, children)
    def evaluate(self)->Node:
        ch0 = self.children[0].evaluate()
        ch1 = self.children[1].evaluate()
        if type(self.value) == str:
            if ch0[1] == "string" or ch1[1] == "string":
                if self.value == ".":
                    return str(ch0[0][0]) + str(ch1[0]), "string"
            if ch0[1] == "string" and ch1[1] == "string":
                if self.value == "==":
                    return int(ch0[0] == ch1[0]), "int"
                if self.value == ">":
                    return int(ch0[0] > ch1[0]), "int"
                if self.value == "<":
                    return int(ch0[0] < ch1[0]), "int"
                else:
                    raise Exception("Error")
            if ch0[1] == "int" and ch1[1] == "int":
                if self.value == "+":
                    return ch0[0] + ch1[0], "int"
                if self.value == "-":
                    return ch0[0] - ch1[0], "int"
                if self.value == "/":
                    return ch0[0] // ch1[0], "int"
                if self.value == "*":
                    return ch0[0] * ch1[0], "int"
                if self.value == "&&":
                    return int(ch0[0] and ch1[0]), "int"
                if self.value == "||":
                    return int(ch0[0] or ch1[0]), "int"
                if self.value == "==":
                    return int(ch0[0] == ch1[0]), "int"
                if self.value == ">":
                    return int(ch0[0] > ch1[0]), "int"
                if self.value == "<":
                    return int(ch0[0] < ch1[0]), "int"
                if self.value == ".":
                    return str(ch0[0]) + str(ch1[0]), "string"
                else:
                    raise Exception("Error")
        else:
            raise Exception("Error")
        
class Un_op(Node):
    def __init__(self, value, children:list): #Aqui 
        super().__init__(value, children)
    def evaluate(self)->Node:
        if type(self.value) == str:
            if self.value == "+":
                return +self.children[0].evaluate()[0],"int"
            if self.value == "-":
                return -self.children[0].evaluate()[0],"int"
            if self.value == "!":
                return int(not self.children[0].evaluate()[0]),"int"
        else:
            raise Exception("Error")

class Int_val(Node):
    def __init__(self, value, children:list=None): #Aqui 
        super().__init__(value, children)
    def evaluate(self)->Node:
        return self.value, "int"

class Str_val(Node):
    def __init__(self, value, children:list=None): #Aqui 
        super().__init__(value, children)
    def evaluate(self)->Node:
        return self.value, "string"
    
class Rule_val(Node):
    def __init__(self, value, children:list=None): #Aqui 
        super().__init__(value, children)
    def evaluate(self)->Node:
        return self.value, "rule"

class No_op(Node):
    def __init__(self, value=None,typedef = "int", children:list=None): #Aqui 
        super().__init__(value, children)
        self.typedef = typedef
    def evaluate(self)->Node:
        return None,self.typedef

class Block(Node):
    def __init__(self, value=None, children:list=None): #Aqui 
        super().__init__(value, children)
    def evaluate(self)->Node:
        for c in self.children:
            c.evaluate()

class Print(Node):
    def __init__(self, value = None, children:list = []): #Aqui 
        super().__init__(value, children)
    def evaluate(self)->Node:
        print(self.children[0].evaluate()[0])

class Scanhost(Node):
    def __init__(self, value = None, children:list = []): #Aqui 
        super().__init__(value, children)
    def evaluate(self)->Node:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        ip, port = self.children
        result = "open"
        try:
            sock.connect((ip.evaluate()[0], port.evaluate()[0]))
        except socket.error:
            result = "closed"
        finally:
            sock.close()
            return result, "string"

class Traffic(Node):
    def __init__(self, value = None, children:list = []): #Aqui 
        super().__init__(value, children)
    def evaluate(self)->Node:
        def parse_ethernet_frame(packet_data):
            ethernet_header = struct.unpack('!6s6sH', packet_data[:14])
            destination_address = ':'.join(f'{byte:02x}' for byte in ethernet_header[0])
            source_address = ':'.join(f'{byte:02x}' for byte in ethernet_header[1])
            ether_type = ethernet_header[2]
            return destination_address, source_address, ether_type
        def parse_ip_packet(packet_data):
            ip_header = struct.unpack('!BBHHHBBH4s4s', packet_data[14:34])
            version_ihl = ip_header[0]
            version = version_ihl >> 4
            ihl = (version_ihl & 0x0F) * 4
            ttl = ip_header[5]
            protocol = ip_header[6]
            source_ip = socket.inet_ntoa(ip_header[8])
            dest_ip = socket.inet_ntoa(ip_header[9])
            return version, ihl, ttl, protocol, source_ip, dest_ip

        raw_socket = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(0x0003))
        packet_data, _ = raw_socket.recvfrom(65536)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        dest_address, src_address, ether_type = parse_ethernet_frame(packet_data)
        print(f"\nTimestamp: {timestamp}")
        print(f"Packet Length: {len(packet_data)} bytes")
        print(f"Source MAC: {src_address}")
        print(f"Destination MAC: {dest_address}")
        print(f"Ethernet Type: {hex(ether_type)}")
        if ether_type == 0x0800:  # IPv4 EtherType
            version, ihl, ttl, protocol, source_ip, dest_ip = parse_ip_packet(packet_data)
            print("IPv4 Header:")
            print(f"Version: {version}")
            print(f"IHL: {ihl} bytes")
            print(f"TTL: {ttl}")
            print(f"Protocol: {protocol}")
            print(f"Source IP: {source_ip}")
            print(f"Destination IP: {dest_ip}")

class Match(Node):
    def __init__(self, value = None, children:list = []): #Aqui 
        super().__init__(value, children)
    def evaluate(self)->Node:
        yara_rule = f"rule {self.children[1].value}" + "{\n\tstrings:"
        strings = self.children[1].evaluate()
        for string in strings:
            yara_rule+= f'\n\t\t${string} = "{strings[string].evaluate()[0]}"'
        yara_rule+="\n\tcondition:\n\t\tall of them\n}"
        compiled_rule = yara.compile(source=yara_rule)
        file_path = self.children[0].evaluate()[0]
        matches = compiled_rule.match(file_path)
        if matches:
            return int(True),"int"
        else:
            return int(False),"int"
    

class Input(Node):
    def __init__(self, value = None, children:list = []): #Aqui 
        super().__init__(value, children)
    def evaluate(self)->Node:
        return input(),"string"

class Identifier(Node):
    def __init__(self, value = None, children:list=[]): #Aqui 
        super().__init__(value, children)
    def evaluate(self)->Node:
        return symbol_table.getter(self.value)

class Assignment(Node):
    def __init__(self, value, children:list): #Aqui 
        super().__init__(value, children)
    def evaluate(self)->Node:
        symbol_table.setter(self.children[0].value,
                            self.children[1].evaluate())

class If(Node):
    def __init__(self, value = None, children:list = []): #Aqui 
        super().__init__(value, children)
    def evaluate(self)->Node:
        #if
        if (self.children[0].evaluate()[0]):
            self.children[1].evaluate()
        #else
        elif len(self.children) > 2:
            return self.children[2].evaluate()
        
class While(Node):
    def __init__(self, value = None, children:list = []): #Aqui 
        super().__init__(value, children)
    def evaluate(self)->Node:
        condition, block = self.children
        while True:
            if not condition.evaluate()[0]: #CONDITION
                break
            block.evaluate() #BLOCK

class Foreach(Node):
    def __init__(self, value = None, children:list = []): #Aqui 
        super().__init__(value, children)
    def evaluate(self)->Node:
        init, final, block = self.children
        init.evaluate() 
        final.evaluate()
        start = init.children[0].evaluate()[0]
        end = final.children[0].evaluate()[0]
        for i in range(start,end):
            block.evaluate() #BLOCK
        
class VarDec(Node):
    def __init__(self, value = None, children:list = []): #Aqui 
        super().__init__(value, children)
        #self.typedef = typedef
    def evaluate(self)->Node:
        if type(self.value) == dict:
            symbol_table.create(self.children[0].value,
                            self.value)
        else:
            symbol_table.create(self.children[0].value,
                            self.children[1].evaluate())





