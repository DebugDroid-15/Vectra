import pytest
from kheramat.lang.lexer import Lexer, LexerError
from kheramat.lang.tokens import TokenType

def test_lexer_numbers_and_identifiers():
    source = "A = [1 2; 3 4.5]"
    lexer = Lexer(source)
    tokens = lexer.tokenize()

    types = [t.type for t in tokens if t.type != TokenType.EOF]
    assert types == [
        TokenType.IDENTIFIER,
        TokenType.ASSIGN,
        TokenType.LBRACKET,
        TokenType.NUMBER,
        TokenType.NUMBER,
        TokenType.SEMICOLON,
        TokenType.NUMBER,
        TokenType.NUMBER,
        TokenType.RBRACKET
    ]

def test_lexer_dot_operators():
    source = "x .* y ./ z .^ 2 A'"
    lexer = Lexer(source)
    tokens = lexer.tokenize()

    types = [t.type for t in tokens if t.type != TokenType.EOF]
    assert types == [
        TokenType.IDENTIFIER,
        TokenType.DOT_MUL,
        TokenType.IDENTIFIER,
        TokenType.DOT_DIV,
        TokenType.IDENTIFIER,
        TokenType.DOT_POW,
        TokenType.NUMBER,
        TokenType.IDENTIFIER,
        TokenType.TRANSPOSE
    ]

