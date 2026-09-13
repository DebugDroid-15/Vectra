from typing import List, Any, Optional

class ASTNode:
    pass

class NumberNode(ASTNode):
    def __init__(self, value: float):
        self.value = value

    def __repr__(self):
        return f"NumberNode({self.value})"

class StringNode(ASTNode):
    def __init__(self, value: str):
        self.value = value

    def __repr__(self):
        return f"StringNode({self.value!r})"

class IdentifierNode(ASTNode):
    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return f"IdentifierNode({self.name})"

class MatrixNode(ASTNode):
    def __init__(self, rows: List[List[ASTNode]]):
        self.rows = rows

    def __repr__(self):
        return f"MatrixNode({self.rows})"

class ColonRangeNode(ASTNode):
    def __init__(self, start: ASTNode, stop: ASTNode, step: Optional[ASTNode] = None):
        self.start = start
        self.stop = stop
        self.step = step

    def __repr__(self):
        return f"ColonRangeNode(start={self.start}, step={self.step}, stop={self.stop})"

class UnaryOpNode(ASTNode):
    def __init__(self, op: str, operand: ASTNode):
        self.op = op
        self.operand = operand

    def __repr__(self):
        return f"UnaryOpNode({self.op}, {self.operand})"

class BinaryOpNode(ASTNode):
    def __init__(self, left: ASTNode, op: str, right: ASTNode):
        self.left = left
        self.op = op
        self.right = right

    def __repr__(self):
        return f"BinaryOpNode({self.left} {self.op} {self.right})"

class IndexingNode(ASTNode):
    def __init__(self, target: ASTNode, indices: List[ASTNode]):
        self.target = target
        self.indices = indices

    def __repr__(self):
        return f"IndexingNode({self.target}, indices={self.indices})"

class MemberAccessNode(ASTNode):
    def __init__(self, obj: ASTNode, member: str):
        self.obj = obj
        self.member = member

    def __repr__(self):
        return f"MemberAccessNode({self.obj}.{self.member})"

class AssignmentNode(ASTNode):
    def __init__(self, target: ASTNode, value: ASTNode, suppress_output: bool = False):
        self.target = target
        self.value = value
        self.suppress_output = suppress_output

    def __repr__(self):
        return f"AssignmentNode({self.target} = {self.value}, suppress={self.suppress_output})"

class CallNode(ASTNode):
    def __init__(self, func_name: str, args: List[ASTNode]):
        self.func_name = func_name
        self.args = args

    def __repr__(self):
        return f"CallNode({self.func_name}, args={self.args})"

class ExpressionStatementNode(ASTNode):
    def __init__(self, expr: ASTNode, suppress_output: bool = False):
        self.expr = expr
        self.suppress_output = suppress_output

    def __repr__(self):
        return f"ExpressionStatementNode({self.expr}, suppress={self.suppress_output})"

class BlockNode(ASTNode):
    def __init__(self, statements: List[ASTNode]):
        self.statements = statements

    def __repr__(self):
        return f"BlockNode({self.statements})"

class IfNode(ASTNode):
    def __init__(self, condition: ASTNode, body: BlockNode, else_body: Optional[BlockNode] = None):
        self.condition = condition
        self.body = body
        self.else_body = else_body

    def __repr__(self):
        return f"IfNode(cond={self.condition})"

class ForNode(ASTNode):
    def __init__(self, var_name: str, range_expr: ASTNode, body: BlockNode):
        self.var_name = var_name
        self.range_expr = range_expr
        self.body = body

    def __repr__(self):
        return f"ForNode(var={self.var_name})"

class WhileNode(ASTNode):
    def __init__(self, condition: ASTNode, body: BlockNode):
        self.condition = condition
        self.body = body

    def __repr__(self):
        return f"WhileNode(cond={self.condition})"

class BreakNode(ASTNode):
    def __repr__(self):
        return "BreakNode()"

class ContinueNode(ASTNode):
    def __repr__(self):
        return "ContinueNode()"

class ReturnNode(ASTNode):
    def __init__(self, return_expr: Optional[ASTNode] = None):
        self.return_expr = return_expr

    def __repr__(self):
        return f"ReturnNode({self.return_expr})"

class FunctionDefNode(ASTNode):
    def __init__(self, name: str, params: List[str], returns: List[str], body: BlockNode):
        self.name = name
        self.params = params
        self.returns = returns
        self.body = body

    def __repr__(self):
        return f"FunctionDefNode(name={self.name}, params={self.params}, returns={self.returns})"

