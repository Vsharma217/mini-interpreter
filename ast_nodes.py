class Expr:
    pass
class Binary(Expr):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right
class Unary(Expr):
    def __init__(self, operator, right):
        self.operator = operator
        self.right = right
class Literal(Expr):
    def __init__(self, value):
        self.value = value
class Variable(Expr):
    def __init__(self, name):
        self.name = name

class Stmt:
    pass
class VarDecl(Stmt):
    def __init__(self, name, initializer):
        self.name = name
        self.initializer = initializer
class PrintStmt(Stmt):
    def __init__(self, expression):
        self.expression = expression
class IfStmt(Stmt):
    def __init__(self, condition, then_branch, else_branch):
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch
class ExprStmt(Stmt):
    def __init__(self, expression):
        self.expression = expression