class ParserException(Exception):
    def __init__(self, message):
        super().__init__()
        self.message = message
    
    def __str__(self):
        return self.message


class InvalidFormat(ParserException):
    pass


class InvalidFile(ParserException):
    pass


class InvalidFeature(ParserException):
    pass
