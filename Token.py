# Token.py
# This file defines the properties and methods of the Token class

from enum import Enum
from typing import Any

class TokenType(Enum):
   # Special Items
   EOF = "EOF"
   ILLEGAL  = "ILLEGAL"

   # Data Types
   IDENT = "IDENT"
   INT = "INT"
   FLOAT = "FLOAT"

   # Arithmetic Symbols
   PLUS = "PLUS"
   MINUS = "MINUS"
   ASTERISK = "ASTERISK"
   SLASH = "SLASH"
   POW = "POW"
   MODULUS = "MODULUS"

   # Assignment
   EQ = "EQ"

   # Comparison Symbols
   LT = '<'
   GT = '>'
   EQ_EQ = '=='
   NOT_EQ = '!='
   LT_EQ = '<='
   GT_EQ = '>='

   # Symbols
   COLON = "COLON"
   COMMA = "COMMA"
   SEMICOLON = "SEMICOLON"
   ARROW = "ARROW"
   LPAREN = "LPAREN"
   RPAREN = "RPAREN"
   LBRACE = "LBRACE"
   RBRACE = "RBRACE"

   # Keywords
   LET = "LET"
   FUNC = "FUNC"
   RETURN = "RETURN"
   IF = "IF"
   
   ELSE = "ELSE"
   TRUE = "TRUE"
   FALSE = "FALSE"

   # Types
   TYPE = "TYPE"

class Token:
    """
    A Token is an identified block of text with a specific meaning`

    Attributes
    ----------
    type : TokenType
        the identifier of the let assignment as an Expression
    literal : str | int | bool
        the raw text from the code
    line_num : str
        the line that the Token is on
    position: int
        the position on the line of the first character of the token
    """
    def __init__(self, type : TokenType, literal: Any, line_num: int, position: int) -> None:
        self.type = type
        self.literal = literal
        self.line_num = line_num
        self.position = position

    def __str__(self) -> str:
        return f"Token[{self.type} : {self.literal} : Line {self.line_num} : Position {self.position}]"

    def __repr__(self) -> str:
        return str(self)

KEYWORDS: dict[str, TokenType] = {
    "let": TokenType.LET,
    "func": TokenType.FUNC,
    "return": TokenType.RETURN,
    "if": TokenType.IF,
    # TODO: Add Elif
    "else": TokenType.ELSE,
    "true": TokenType.TRUE,
    "false": TokenType.FALSE,
}

TYPE_KEYWORDS: list[str] = ["int", "float"]

def lookup_ident(identifier: str) -> TokenType:
    token_type: TokenType | None = KEYWORDS.get(identifier)
    if token_type is not None:
        return token_type
    
    if identifier in TYPE_KEYWORDS:
        return TokenType.TYPE
    
    return TokenType.IDENT