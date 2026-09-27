from token_types import TokenType, Token

KEYWORDS = {
    "var": TokenType.VAR,
    "print":TokenType.PRINT,
    "if":TokenType.IF,
    "else":TokenType.ELSE,
}

class Scanner:
    def __init__(self, source: str):
        self.source = source
        self.tokens = []
        self.start = 0
        self.current = 0
        self.line = 1
    def scan_tokens(self):
        while not self.is_at_end():
            self.start = self.current
            self.scan_token()
        self.tokens.append(Token(TokenType.EOF, "", None, self.line))
        return self.tokens
    def is_at_end(self):
        return self.current >= len(self.source)
    def advance(self):
        ch = self.source[self.current]
        self.current +=1
        return ch
    def peek(self):
        if self.is_at_end():
            return '\0'
        return self.source[self.current]
    def match(self, expected):
        if self.is_at_end() or self.source[self.current] != expected:
            return False
        self.current += 1
        return True
    def add_token(self, type_, literal=None):
        text = self.source[self.start:self.current]
        self.tokens.append(Token(type_, text, literal, self.line))

    def scan_token(self):
        c = self.advance()
        if c == '(':
            self.add_token(TokenType.LPAREN)
        elif c == ')':
            self.add_token(TokenType.RPAREN)
        elif c == '+':
            self.add_token(TokenType.PLUS)
        elif c == '-':
            self.add_token(TokenType.MINUS)
        elif c == '*':
            self.add_token(TokenType.STAR)
        elif c == '/':
            self.add_token(TokenType.SLASH)
        elif c == '=':
            self.add_token(TokenType.EQUAL_EQUAL if self.match('=') else TokenType.EQUAL)
        elif c == '<':
            self.add_token(TokenType.LESS)
        elif c == '>':
            self.add_token(TokenType.GREATER)
        elif c in ' \r\t':
            pass
        elif c == '\n':
            self.line += 1
        elif c.isdigit():
            self.number()
        elif c.isalpha() or c == '_':
            self.identifier()
        else:
            print(f"[line {self.line}] Error: unexpected character '{c}'")
    def number(self):
        while self.peek().isdigit():
            self.advance()
        if self.peek() == '.' and self.source[self.current+1:self.current+2].isdigit():
            self.advance()
            while self.peek().isdigit():
                self.advance()
        value = float(self.source[self.start:self.current])
        self.add_token(TokenType.NUMBER, value)
    def identifier(self):
        while self.peek().isalnum() or self.peek() == '_':
            self.advance()
        text = self.source[self.start:self.current]
        token_type = KEYWORDS.get(text, TokenType.IDENTIFIER)
        self.add_token(token_type)