class Prepro:
    def __init__(self,file:str = None) -> None:
        self.file:str = file
        self.code:str = None

    def open(self)->None:
        if self.file.split(".")[-1] == "gst":
            with open(self.file, 'r') as f:
                self.code = f.read()
        else:
            raise Exception("Not a Guardscript File.")
        
    def filter(self,file:str = None) -> str:
        if file != None:
            self.file = file
        self.open()
        lines = self.code.split('\n')
        cleaned_lines = []

        for line in lines:
            if '//' in line:
                cleaned_line = line.split('//')[0]
                cleaned_lines.append(cleaned_line.rstrip())
            else:
                cleaned_lines.append(line.rstrip())

        cleaned_code = '\n'.join(cleaned_lines)
        return cleaned_code