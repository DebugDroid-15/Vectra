from typing import List, Optional
from .tokens import Token, TokenType
from .ast_nodes import (
    ASTNode, NumberNode, StringNode, IdentifierNode, MatrixNode, ColonRangeNode,
    UnaryOpNode, BinaryOpNode, IndexingNode, MemberAccessNode, AssignmentNode, CallNode,
    ExpressionStatementNode, BlockNode, IfNode, ForNode, WhileNode,
    BreakNode, ContinueNode, ReturnNode, FunctionDefNode
)

class ParserError(Exception):
    def __init__(self, message: str, token: Optional[Token] = None):
        if token:
            super().__init__(f"Parser Error at line {token.line}, column {token.column}: {message} (got {token.type.name})")
        else:
            super().__init__(f"Parser Error: {message}")
        self.token = token

class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0
        self.in_matrix_row = False

    def _peek(self, offset: int = 0) -> Token:
        idx = self.pos + offset
        if idx >= len(self.tokens):
            return self.tokens[-1]
        return self.tokens[idx]

    def _advance(self) -> Token:
        tok = self._peek()
        if tok.type != TokenType.EOF:
            self.pos += 1
        return tok

    def _match(self, *types: TokenType) -> bool:
        if self._peek().type in types:
            self._advance()
            return True
        return False

    def _expect(self, expected_type: TokenType, message: str = "") -> Token:
        tok = self._peek()
        if tok.type == expected_type:
            return self._advance()
        raise ParserError(message or f"Expected {expected_type.name}", tok)

    def parse(self) -> BlockNode:
        statements = []
        fn_defs = []
        while self._peek().type != TokenType.EOF:
            if self._match(TokenType.NEWLINE, TokenType.SEMICOLON):
                continue
            stmt = self.parse_statement()
            if stmt:
                if isinstance(stmt, FunctionDefNode):
                    fn_defs.append(stmt)
                else:
                    statements.append(stmt)
        return BlockNode(fn_defs + statements)

    def parse_statement(self) -> Optional[ASTNode]:
        tok = self._peek()

        if tok.type == TokenType.IF:
            return self.parse_if_statement()
        if tok.type == TokenType.FOR:
            return self.parse_for_statement()
        if tok.type == TokenType.WHILE:
            return self.parse_while_statement()
        if tok.type == TokenType.BREAK:
            self._advance()
            self._match_statement_terminator()
            return BreakNode()
        if tok.type == TokenType.CONTINUE:
            self._advance()
            self._match_statement_terminator()
            return ContinueNode()
        if tok.type == TokenType.RETURN:
            self._advance()
            self._match_statement_terminator()
            return ReturnNode()
        if tok.type == TokenType.FUNCTION:
            return self.parse_function_definition()

        # MATLAB Command Syntax: e.g. grid on, hold on, clear x y, help fft, close all
        if tok.type == TokenType.IDENTIFIER:
            nxt = self._peek(1)
            if nxt.type in (TokenType.IDENTIFIER, TokenType.STRING, TokenType.NUMBER) and nxt.line == tok.line:
                func_name = self._advance().value
                cmd_args = []
                while self._peek().type in (TokenType.IDENTIFIER, TokenType.STRING, TokenType.NUMBER) and self._peek().line == tok.line:
                    arg_tok = self._advance()
                    cmd_args.append(StringNode(str(arg_tok.value)))
                suppress = self._match_statement_terminator()
                return ExpressionStatementNode(CallNode(func_name, cmd_args), suppress_output=suppress)

        expr = self.parse_expression()
        if expr is None:
            return None

        # Check for assignment target
        if self._peek().type == TokenType.ASSIGN:
            self._advance()
            val = self.parse_expression()
            suppress = self._match_statement_terminator()
            return AssignmentNode(expr, val, suppress_output=suppress)

        suppress = self._match_statement_terminator()
        return ExpressionStatementNode(expr, suppress_output=suppress)

    def _match_statement_terminator(self) -> bool:
        suppress = False
        while self._peek().type in (TokenType.SEMICOLON, TokenType.NEWLINE, TokenType.COMMA):
            tok = self._advance()
            if tok.type == TokenType.SEMICOLON:
                suppress = True
        return suppress

    def parse_if_statement(self) -> IfNode:
        self._expect(TokenType.IF)
        condition = self.parse_expression()
        self._match_statement_terminator()

        body_stmts = []
        else_stmts = []
        in_else = False

        while self._peek().type not in (TokenType.END, TokenType.EOF):
            if self._match(TokenType.NEWLINE, TokenType.SEMICOLON):
                continue
            if self._match(TokenType.ELSE):
                in_else = True
                self._match_statement_terminator()
                continue

            stmt = self.parse_statement()
            if stmt:
                if in_else: else_stmts.append(stmt)
                else: body_stmts.append(stmt)

        self._expect(TokenType.END, "Expected 'end' at termination of if block")
        else_block = BlockNode(else_stmts) if else_stmts else None
        return IfNode(condition, BlockNode(body_stmts), else_block)

    def parse_for_statement(self) -> ForNode:
        self._expect(TokenType.FOR)
        var_tok = self._expect(TokenType.IDENTIFIER, "Expected loop variable name")
        self._expect(TokenType.ASSIGN, "Expected '=' in for loop")
        range_expr = self.parse_expression()
        self._match_statement_terminator()

        body_stmts = []
        while self._peek().type not in (TokenType.END, TokenType.EOF):
            if self._match(TokenType.NEWLINE, TokenType.SEMICOLON):
                continue
            stmt = self.parse_statement()
            if stmt: body_stmts.append(stmt)

        self._expect(TokenType.END, "Expected 'end' at termination of for block")
        return ForNode(var_tok.value, range_expr, BlockNode(body_stmts))

    def parse_while_statement(self) -> WhileNode:
        self._expect(TokenType.WHILE)
        condition = self.parse_expression()
        self._match_statement_terminator()

        body_stmts = []
        while self._peek().type not in (TokenType.END, TokenType.EOF):
            if self._match(TokenType.NEWLINE, TokenType.SEMICOLON):
                continue
            stmt = self.parse_statement()
            if stmt: body_stmts.append(stmt)

        self._expect(TokenType.END, "Expected 'end' at termination of while block")
        return WhileNode(condition, BlockNode(body_stmts))

    def parse_function_definition(self) -> FunctionDefNode:
        self._expect(TokenType.FUNCTION)
        returns = []
        
        # Check if function has return values: function y = f(x) or function [a, b] = f(x)
        if self._peek().type == TokenType.LBRACKET:
            self._advance()
            while self._peek().type != TokenType.RBRACKET and self._peek().type != TokenType.EOF:
                if self._peek().type == TokenType.IDENTIFIER:
                    returns.append(self._advance().value)
                elif self._peek().type in (TokenType.COMMA, TokenType.SEMICOLON):
                    self._advance()
                else:
                    break
            self._expect(TokenType.RBRACKET)
            self._expect(TokenType.ASSIGN)
        elif self._peek().type == TokenType.IDENTIFIER and self._peek(1).type == TokenType.ASSIGN:
            returns.append(self._advance().value)
            self._expect(TokenType.ASSIGN)

        func_name_tok = self._expect(TokenType.IDENTIFIER, "Expected function name")
        params = []
        if self._match(TokenType.LPAREN):
            if self._peek().type != TokenType.RPAREN:
                while True:
                    param_tok = self._expect(TokenType.IDENTIFIER, "Expected parameter name")
                    params.append(param_tok.value)
                    if not self._match(TokenType.COMMA):
                        break
            self._expect(TokenType.RPAREN)

        self._match_statement_terminator()

        body_stmts = []
        while self._peek().type not in (TokenType.END, TokenType.EOF):
            if self._match(TokenType.NEWLINE, TokenType.SEMICOLON):
                continue
            stmt = self.parse_statement()
            if stmt: body_stmts.append(stmt)

        self._expect(TokenType.END, "Expected 'end' at termination of function block")
        return FunctionDefNode(func_name_tok.value, params, returns, BlockNode(body_stmts))

    def parse_expression(self) -> ASTNode:
        return self.parse_colon_range()

    def parse_colon_range(self) -> ASTNode:
        left = self.parse_logical_or()
        if self._peek().type == TokenType.COLON:
            self._advance()
            if self._peek().type in (TokenType.COMMA, TokenType.RPAREN, TokenType.RBRACKET, TokenType.SEMICOLON):
                return ColonRangeNode(start=left, stop=StringNode(":"))
            second = self.parse_logical_or()
            if self._peek().type == TokenType.COLON:
                self._advance()
                third = self.parse_logical_or()
                return ColonRangeNode(start=left, step=second, stop=third)
            return ColonRangeNode(start=left, stop=second)
        return left

    def parse_logical_or(self) -> ASTNode:
        left = self.parse_logical_and()
        while self._peek().type == TokenType.OR:
            op_tok = self._advance()
            right = self.parse_logical_and()
            left = BinaryOpNode(left, op_tok.value, right)
        return left

    def parse_logical_and(self) -> ASTNode:
        left = self.parse_equality()
        while self._peek().type == TokenType.AND:
            op_tok = self._advance()
            right = self.parse_equality()
            left = BinaryOpNode(left, op_tok.value, right)
        return left

    def parse_equality(self) -> ASTNode:
        left = self.parse_relational()
        while self._peek().type in (TokenType.EQ, TokenType.NEQ):
            op_tok = self._advance()
            right = self.parse_relational()
            left = BinaryOpNode(left, op_tok.value, right)
        return left

    def parse_relational(self) -> ASTNode:
        left = self.parse_additive()
        while self._peek().type in (TokenType.LT, TokenType.LTE, TokenType.GT, TokenType.GTE):
            op_tok = self._advance()
            right = self.parse_additive()
            left = BinaryOpNode(left, op_tok.value, right)
        return left

    def parse_additive(self) -> ASTNode:
        left = self.parse_multiplicative()
        while self._peek().type in (TokenType.PLUS, TokenType.MINUS):
            op_tok = self._peek()
            next_tok = self._peek(1)
            
            # MATLAB matrix literal spacing semantics:
            # [1 -6] -> 1, -6 (op has space before, but no space after -> unary)
            # [1 - 6] -> -5 (op has space before and after -> binary)
            # [1-6] -> -5 (op has no space before or after -> binary)
            if self.in_matrix_row and op_tok.ws_before and not next_tok.ws_before:
                break
                
            self._advance()
            right = self.parse_multiplicative()
            left = BinaryOpNode(left, op_tok.value, right)
        return left

    def parse_multiplicative(self) -> ASTNode:
        left = self.parse_power()
        while self._peek().type in (TokenType.MUL, TokenType.DOT_MUL, TokenType.DIV, TokenType.DOT_DIV):
            op_tok = self._advance()
            right = self.parse_power()
            left = BinaryOpNode(left, op_tok.value, right)
        return left

    def parse_power(self) -> ASTNode:
        left = self.parse_unary()
        while self._peek().type in (TokenType.POW, TokenType.DOT_POW):
            op_tok = self._advance()
            right = self.parse_unary()
            left = BinaryOpNode(left, op_tok.value, right)
        return left

    def parse_unary(self) -> ASTNode:
        if self._peek().type in (TokenType.PLUS, TokenType.MINUS, TokenType.NOT):
            op_tok = self._advance()
            operand = self.parse_unary()
            return UnaryOpNode(op_tok.value, operand)
        return self.parse_postfix()

    def parse_postfix(self) -> ASTNode:
        expr = self.parse_primary()
        while True:
            if self._peek().type in (TokenType.TRANSPOSE, TokenType.DOT_TRANSPOSE):
                op_tok = self._advance()
                expr = UnaryOpNode(op_tok.value, expr)
            elif self._peek().type == TokenType.DOT:
                self._advance()
                member_tok = self._expect(TokenType.IDENTIFIER, "Expected member name after '.'")
                expr = MemberAccessNode(expr, member_tok.value)
            elif self._peek().type == TokenType.LPAREN:
                self._advance()
                args = []
                if self._peek().type != TokenType.RPAREN:
                    while True:
                        if self._peek().type == TokenType.COLON and self._peek(1).type in (TokenType.COMMA, TokenType.RPAREN):
                            self._advance()
                            args.append(StringNode(":"))
                        else:
                            args.append(self.parse_expression())
                        if not self._match(TokenType.COMMA):
                            break
                self._expect(TokenType.RPAREN, "Expected ')'")
                expr = IndexingNode(expr, args)
            else:
                break
        return expr

    def parse_primary(self) -> ASTNode:
        tok = self._peek()

        if tok.type == TokenType.NUMBER:
            self._advance()
            return NumberNode(tok.value)

        if tok.type == TokenType.STRING:
            self._advance()
            return StringNode(tok.value)

        if tok.type == TokenType.IDENTIFIER:
            self._advance()
            return IdentifierNode(tok.value)

        if tok.type == TokenType.LPAREN:
            self._advance()
            expr = self.parse_expression()
            self._expect(TokenType.RPAREN, "Expected closing ')'")
            return expr

        if tok.type == TokenType.LBRACKET:
            return self.parse_matrix_literal()

        raise ParserError("Unexpected expression token", tok)

    def parse_matrix_literal(self) -> MatrixNode:
        self._expect(TokenType.LBRACKET)
        rows: List[List[ASTNode]] = []
        current_row: List[ASTNode] = []

        while self._peek().type != TokenType.RBRACKET and self._peek().type != TokenType.EOF:
            if self._match(TokenType.SEMICOLON) or self._match(TokenType.NEWLINE):
                if current_row:
                    rows.append(current_row)
                    current_row = []
                continue

            # Special case for discard placeholder [~, x] in assignment
            if self._peek().type == TokenType.NOT and self._peek(1).type in (TokenType.COMMA, TokenType.RBRACKET, TokenType.SEMICOLON, TokenType.NEWLINE):
                self._advance()
                elem = IdentifierNode("~")
                current_row.append(elem)
            else:
                old_in_matrix = self.in_matrix_row
                self.in_matrix_row = True
                elem = self.parse_expression()
                self.in_matrix_row = old_in_matrix
                current_row.append(elem)

            self._match(TokenType.COMMA)

        if current_row:
            rows.append(current_row)

        self._expect(TokenType.RBRACKET, "Expected closing ']' in matrix construction")
        return MatrixNode(rows)
