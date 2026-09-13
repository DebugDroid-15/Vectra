from typing import List
from .tokens import Token, TokenType, KEYWORDS

class LexerError(Exception):
    def __init__(self, message: str, line: int, column: int):
        super().__init__(f"Lexer Error at line {line}, column {column}: {message}")
        self.line = line
        self.column = column

class Lexer:
    def __init__(self, source: str):
        self.source = source
        self.pos = 0
        self.line = 1
        self.column = 1
        self.tokens: List[Token] = []

    def _peek(self, offset: int = 0) -> str:
        idx = self.pos + offset
        if idx >= len(self.source):
            return '\0'
        return self.source[idx]

    def _advance(self) -> str:
        ch = self._peek()
        self.pos += 1
        if ch == '\n':
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        return ch

    def tokenize(self) -> List[Token]:
        self.tokens = []
        
        while self.pos < len(self.source):
            ch = self._peek()

            # Skip comments % ...
            if ch == '%':
                while self._peek() not in ('\n', '\0'):
                    self._advance()
                continue

            # Whitespace handling (preserve newlines for command termination)
            if ch in ' \t\r':
                self._advance()
                continue

            if ch == '\n':
                self.tokens.append(Token(TokenType.NEWLINE, '\n', self.line, self.column))
                self._advance()
                continue

            start_line = self.line
            start_col = self.column

            # Numbers: e.g. 10, 3.14, 1e-5, .5
            if ch.isdigit() or (ch == '.' and self._peek(1).isdigit()):
                num_str = ""
                has_dot = False
                has_exp = False

                while True:
                    cur = self._peek()
                    if cur == '.' and not has_dot and not has_exp and self._peek(1) != '*':
                        has_dot = True
                        num_str += self._advance()
                    elif cur in ('e', 'E') and not has_exp:
                        has_exp = True
                        num_str += self._advance()
                        if self._peek() in ('+', '-'):
                            num_str += self._advance()
                    elif cur.isdigit():
                        num_str += self._advance()
                    else:
                        break

                val = float(num_str) if (has_dot or has_exp) else int(num_str)
                self.tokens.append(Token(TokenType.NUMBER, val, start_line, start_col))
                continue

            # Identifiers and Keywords
            if ch.isalpha() or ch == '_':
                ident = ""
                while self._peek().isalnum() or self._peek() == '_':
                    ident += self._advance()
                
                token_type = KEYWORDS.get(ident, TokenType.IDENTIFIER)
                self.tokens.append(Token(token_type, ident, start_line, start_col))
                continue

            # Strings: "hello" or 'hello'
            if ch == '"' or (ch == "'" and not self._is_transpose_context()):
                quote_char = self._advance()
                string_val = ""
                while self._peek() != quote_char and self._peek() != '\0':
                    if self._peek() == '\\':
                        self._advance()
                        nxt = self._advance()
                        if nxt == 'n': string_val += '\n'
                        elif nxt == 't': string_val += '\t'
                        elif nxt in ('\\', '\'', '"'): string_val += nxt
                        else: string_val += '\\' + nxt
                    else:
                        string_val += self._advance()

                if self._peek() == quote_char:
                    self._advance()
                    self.tokens.append(Token(TokenType.STRING, string_val, start_line, start_col))
                    continue
                else:
                    raise LexerError("Unterminated string literal", start_line, start_col)

            # Dot operators: .*, ./, .^, .'
            if ch == '.':
                nxt = self._peek(1)
                if nxt == '*':
                    self._advance(); self._advance()
                    self.tokens.append(Token(TokenType.DOT_MUL, ".*", start_line, start_col))
                    continue
                elif nxt == '/':
                    self._advance(); self._advance()
                    self.tokens.append(Token(TokenType.DOT_DIV, "./", start_line, start_col))
                    continue
                elif nxt == '^':
                    self._advance(); self._advance()
                    self.tokens.append(Token(TokenType.DOT_POW, ".^", start_line, start_col))
                    continue
                elif nxt == "'":
                    self._advance(); self._advance()
                    self.tokens.append(Token(TokenType.DOT_TRANSPOSE, ".'", start_line, start_col))
                    continue
                elif not nxt.isdigit():
                    # Single dot accessor
                    self._advance()
                    self.tokens.append(Token(TokenType.DOT_MUL, ".", start_line, start_col))
                    continue

            # Single quote transpose
            if ch == "'" and self._is_transpose_context():
                self._advance()
                self.tokens.append(Token(TokenType.TRANSPOSE, "'", start_line, start_col))
                continue

            # Two-character operators
            if ch == '=' and self._peek(1) == '=':
                self._advance(); self._advance()
                self.tokens.append(Token(TokenType.EQ, "==", start_line, start_col))
                continue
            if (ch == '~' or ch == '!') and self._peek(1) == '=':
                self._advance(); self._advance()
                self.tokens.append(Token(TokenType.NEQ, "~=", start_line, start_col))
                continue
            if ch == '<' and self._peek(1) == '=':
                self._advance(); self._advance()
                self.tokens.append(Token(TokenType.LTE, "<=", start_line, start_col))
                continue
            if ch == '>' and self._peek(1) == '=':
                self._advance(); self._advance()
                self.tokens.append(Token(TokenType.GTE, ">=", start_line, start_col))
                continue
            if ch == '&' and self._peek(1) == '&':
                self._advance(); self._advance()
                self.tokens.append(Token(TokenType.AND, "&&", start_line, start_col))
                continue
            if ch == '|' and self._peek(1) == '|':
                self._advance(); self._advance()
                self.tokens.append(Token(TokenType.OR, "||", start_line, start_col))
                continue

            # Single character operators and punctuation
            op_map = {
                '+': TokenType.PLUS,
                '-': TokenType.MINUS,
                '*': TokenType.MUL,
                '/': TokenType.DIV,
                '^': TokenType.POW,
                '=': TokenType.ASSIGN,
                '<': TokenType.LT,
                '>': TokenType.GT,
                '~': TokenType.NOT,
                '&': TokenType.AND,
                '|': TokenType.OR,
                '(': TokenType.LPAREN,
                ')': TokenType.RPAREN,
                '[': TokenType.LBRACKET,
                ']': TokenType.RBRACKET,
                '{': TokenType.LBRACE,
                '}': TokenType.RBRACE,
                ',': TokenType.COMMA,
                ';': TokenType.SEMICOLON,
                ':': TokenType.COLON,
            }

            if ch in op_map:
                ttype = op_map[ch]
                self._advance()
                self.tokens.append(Token(ttype, ch, start_line, start_col))
                continue

            raise LexerError(f"Unexpected character: {ch!r}", start_line, start_col)

        self.tokens.append(Token(TokenType.EOF, None, self.line, self.column))
        return self.tokens

    def _is_transpose_context(self) -> bool:
        """Determines if a single quote represents matrix transpose based on preceding token."""
        if not self.tokens:
            return False
        last_tok = self.tokens[-1]
        return last_tok.type in (
            TokenType.IDENTIFIER,
            TokenType.NUMBER,
            TokenType.RPAREN,
            TokenType.RBRACKET,
            TokenType.RBRACE,
            TokenType.TRANSPOSE,
            TokenType.DOT_TRANSPOSE
        )

