#!/usr/bin/env python3
from basicLexer import *
from ast import *

# Lesson 3: Parser (AST)
# In this lesson you will learn how an AST parses code into something the machine can read
# Check out `https://astexplorer.net` 


class Parser:
    def __init__(self, tokens: list[Token] = []) -> None:
        self.tokens = tokens

    def front(self) -> Token:
        return self.tokens[0]

    def notEOF(self) -> bool:
        return self.tokens[0].typee != tokenType["EOF"]
    
    def eat(self) -> Token:
        prev = self.front()
        del self.tokens[0]
        return prev
    
    def expect(self, tk_type: int, message: str) -> Token:
        prev = self.front()
        if prev.typee != tk_type:
            raise Exception(f"Parser Error: {message}, Expected: {tokenTypeRev[tk_type]}, Got: {tokenTypeRev[prev.typee]}")
        del self.tokens[0]
        return prev

    def produceAST(self, sourceCode: str) -> Program:
        self.tokens = tokenize(sourceCode)
        # print(self.tokens)
        program = Program()

        while self.notEOF():
            program.body.append(self.parse_statement())

        return program
    
    def parse_statement(self) -> Statement:
        # for now skip to parse_expr:
        return self.parse_expr()
    
    def parse_expr(self) -> Expr:
        return self.parse_additive_expr()
    
    def parse_multiplicative_expr(self) -> Expr:
        left = self.parse_primary_expr()

        while self.front().value == "*" or self.front().value == "/" or self.front().value == "%":
            operator = self.eat().value
            right = self.parse_primary_expr()
            left = BinaryExpr(left, right, operator)
        return left

    def parse_additive_expr(self) -> Expr:
        left = self.parse_multiplicative_expr()

        while self.front().value == "+" or self.front().value == "-":
            operator = self.eat().value
            right = self.parse_multiplicative_expr()
            left = BinaryExpr(left, right, operator)
        return left

    def parse_primary_expr(self) -> Expr:
        tk = self.front()

        if tk.typee == tokenType["Identifier"]:
            return Identifier(self.eat().value)
        elif tk.typee == tokenType["Null"]:
            self.eat()
            return NullLiteral()
        elif tk.typee == tokenType["Number"]:
            return NumericLiteral(float(self.eat().value))
        elif tk.typee == tokenType["OpenParen"]:
            self.eat() # eat open parenthesis
            value = self.parse_expr()
            self.eat() # eat closed parenthesis
            return value

        else:
            raise Exception("Unexpected token found during parsing!" + repr(tk))