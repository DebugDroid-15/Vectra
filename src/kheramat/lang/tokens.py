from enum import Enum, auto
from typing import Any

class TokenType(Enum):
    # Literals
    NUMBER = auto()
    STRING = auto()
    IDENTIFIER = auto()

    # Operators
    PLUS = auto()           # +
    MINUS = auto()          # -
    MUL = auto()            # *
    DOT_MUL = auto()        # .*
    DIV = auto()            # /
    DOT_DIV = auto()        # ./
    POW = auto()            # ^
    DOT_POW = auto()        # .^
    TRANSPOSE = auto()      # '
    DOT_TRANSPOSE = auto()  # .'

    # Assignment & Equality / Comparison
    ASSIGN = auto()         # =
    EQ = auto()             # ==
    NEQ = auto()            # ~= or !=
    LT = auto()             # <
    LTE = auto()            # <=
    GT = auto()             # >
    GTE = auto()            # >=
    AND = auto()            # & or &&
    OR = auto()             # | or ||
    NOT = auto()            # ~

    # Delimiters
    LPAREN = auto()         # (
    RPAREN = auto()         # )
    LBRACKET = auto()       # [
    RBRACKET = auto()       # ]
    LBRACE = auto()         # {
    RBRACE = auto()         # }
    COMMA = auto()          # ,
    SEMICOLON = auto()      # ;
    COLON = auto()          # :
    NEWLINE = auto()        # \n

    # Keywords
    FUNCTION = auto()
    END = auto()
    IF = auto()
    ELSE = auto()
    ELSEIF = auto()
    FOR = auto()
    WHILE = auto()
    RETURN = auto()
    BREAK = auto()
    CONTINUE = auto()

    EOF = auto()

KEYWORDS = {
    "function": TokenType.FUNCTION,
    "end": TokenType.END,
    "if": TokenType.IF,
    "else": TokenType.ELSE,
    "elseif": TokenType.ELSEIF,
    "for": TokenType.FOR,
    "while": TokenType.WHILE,
    "return": TokenType.RETURN,
    "break": TokenType.BREAK,
    "continue": TokenType.CONTINUE,
}

class Token:
    def __init__(self, token_type: TokenType, value: Any = None, line: int = 1, column: int = 1):
        self.type = token_type
        self.value = value
        self.line = line
        self.column = column

    def __repr__(self) -> str:
        if self.value is not None:
            return f"Token({self.type.name}, {self.value!r}, line={self.line}, col={self.column})"
        return f"Token({self.type.name}, line={self.line}, col={self.column})"

