from enum import Enum, auto

class TokenType(Enum):
    # Literals
    NUMBER = auto()
    IDENTIFIER = auto()
    # Operators
    PLUS = auto()
    MINUS = auto()
    STAR = auto()
    SLASH = auto()
    EQUAL = auto()          
    EQUAL_EQUAL = auto()    
    LESS = auto()
    GREATER = auto()
    # Punctuation
    LPAREN = auto()
    RPAREN = auto()
    # Keywords
    VAR = auto()
    PRINT = auto()
    IF = auto()
    ELSE = auto()
    # End
    EOF = auto()

class Token:
    def __init__(self, type_, lexeme, literal, line):
        self.type = type_
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def __repr__(self):
        return f"Token({self.type}, {self.lexeme!r}, {self.literal})"