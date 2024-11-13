# AST.py
# This is where the structure of turtle script is defined

from abc import ABC, abstractmethod
from enum import Enum
import json

class NodeType(Enum): # RANT: this is the way the python handles enumeration

    Program = "Program"

    # Statements
    ExpressionStatement = "ExpressionStatement"     # All Statements below are Expression Statements
    LetStatement = "LetStatement"                   # ex: let x = ...
    FunctionStatement = "FunctionStatement"         # ex: func add(x : int, y: int)
    BlockStatement = "BlockStatement"               # ex: { x = 5; y = x - 7; }
    ReturnStatement = "ReturnStatement"             # ex: return 10
    AssignStatement = "AssignStatement"             # ex: x = 5
    IfStatement = "IfStatement"                     # ex: if (x < 5)

    # Expressions
    InfixExpression = "InfixExpression"             # ex: 5 + 5 * 3
    CallExpression = "CallExpression"               # ex: add(1,2)

    # Literals
    IntegerLiteral = "IntegerLiteral"               # ex: 367
    FloatLiteral = "FloatLiteral"                   # ex: 3.14
    IdentifierLiteral = "IdentifierLiteral"         # ex: x
    BooleanLiteral = "BooleanLiteral"               # ex: true

    # Helper                                              v       v
    FunctionParameter = "FunctionParameter"         # add(x: int, y: int)

class Node(ABC):
    """
    Node is an abstract base class which other classes will inherit from.
    It provides abstract methods `type()` and `data()`
    """
    @abstractmethod
    def type(self) -> NodeType:
        "Returns the NodeType of the Node"
        pass

    @abstractmethod
    def data(self) -> dict:
        "Returns the contents contained in Node"
        pass

    def __str__(self) -> str:
        with open("debug/parser.json", "a") as f:
           json.dump(self.data(), f, indent = 4)

    def __repr__(self) -> None:
        return str(self)
    

class Statement(Node):
    """
    Statements are a block of code that doesn't neccessarily prodice a result:
    For example: `print(my_string)`, `x = 5`, `if (x > 10): ...` and `for i in range(10): ...`
    """
    pass

class Expression(Node):
    """
    Expressions are a block of code that evaluate to a value.
    For example: `len(my_string)`, `2 + 2` and `add(5, 5)`
    """
    pass

class Program(Node):
    """
    This is the top/head node where parsing will begin. It contains a list of statments at `self.statements`.
    """
    def __init__(self) -> None:
        self.statements: list[Statement] = []

    def type(self) -> NodeType:
        return NodeType.Program

    def data(self) -> dict:
        """
        Returns the type and statement in a dictionary
        """
        return {
            "type": self.type().value,
            "statements": [
                { stmt.type().value: stmt.data() } for stmt in self.statements
            ]
        }
    
# region Helpers
class FunctionParameter(Expression):
    """
    TODO: Add Docstring
    """
    def __init__(self, name: str, value_type: str = None) -> None:
        self.name = name
        self.value_type = value_type
    
    def type(self) -> NodeType:
        return NodeType.FunctionParameter

    def data(self) -> dict:
        return {
            "type": self.type().value,
            "name": self.name,
            "value_type": self.value_type
        }

# endregion
    
# region Statements
class ExpressionStatement(Statement):
    """
    An Expression Statement is a Statement that evaluates to an expression
    """
    def __init__(self, expr: Expression = None) -> None:
        self.expr: Expression = expr

    def type(self) -> NodeType:
        return NodeType.ExpressionStatement
    
    def data(self) -> dict:
        return {
            "type": self.type().value,
            "expr": self.expr.data()
        }

class LetStatement(Statement):
    """
    A Let Statement allows the assignment of a variable. Ex: `let x: int = 5`

    Attributes
    ----------
    name : Expression
        the identifier of the let assignment as an Expression
    value : Expression
        the value of the let assignment as an Expression
    value_type : str
        the type of the variable to be assigned
    """
    def __init__(self, name: Expression = None, value: Expression = None, value_type: str = None) -> None:
        self.name: Expression = name
        self.value: Expression = value
        self.value_type: str = value_type

    def type(self) -> NodeType:
        return NodeType.LetStatement
    
    def data(self) -> dict:
        return {
            "type": self.type().value,
            "expr": self.name.data(),
            "value": self.value.data(),
            "value_type": self.value_type
        }
    
class BlockStatement(Statement):
    """
    A Block Statement is a group of statements. Think `{}` in Java

    Attributes
    ----------
    statements : list[Statement]
        the list of statements contained within the Block Statement
    """
    def __init__(self, statements: list[Statement] = None) -> None:
        self.statements = statements if statements is not None else []

    def type(self) -> NodeType:
        return NodeType.BlockStatement
    
    def data(self) -> dict:
        return {
            "type": self.type().value,
            "statements": [stmt.data() for stmt in self.statements]
        }
    
class ReturnStatement(Statement):
    """
    TODO: Add Docstring
    """
    def __init__(self, return_value: Expression = None) -> None:
        self.return_value = return_value

    def type(self) -> NodeType:
        return NodeType.ReturnStatement
    
    def data(self) -> dict:
        return {
            "type": self.type().value,
            "return_value": self.return_value.data(),
        }
    
class FunctionStatement(Statement):
    """
    TODO: Add Docstring
    """
    def __init__(self, parameters: list[FunctionParameter] = [], body: BlockStatement = None, name = None, return_type: str = None) -> None:
        self.parameters = parameters
        self.body = body
        self.name = name
        self.return_type = return_type

    def type(self) -> NodeType:
        return NodeType.FunctionStatement
    
    def data(self) -> dict:
        return {
            "type": self.type().value,
            "name": self.name.data(),
            "return_type": self.return_type,
            "parameters": [p.data() for p in self.parameters],
            "body": self.body.data()
        }

class AssignStatement(Statement):
    """
    TODO: Add Docstring
    """
    def __init__(self, ident: Expression = None, right_value: Expression = None) -> None:
        self.ident = ident
        self.right_value = right_value

    def type(self) -> NodeType:
        return NodeType.AssignStatement
    
    def data(self) -> dict:
        return {
            "type": self.type().value,
            "ident": self.ident.data(),
            "right_value": self.right_value.data()
        }

class IfStatement(Statement):
    """
    TODO: Add Docstring
    """
    def __init__(self, condition: Expression = None, consequence: BlockStatement = None, alternative: BlockStatement = None) -> None:
        self.condition = condition
        self.consequence = consequence
        self.alternative = alternative

    def type(self) -> NodeType:
        return NodeType.IfStatement
    
    def data(self) -> dict:
        return {
            "type": self.type().value,
            "condition": self.condition.data(),
            "consequence": self.consequence.data(),
            "alternative": self.alternative.data(),
        }

# endregion

# region Expressions
class InfixExpression(Expression):
    """
    TODO: Add Docstring
    """
    def __init__(self, left_node: Expression, operator: str, right_node: Expression = None) -> None:
       self.left_node: Expression = left_node
       self.operator: str = operator
       self.right_node: Expression = right_node
    
    def type(self) -> NodeType:
        return NodeType.InfixExpression
    
    def data(self) -> dict:
        return {
            "type": self.type().value,
            "left_node": self.left_node.data(),
            "operator": self.operator,
            "right_node": self.right_node.data()  
        }

class CallExpression(Expression):
    """
    TODO: Add Docstring
    """
    def __init__(self, function: Expression = None, arguments: list[Expression] = None) -> None:
       self.function = function
       self.arguments = arguments
    
    def type(self) -> NodeType:
        return NodeType.CallExpression
    
    def data(self) -> dict:
        return {
            "type": self.type().value,
            "function": self.function.data(),
            "arguments": [arg.data() for arg in self.arguments]
        }
# endregion

# region Literals
class IntegerLiteral(Expression):
    """
    TODO: Add Docstring
    """
    def __init__(self, value: int = None) -> None:
       self.value: int = value
    
    def type(self) -> NodeType:
        return NodeType.IntegerLiteral
    
    def data(self) -> dict:
        return {
            "type": self.type().value,
            "value": self.value
        }

class FloatLiteral(Expression):
    """
    TODO: Add Docstring
    """
    def __init__(self, value: float = None) -> None:
       self.value: int = value
    
    def type(self) -> NodeType:
        return NodeType.FloatLiteral
    
    def data(self) -> dict:
        return {
            "type": self.type().value,
            "value": self.value  
        }

class IdentifierLiteral(Expression):
    """
    TODO: Add Docstring
    """
    def __init__(self, value: str = None) -> None:
       self.value: str = value
    
    def type(self) -> NodeType:
        return NodeType.IdentifierLiteral
    
    def data(self) -> dict:
        return {
            "type": self.type().value,
            "value": self.value
        }

class BooleanLiteral(Expression):
    """
    TODO: Add Docstring
    """
    def __init__(self, value: bool = None) -> None:
       self.value: bool = value
    
    def type(self) -> NodeType:
        return NodeType.BooleanLiteral
    
    def data(self) -> dict:
        return {
            "type": self.type().value,
            "value": self.value
        }
# endregion