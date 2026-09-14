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
    BACKSLASH = auto()      # \
    DOT_BACKSLASH = auto()  # .\
    POW = auto()            # ^
    DOT_POW = auto()        # .^
    TRANSPOSE = auto()      # '
    DOT_TRANSPOSE = auto()  # .'
    DOT = auto()            # .

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
    TRY = auto()
    CATCH = auto()
    SWITCH = auto()
    CASE = auto()
    OTHERWISE = auto()
    GLOBAL = auto()
    PERSISTENT = auto()

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
    "try": TokenType.TRY,
    "catch": TokenType.CATCH,
    "switch": TokenType.SWITCH,
    "case": TokenType.CASE,
    "otherwise": TokenType.OTHERWISE,
    "global": TokenType.GLOBAL,
    "persistent": TokenType.PERSISTENT,
}

class Token:
    def __init__(self, token_type: TokenType, value: Any = None, line: int = 1, column: int = 1, ws_before: bool = False):
        self.type = token_type
        self.value = value
        self.line = line
        self.column = column
        self.ws_before = ws_before

    def __repr__(self) -> str:
        if self.value is not None:
            return f"Token({self.type.name}, {self.value!r}, line={self.line}, col={self.column}, ws={self.ws_before})"
        return f"Token({self.type.name}, line={self.line}, col={self.column}, ws={self.ws_before})"
