#!/usr/bin/env python3
from basicLexer import iota

# Lesson 2: Abstract Syntax Tree (AST)
# In this lesson you will learn how an AST parses code into something the machine can read
# Check out `https://astexplorer.net` 

nodeTypes = {
    "Program": iota(True),
    "NumericLiteral": iota(),
    "Identifier": iota(),
    "BinaryExpr": iota(),
}

class Statement:
    def __init__(self, kind) -> None:
        self.kind = kind
    def __repr__(self) -> str:
        return "__statement__"

class Program(Statement):
    def __init__(self) -> None:
        super().__init__("Program")
        self.body: list[Statement] = []
    
    def __repr__(self) -> str:
        ret = "{\n"
        for stmt in self.body:
            ret += repr(stmt) + "\n"
        ret += "}"
        return ret

class Expr(Statement):
    def __init__(self, kind) -> None:
        super().__init__(kind)
    def __repr__(self) -> str:
        return "__expr__"

class BinaryExpr(Expr):
    def __init__(self, left: Expr, right: Expr, op: str) -> None:
        super().__init__("BinaryExpr")
        self.left = left
        self.right = right
        self.op = op
    
    def __repr__(self) -> str:
        ret = "("
        ret += repr(self.left) + " "
        ret += self.op + " "
        ret += repr(self.right)
        ret += ")"
        return ret

class Identifier(Expr):
    def __init__(self, symbol) -> None:
        super().__init__("Identifier")
        self.symbol = symbol
    def __repr__(self) -> str:
        return self.symbol

class NumericLiteral(Expr):
    def __init__(self, value: float) -> None:
        super().__init__("NumericLiteral")
        self.value = value

    def __repr__(self) -> str:
        return str(self.value)
