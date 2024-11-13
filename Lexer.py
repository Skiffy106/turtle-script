# Lexer.py
# This file creates a Lexer class to read the source code and prodce tokens

from typing import Any
from Token import Token, TokenType, lookup_ident

class Lexer:
    """
    A Lexer reads text and produces tokens

    Attributes
    ----------
    source : str
        the source code as a string
    position : int
        the current cursor position of the lexer
    read_position: int
        the current read positon of the lexer
    curent_char: int
        the character at the `read_position`

    Methods
    ----------
    def __read_char(self) -> None:
        reads the next character from `self.source`, sets `current_char`, and increments positions
    
    def __peek_char(self) -> str | None:
        reads the next character from `self.source` and returns it

    def __skip_whitepace(self) -> None:
        skips to the next non whitepace character

    TODO: Other Methods
    """
    def __init__(self, source: str) -> None:
        self.source = source

        self.position = -1
        self.read_position: int = 0
        self.line_num: int = 0

        self.current_char: str | None = None

        self.__read_char()

    def __read_char(self) -> None:
        if self.read_position >= len(self.source):
            self.current_char = None
        else:
            self.current_char = self.source[self.read_position]

        self.position = self.read_position
        self.read_position += 1

    def __peek_char(self) -> str | None:
        """ Peeks to the upcoming char without advancing the lexer position """
        if self.read_position >= len(self.source):
            return None

        return self.source[self.read_position]

    def skip_whitespace(self) -> None:
        while self.current_char in [' ', '\t', '\n', '\r']:
            if self.current_char == '\n':
                self.line_num += 1
            
            self.__read_char()

    def __new_token(self, tt: TokenType, literal: Any):
        return Token(tt, literal, self.line_num, self.position)

    def __is_digit(self, ch: str) -> bool:
        return ch.isdigit()

    def __is_letter(self, ch: str) -> bool:
        return ch.isalpha() or ch == '_'

    def __read_number(self) -> Token:
        """
        Reads all the digits of a number into a new Token and returns the Token
        """
        start_pos: int = self.position
        dot_count: int = 0

        output: str = ""
        while self.__is_digit(self.current_char) or self.current_char == '.':
            if self.current_char == '.':
                dot_count += 1
                
            if dot_count > 1:
                print(f"Too many decimals on line {self.line_num}, position {self.position}")
                return self.__new_token(TokenType.ILLEGAL, self.source[start_pos:self.position])

            output += self.source[self.position]

            self.__read_char()

            if self.current_char is None:
                break
            
        if dot_count == 0:
            return self.__new_token(TokenType.INT, int(output))
        else:
            return self.__new_token(TokenType.FLOAT, float(output))

    def __read_identifier(self) -> str:
        """
        Reads all the characters of a word into a new Token and returns the Token
        """
        position = self.position
        while self.current_char is not None and self.__is_letter(self.current_char):
            self.__read_char()
        
        return self.source[position:self.position]

    def next_token(self) -> Token:
        """
        Reads the next token
        """
        tok: Token = None

        self.skip_whitespace()

        # RANT: All my homies love Python 3.10
        match self.current_char:
            case '+':
                tok = self.__new_token(TokenType.PLUS, self.current_char)
            case '-':
                # Handle the arrow
                if self.__peek_char() == '>':
                    ch = self.current_char
                    self.__read_char();
                    tok = self.__new_token(TokenType.ARROW, ch + self.current_char)
                else:
                    tok = self.__new_token(TokenType.MINUS, self.current_char)                   

            case '*':
                tok = self.__new_token(TokenType.ASTERISK, self.current_char)
            case '/':
                tok = self.__new_token(TokenType.SLASH, self.current_char)
            case '^':
                tok = self.__new_token(TokenType.POW, self.current_char)
            case '%':
                tok = self.__new_token(TokenType.MODULUS, self.current_char)
            case '<':
                # Handle <=
                if self.__peek_char() == '=':
                    ch = self.current_char
                    self.__read_char()
                    tok = self.__new_token(TokenType.LT_EQ, ch + self.current_char)
                else:
                    tok = self.__new_token(TokenType.LT, self.current_char)
            case '>':
                # Handle >=
                if self.__peek_char() == '=':
                    ch = self.current_char
                    self.__read_char()
                    tok = self.__new_token(TokenType.GT_EQ, ch + self.current_char)
                else:
                    tok = self.__new_token(TokenType.GT, self.current_char) 
            case '=':
                # Handle ==
                if self.__peek_char() == '=':
                    ch = self.current_char
                    self.__read_char()
                    tok = self.__new_token(TokenType.EQ_EQ, ch + self.current_char)
                else:
                    tok = self.__new_token(TokenType.EQ, self.current_char) 
            case '!':
                # Handle !=
                if self.__peek_char() == '=':
                    ch = self.current_char
                    self.__read_char()
                    tok = self.__new_token(TokenType.NOT_EQ, ch + self.current_char)
                else:
                    # TODO: Add `not` token ~This can be added with unary operators~
                    tok = self.__new_token(TokenType.ILLEGAL, self.current_char) 
            case ':':
                tok = self.__new_token(TokenType.COLON, self.current_char)
            case ',':
                tok = self.__new_token(TokenType.COMMA, self.current_char)
            case '(':
                tok = self.__new_token(TokenType.LPAREN, self.current_char)
            case ')':
                tok = self.__new_token(TokenType.RPAREN, self.current_char)
            case '{':
                tok = self.__new_token(TokenType.LBRACE, self.current_char)
            case '}':
                tok = self.__new_token(TokenType.RBRACE, self.current_char)
            case ';':
                tok = self.__new_token(TokenType.SEMICOLON, self.current_char)
            case None:
                tok = self.__new_token(TokenType.EOF, "")
            case _:
                if self.__is_letter(self.current_char):
                    literal: str = self.__read_identifier()
                    tt: TokenType = lookup_ident(literal)
                    tok = self.__new_token(tt=tt, literal=literal)
                    return tok
                elif self.__is_digit(self.current_char):
                    return  self.__read_number()
                else:
                    tok = self.__new_token(TokenType.ILLEGAL, self.current_char)
        
        self.__read_char()
        return tok