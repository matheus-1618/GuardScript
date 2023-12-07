class Symbol_table:
    def __init__(self) -> None:
        self.table = {}
    def getter(self, key:str)->dict:
        return self.table[key]
    def setter(self,key:str,values:tuple)->None:
        if key in self.table:
            if values[1] == self.table[key][1]:
                self.table[key] = values
            else: raise Exception("Error")
        else: raise Exception("Error")
    def create(self,key:str,values:tuple)->None:
        if key not in self.table:
            self.table[key] = values
        else: raise Exception("Error")
            
