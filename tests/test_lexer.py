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

def test_lexer_backslash_operators():
    source = "A \\ b; x .\\ y"
    lexer = Lexer(source)
    tokens = lexer.tokenize()

    types = [t.type for t in tokens if t.type != TokenType.EOF]
    assert types == [
        TokenType.IDENTIFIER,
        TokenType.BACKSLASH,
        TokenType.IDENTIFIER,
        TokenType.SEMICOLON,
        TokenType.IDENTIFIER,
        TokenType.DOT_BACKSLASH,
        TokenType.IDENTIFIER,
    ]

def test_lexer_string_escapes():
    source = r"""
s1 = 'hello\nworld';
s2 = 'tab\there';
s3 = 'Path: C:\\PROJECTS\\MATLAB';
s4 = 'It\'s working';
s5 = 'It''s matlab style';
s6 = "Double \"quote\"";
"""
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    string_tokens = [t.value for t in tokens if t.type == TokenType.STRING]

    assert string_tokens[0] == "hello\nworld"
    assert string_tokens[1] == "tab\there"
    assert string_tokens[2] == "Path: C:\\PROJECTS\\MATLAB"
    assert string_tokens[3] == "It's working"
    assert string_tokens[4] == "It's matlab style"
    assert string_tokens[5] == 'Double "quote"'


