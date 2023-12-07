class Token:
    def __init__(self, type:str=None, value:int=None) -> None:
        self.type:str = type
        self.value:int = value