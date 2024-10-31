#!/usr/bin/env python3
import os

# Lesson 1: Basic Lexer
# In this lesson you will learn how to parse text into tokens using a lexer/tokenizer

# This is a fix for python enums in the style of golang but you can ignore this
# Thanks to `https://www.youtube.com/@TsodingDaily` for this code
iota_counter: int = 0
def iota(reset=False) -> int:
    global iota_counter
    if reset:
        iota_counter = 0
    result: int = iota_counter
    iota_counter += 1
    return result

# We will start with some basic types
# Thanks to `https://github.com/tlaceby` and `https://en.wikipedia.org/wiki/Lexical_analysis`
tokenType = {
    "Number": iota(True),
	"Identifier": iota(),
	"Let": iota(),
	"BinaryOperator": iota(),
	"Equals": iota(),
	"OpenParen": iota(),
	"CloseParen": iota(),
    "EOF": iota()
}

# Reverses the dictionary to allow use like `tokenTypeRev[1]`
tokenTypeRev = dict(map(reversed, tokenType.items()))

keywords = {
    "let": "Let",
}

# We will use classes as a replacement for types
class Token:
    def __init__(self, typee: int, value: str = "") -> None:
        self.typee = typee
        self.value = value

    def __repr__(self) -> str:
        return f"({tokenTypeRev[self.typee]}, \"{self.value}\")"

# Imagine our code looks like this:
#   let x = 5 * ( 4 + 2 )

def tokenize(code: str) -> list[Token]: 
    tokens = []
    while len(code) > 0:
        if code[0] == '(':
            tokens.append(Token(tokenType["OpenParen"], code[0]))
            code = code[1:] # this is not optimal but it works
        elif code[0] == ')':
            tokens.append(Token(tokenType["CloseParen"], code[0]))
            code = code[1:]
        elif code[0] == '+' or code[0] == '-' or code[0] == '*' or code[0] == '/' or code[0] == '%': # ignore the unary `-` operator for now
            tokens.append(Token(tokenType["BinaryOperator"], code[0]))
            code = code[1:]
        elif code[0] == '=':
            tokens.append(Token(tokenType["Equals"], code[0]))
            code = code[1:]
        elif code[0] == ' ' or code[0] == '\t' or code[0] == '\n':
            code = code[1:]
        else:
            # Now handle multi-charater tokens
            if code[0].isnumeric():
                num = ""
                while len(code) > 0 and code[0].isnumeric():
                    num += code[0]
                    code = code[1:]
                
                tokens.append(Token(tokenType["Number"], num))

            elif code[0].isalpha():
                ident = "";
                while len(code) > 0 and code[0].isalpha():
                    ident += code[0]
                    code = code[1:]
                
                # Check if reserved keyword
                if ident in keywords:
                    tokens.append(Token(tokenType[keywords[ident]], ident)) # Rant: this goofy dictionary stuff is all because python doesn't have types :(
                else:
                    tokens.append(Token(tokenType["Identifier"], ident))
            
            else:
                raise Exception(f"Unknown charcter: `{code[0]}`")
    tokens.append(Token(tokenType["EOF"]))
    return tokens
        

def tokenizeFile(filename: str) -> list[Token]:
    # necessary for local file pathing to work
    os.chdir(os.path.dirname(__file__))

    tokens = []
    with open(filename, "r") as file:
        tokens = tokenize(file.read())

    return tokens

if __name__ == "__main__":
    print(tokenizeFile("code.trtl"))
