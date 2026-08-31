class ReaderRegistry:
    def __init__(self):
        self.readers = {}

    def register(self, format, reader):
        if not isinstance(format, str): # add validation for reader object format once reader abstraction made
            raise TypeError("Format must be type string.")
        elif format in self.readers:
            raise ValueError("This format is already registered.")
    
        
        self.readers[format] = reader

