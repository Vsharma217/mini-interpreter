from token_types import TokenType
from ast_nodes import Binary, Unary, Literal, Variable, VarDecl, PrintStmt, IfStmt, ExprStmt

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current =0
    def parse(self):
        statements =[]
        while not self.is_at_end():
            statements.append(self.statement())
        return statements
    def statement(self):
        if self.match(TokenType.VAR):
            return self.var_decl()
        if self.match(TokenType.PRINT):
            return self.print_stmt()
        if self.match(TokenType.IF):
            return self.if_stmt()
        return self.expr_stmt()
    def var_decl(self):
        name = self.consume(TokenType.IDENTIFIER, "Expected variable name.")
        self.consume(TokenType.EQUAL, "Expected '=' after variable name.")
        initializer = self.expression()
        return VarDecl(name, initializer)
    def print_stmt(self):
        value = self.expression()
        return PrintStmt(value)
    def if_stmt(self):
        condition = self.expression()
        then_branch = self.statement()
        else_branch = None
        if self.match(TokenType.ELSE):
            else_branch = self.statement()
        return IfStmt(condition, then_branch, else_branch)
    def expr_stmt(self):
        expr = self.expression()
        return ExprStmt(expr)
    def expression(self):
        return self.equality()
    def equality(self):
        expr = self.comparison()
        while self.match(TokenType.EQUAL_EQUAL):
            operator = self.previous()
            right = self.comparison()
            expr = Binary(expr, operator, right)
        return expr
    def comparison(self):
        expr = self.term()
        while self.match(TokenType.LESS, TokenType.GREATER):
            operator = self.previous()
            right = self.term()
            expr = Binary(expr, operator, right)
        return expr
    def term(self):
        expr = self.factor()
        while self.match(TokenType.PLUS, TokenType.MINUS):
            operator = self.previous()
            right = self.factor()
            expr = Binary(expr, operator, right)
        return expr
    def factor(self):
        expr = self.unary()
        while self.match(TokenType.STAR, TokenType.SLASH):
            operator = self.previous()
            right = self.unary()
            expr = Binary(expr, operator, right)
        return expr
    def unary(self):
        if self.match(TokenType.MINUS):
            operator = self.previous()
            right = self.unary()
            return Unary(operator, right)
        return self.primary()
    def primary(self):
        if self.match(TokenType.NUMBER):
            return Literal(self.previous().literal)
        if self.match(TokenType.IDENTIFIER):
            return Variable(self.previous())
        if self.match(TokenType.LPAREN):
            expr = self.expression()
            self.consume(TokenType.RPAREN, "Expected ')' after expression.")
            return expr
        raise SyntaxError(f"Unexpected toke: {self.peek()}")
    def match(self, *types):
        for t in types:
            if self.check(t):
                self.advance()
                return True
        return False
    def check(self, type_):
        return self.peek().type == type_
    def advance(self):
        if not self.is_at_end():
            self.current +=1
        return self.previous()
    def is_at_end(self):
        return self.peek().type == TokenType.EOF
    def peek(self):
        return self.tokens[self.current]
    def previous(self):
        return self.tokens[self.current - 1]
    def consume(self, type_, message):
        if self.check(type_):
            return self.advance()
        raise SyntaxError(f"[line {self.peek().line}] {message}")
    