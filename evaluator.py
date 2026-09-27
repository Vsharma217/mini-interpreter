from token_types import TokenType
from ast_nodes import Binary, Unary, Literal, Variable, VarDecl, PrintStmt, IfStmt, ExprStmt

class Evaluator:
    def __init__(self, environment):
        self.environment = environment
    def evaluate(self, node):
        if isinstance(node, Literal):
            return node.value
        if isinstance(node, Variable):
            return self.environment.get(node.name)
        if isinstance(node, Unary):
            return self.eval_unary(node)
        if isinstance(node, Binary):
            return self.eval_binary(node)
        raise RuntimeError(f"Unknown expression node: {node}")
    def eval_unary(self, node):
        right = self.evaluate(node.right)
        if node.operator.type == TokenType.MINUS:
            return -right
        raise RuntimeError(f"Unknown unary operator: {node.operator.lexeme}")
    def eval_binary(self, node):
        left = self.evaluate(node.left)
        right = self.evaluate(node.right)
        op = node.operator.type
        if op == TokenType.PLUS:
            return left + right
        if op == TokenType.MINUS:
            return left - right
        if op == TokenType.STAR:
            return left * right
        if op == TokenType.SLASH:
            if right == 0:
                raise RuntimeError(f"[line {node.operator.line}] Division by 0.")
            return left / right
        if op == TokenType.EQUAL_EQUAL:
            return left == right
        if op == TokenType.LESS:
            return left < right
        if op == TokenType.GREATER:
            return left > right
        raise RuntimeError(f"Unknown binary operator: {node.operator.lexeme}")
    def execute(self, stmt):
        if isinstance(stmt, VarDecl):
            self.exec_var_decl(stmt)
        elif isinstance(stmt, PrintStmt):
            self.exec_print(stmt)
        elif isinstance(stmt, IfStmt):
            self.exec_if(stmt)
        elif isinstance(stmt, ExprStmt):
            self.evaluate(stmt.expression)
        else:
            raise RuntimeError(f"Unknown statement: {stmt}")
    def exec_var_decl(self, stmt):
        value = self.evaluate(stmt.initializer)
        self.environment.define(stmt.name.lexeme, value)
    def exec_print(self, stmt):
        value = self.evaluate(stmt.expression)
        print(value)
    def exec_if(self, stmt):
        condition_value = self.evaluate(stmt.condition)
        if condition_value:
            self.execute(stmt.then_branch)
        elif stmt.else_branch is not None:
            self.execute(stmt.else_branch)
    def run(self, statements):
        for stmt in statements:
            self.execute(stmt)