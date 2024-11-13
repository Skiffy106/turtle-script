# Environment.py
# This file defines an Environment class
from llvmlite import ir

class Environment:
    """
    An Environment used to store the values of variables

    Attributes
    ----------
    records: dict[str, tuple[ir.Value, ir.Type]]
        records is a dictionary that maps variable names to a tuple of the value and type
    parent : Environment | None
        a reference to the parent Environment
    name: str
        the name of the current environment

    Methods
    ----------
    def define(self, name: str, value: ir.Value, __type: ir.Type) -> None:
        defines the variable in the Environment

    def lookup(self, name: str) -> tuple[ir.Value, ir.Type]:
        returns the mapping from the dictionary

    def __resolve(self, name: str) -> tuple[ir.Value, ir.Type]:
        returns the mapping from the current environment and all of its parent environments
    
    """
    def __init__(self, records: dict[str, tuple[ir.Value, ir.Type]] = None, parent = None, name : str  = "global") -> None:
       self.records: dict[str, tuple[ir.Value, ir.Type]] = records if records else {}
       self.parent : Environment | None = parent
       self.name : str = name

    def define(self, name: str, value: ir.Value, __type: ir.Type) -> ir.Value:
        self.records[name] = (value, __type)
        return value

    def lookup(self, name: str) -> tuple[ir.Value, ir.Type]:
        return self.__resolve(name)

    def __resolve(self, name: str) -> tuple[ir.Value, ir.Type]:
        if name in self.records:
            return self.records[name]
        elif self.parent:
            return self.parent.__resolve(name)
        else:
            return None
        
            