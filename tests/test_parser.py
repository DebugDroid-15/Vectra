import pytest
from kheramat.lang.lexer import Lexer
from kheramat.lang.parser import Parser
from kheramat.lang.ast_nodes import (
    AssignmentNode, BinaryOpNode, MatrixNode, ColonRangeNode, NumberNode
)

def test_parser_matrix_assignment():
    source = "A = [1 2; 3 4];"
    tokens = Lexer(source).tokenize()
    ast = Parser(tokens).parse()

    assert len(ast.statements) == 1
    stmt = ast.statements[0]
    assert isinstance(stmt, AssignmentNode)
    assert stmt.target.name == "A"
    assert stmt.suppress_output == True
    assert isinstance(stmt.value, MatrixNode)

def test_parser_colon_range():
    source = "x = 0:0.1:10"
    tokens = Lexer(source).tokenize()
    ast = Parser(tokens).parse()

    stmt = ast.statements[0]
    assert isinstance(stmt, AssignmentNode)
    assert isinstance(stmt.value, ColonRangeNode)
    assert stmt.value.start.value == 0
    assert stmt.value.step.value == 0.1
    assert stmt.value.stop.value == 10

