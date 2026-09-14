from typing import Any, Dict, List, Optional
import numpy as np
from ..lang.ast_nodes import (
    ASTNode, NumberNode, StringNode, IdentifierNode, MatrixNode, ColonRangeNode,
    UnaryOpNode, BinaryOpNode, IndexingNode, MemberAccessNode, AssignmentNode, CallNode,
    ExpressionStatementNode, BlockNode, IfNode, ForNode, WhileNode,
    BreakNode, ContinueNode, ReturnNode, FunctionDefNode
)
from ..lang.lexer import Lexer
from ..lang.parser import Parser
from .kheramat_array import KheraMATArray
from .workspace import Workspace
from ..logger import get_logger
from ..toolbox.core_math import CORE_MATH_FUNCTIONS
from ..toolbox.plotting import PLOTTING_FUNCTIONS
from ..toolbox.signal_processing import SIGNAL_FUNCTIONS
from ..toolbox.dsp import DSP_FUNCTIONS
from ..toolbox.communications import COMMUNICATION_FUNCTIONS
from ..toolbox.electromagnetics import ELECTROMAGNETICS_FUNCTIONS
from ..toolbox.control import CONTROL_FUNCTIONS
from ..toolbox.symbolic import SYMBOLIC_FUNCTIONS

class InterpreterError(Exception):
    def __init__(self, message: str, node: Optional[ASTNode] = None):
        super().__init__(f"Error: {message}")
        self.node = node

class BreakSignal(Exception): pass
class ContinueSignal(Exception): pass
class ReturnSignal(Exception):
    def __init__(self, value: Any = None):
        self.value = value

class Interpreter:
    def __init__(self, workspace: Optional[Workspace] = None):
        self.workspace = workspace or Workspace()
        self.clear_callback = None
        self.functions: Dict[str, Any] = {}
        self.functions.update(CORE_MATH_FUNCTIONS)
        self.functions.update(PLOTTING_FUNCTIONS)
        self.functions.update(SIGNAL_FUNCTIONS)
        self.functions.update(DSP_FUNCTIONS)
        self.functions.update(COMMUNICATION_FUNCTIONS)
        self.functions.update(ELECTROMAGNETICS_FUNCTIONS)
        self.functions.update(CONTROL_FUNCTIONS)
        self.functions.update(SYMBOLIC_FUNCTIONS)
        self.functions["clear"] = self._cmd_clear
        self.functions["clc"] = self._cmd_clc
        self.functions["help"] = self._cmd_help
        self.functions["doc"] = self._cmd_doc

    def _cmd_help(self, *args):
        from ..help_docs import get_help_text
        if not args:
            return get_help_text("plot")
        topic = str(args[0]._array.item() if hasattr(args[0], "_array") else args[0])
        return get_help_text(topic)

    def _cmd_doc(self, *args):
        from ..help_docs import open_doc_url
        if not args:
            return open_doc_url("plot")
        topic = str(args[0]._array.item() if hasattr(args[0], "_array") else args[0])
        return open_doc_url(topic)

    def _cmd_clear(self, *args):
        if not args:
            self.workspace.clear()
        else:
            for arg in args:
                var_name = str(arg._array.item()) if hasattr(arg, "_array") else str(arg)
                self.workspace.clear(var_name)
        return None

    def _cmd_clc(self, *args):
        if self.clear_callback:
            self.clear_callback()
        return None

    def eval_code(self, source_code: str) -> List[str]:
        logger = get_logger("runtime.interpreter")
        logger.debug(f"Evaluating source code block ({len(source_code)} chars)")
        try:
            lexer = Lexer(source_code)
            tokens = lexer.tokenize()
            parser = Parser(tokens)
            ast = parser.parse()
            res = self.eval_block(ast)
            return res
        except Exception as e:
            logger.error(f"Execution error evaluating code: {e}", exc_info=True)
            raise

    def eval_block(self, block: BlockNode) -> List[str]:
        output_logs = []
        for stmt in block.statements:
            res = self.visit(stmt)
            if res is not None:
                output_logs.append(res)
        return output_logs

    def visit(self, node: ASTNode) -> Any:
        method_name = f"visit_{type(node).__name__}"
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node: ASTNode):
        raise InterpreterError(f"No visit_{type(node).__name__} method defined for AST node {node}")

    def visit_NumberNode(self, node: NumberNode) -> KheraMATArray:
        return KheraMATArray(node.value)

    def visit_StringNode(self, node: StringNode) -> str:
        return node.value

    def visit_IdentifierNode(self, node: IdentifierNode) -> Any:
        if self.workspace.has(node.name):
            return self.workspace.get(node.name)
        if node.name in self.functions:
            return self.functions[node.name]()
        raise InterpreterError(f"Undefined function or variable '{node.name}'.")

    def visit_MatrixNode(self, node: MatrixNode) -> KheraMATArray:
        evaluated_rows = []
        for row in node.rows:
            row_vals = []
            for item in row:
                val = self.visit(item)
                if isinstance(val, KheraMATArray):
                    row_vals.extend(val._array.flatten())
                else:
                    row_vals.append(val)
            evaluated_rows.append(row_vals)
        return KheraMATArray(np.array(evaluated_rows))

    def visit_ColonRangeNode(self, node: ColonRangeNode) -> KheraMATArray:
        start_val = float(self.visit(node.start)._array.item())
        stop_val = float(self.visit(node.stop)._array.item())

        if node.step is not None:
            step_val = float(self.visit(node.step)._array.item())
        else:
            step_val = 1.0

        arr = np.arange(start_val, stop_val + step_val/2.0, step_val)
        return KheraMATArray(arr.reshape((1, -1)))

    def visit_UnaryOpNode(self, node: UnaryOpNode) -> Any:
        val = self.visit(node.operand)
        if node.op == '-':
            return -val
        elif node.op == '+':
            return val
        elif node.op in ("'", ".'"):
            if isinstance(val, KheraMATArray):
                return val.transpose() if node.op == "'" else val.dot_transpose()
        raise InterpreterError(f"Unsupported unary operator '{node.op}'")

    def visit_BinaryOpNode(self, node: BinaryOpNode) -> Any:
        left = self.visit(node.left)
        right = self.visit(node.right)

        if isinstance(left, KheraMATArray) and isinstance(right, KheraMATArray):
            if node.op == '+': return left + right
            elif node.op == '-': return left - right
            elif node.op == '*': return left.matmul(right)
            elif node.op == '.*': return left.dot_mul(right)
            elif node.op == '/': return left.matdiv(right)
            elif node.op == './': return left.dot_div(right)
            elif node.op == '^': return left.matpow(right)
            elif node.op == '.^': return left.dot_pow(right)
            elif node.op == '==': return left == right
            elif node.op == '~=': return left != right
            elif node.op == '<': return left < right
            elif node.op == '<=': return left <= right
            elif node.op == '>': return left > right
            elif node.op == '>=': return left >= right
            elif node.op in ('&', '&&'): return left & right
            elif node.op in ('|', '||'): return left | right

        # Fallback for SymPy or generic objects
        if hasattr(right, "_array") and isinstance(right, KheraMATArray):
            right = right._array.item() if right._array.size == 1 else right._array
        if hasattr(left, "_array") and isinstance(left, KheraMATArray):
            left = left._array.item() if left._array.size == 1 else left._array

        import sympy as sp
        if isinstance(left, sp.Basic) or isinstance(right, sp.Basic):
            if node.op == '==': return sp.Eq(left, right)
            elif node.op == '~=': return sp.Ne(left, right)

        if node.op == '+': return left + right
        elif node.op == '-': return left - right
        elif node.op in ('*', '.*'): return left * right
        elif node.op in ('/', './'): return left / right
        elif node.op in ('^', '.^'): return left ** right
        elif node.op == '==': return left == right
        elif node.op == '~=': return left != right
        elif node.op in ('&', '&&'): return bool(left and right)
        elif node.op in ('|', '||'): return bool(left or right)

        raise InterpreterError(f"Unsupported binary operator '{node.op}'")

    def visit_AssignmentNode(self, node: AssignmentNode) -> Optional[str]:
        val = self.visit(node.value)
        import sympy as sp
        from ..toolbox.symbolic import clean_sym_str
        if isinstance(node.target, IdentifierNode):
            name = node.target.name
            self.workspace.set(name, val)
            if not node.suppress_output:
                formatted_val = clean_sym_str(val) if isinstance(val, sp.Basic) else str(val)
                return f"\n{name} =\n\n{formatted_val}\n"
        elif isinstance(node.target, (IndexingNode, CallNode)):
            if isinstance(node.target, IndexingNode):
                target_name = node.target.target.name if isinstance(node.target.target, IdentifierNode) else None
                raw_indices = node.target.indices
                target_arr = self.visit(node.target.target)
            else:
                target_name = node.target.func_name
                raw_indices = node.target.args
                target_arr = self.workspace.get(target_name)

            idx_vals = [self.visit(i) if not (isinstance(i, StringNode) and i.value == ":") else ":" for i in raw_indices]
            target_arr.set_index(val, *idx_vals)
            if target_name:
                self.workspace.set(target_name, target_arr)
                if not node.suppress_output:
                    return f"\n{target_name} =\n\n{target_arr}\n"
        elif isinstance(node.target, MatrixNode):
            # Multiple output assignment: [a, b] = expr or [a, b, c] = expr
            targets = []
            for row in node.target.rows:
                for item in row:
                    if isinstance(item, IdentifierNode):
                        targets.append(item.name)
                    else:
                        raise InterpreterError("Invalid target in multi-variable assignment.")
            if isinstance(val, tuple):
                out_str = []
                # Map available returned outputs to target variables
                for name, v in zip(targets, val):
                    self.workspace.set(name, v)
                    if not node.suppress_output:
                        out_str.append(f"\n{name} =\n\n{v}\n")
                return "".join(out_str) if out_str else None
            else:
                self.workspace.set(targets[0], val)
                if not node.suppress_output:
                    return f"\n{targets[0]} =\n\n{val}\n"
                return None
        return None

    def visit_MemberAccessNode(self, node: MemberAccessNode) -> Any:
        obj = self.visit(node.obj)
        if hasattr(obj, node.member):
            return getattr(obj, node.member)
        elif isinstance(obj, dict) and node.member in obj:
            return obj[node.member]
        raise InterpreterError(f"Object {obj} has no member '{node.member}'")

    def visit_CallNode(self, node: CallNode) -> Any:
        args = [self.visit(arg) for arg in node.args]

    def visit_BreakNode(self, node: BreakNode):
        raise BreakSignal()

    def visit_ContinueNode(self, node: ContinueNode):
        raise ContinueSignal()

    def visit_ReturnNode(self, node: ReturnNode):
        val = self.visit(node.return_expr) if node.return_expr else None
        raise ReturnSignal(val)

    def visit_FunctionDefNode(self, node: FunctionDefNode):
        def user_func(*args):
            old_workspace = self.workspace
            local_ws = Workspace()
            # Bind parameters
            for p_name, arg_val in zip(node.params, args):
                local_ws.set(p_name, arg_val)
            self.workspace = local_ws
            try:
                self.eval_block(node.body)
            except ReturnSignal as ret:
                pass
            finally:
                res_vals = []
                for ret_name in node.returns:
                    if local_ws.has(ret_name):
                        res_vals.append(local_ws.get(ret_name))
                self.workspace = old_workspace

            if len(res_vals) == 0:
                return None
            elif len(res_vals) == 1:
                return res_vals[0]
            return tuple(res_vals)

        self.functions[node.name] = user_func
        return None

    def visit_CallNode(self, node: CallNode) -> Any:
        if node.func_name == "syms":
            import sympy as sp
            created = []
            for arg_node in node.args:
                sym_name = arg_node.name if isinstance(arg_node, IdentifierNode) else str(arg_node.value)
                sym_obj = sp.Symbol(sym_name)
                self.workspace.set(sym_name, sym_obj)
                created.append(sym_obj)
            return created[0] if len(created) == 1 else tuple(created)

        args = [self.visit(arg) for arg in node.args]

        if self.workspace.has(node.func_name):
            val = self.workspace.get(node.func_name)
            if isinstance(val, KheraMATArray):
                return val.get_index(*args)

        if node.func_name in self.functions:
            func = self.functions[node.func_name]
            return func(*args)

        # Dynamic fallback for NumPy and SciPy functions
        if hasattr(np, node.func_name):
            raw_args = [a._array if isinstance(a, KheraMATArray) else a for a in args]
            res = getattr(np, node.func_name)(*raw_args)
            if isinstance(res, np.ndarray):
                return KheraMATArray(res)
            elif isinstance(res, (int, float, complex, np.number)):
                return KheraMATArray(res)
            return res

        import scipy.linalg as la
        if hasattr(la, node.func_name):
            raw_args = [a._array if isinstance(a, KheraMATArray) else a for a in args]
            res = getattr(la, node.func_name)(*raw_args)
            if isinstance(res, np.ndarray):
                return KheraMATArray(res)
            elif isinstance(res, (int, float, complex, np.number)):
                return KheraMATArray(res)
            return res

        raise InterpreterError(f"Undefined function or variable '{node.func_name}'.")

    def visit_IndexingNode(self, node: IndexingNode) -> Any:
        idx_vals = [self.visit(i) if not (isinstance(i, StringNode) and i.value == ":") else ":" for i in node.indices]
        if isinstance(node.target, IdentifierNode):
            func_name = node.target.name
            if self.workspace.has(func_name):
                val = self.workspace.get(func_name)
                if isinstance(val, KheraMATArray):
                    return val.get_index(*idx_vals)
                elif isinstance(val, (int, float, complex, np.number, np.ndarray)):
                    return KheraMATArray(val).get_index(*idx_vals)
                elif isinstance(val, (list, tuple)):
                    if len(idx_vals) == 1:
                        idx = idx_vals[0]
                        py_idx = int(idx._array.item() if isinstance(idx, KheraMATArray) else idx) - 1
                        elem = val[py_idx]
                        return KheraMATArray(elem) if isinstance(elem, (int, float, complex, np.number, np.ndarray)) else elem
            if func_name in self.functions:
                func = self.functions[func_name]
                return func(*idx_vals)
            if hasattr(np, func_name):
                raw_args = [a._array if isinstance(a, KheraMATArray) else a for a in idx_vals]
                res = getattr(np, func_name)(*raw_args)
                if isinstance(res, np.ndarray):
                    return KheraMATArray(res)
                elif isinstance(res, (int, float, complex, np.number)):
                    return KheraMATArray(res)
                return res
        target = self.visit(node.target)
        if isinstance(target, KheraMATArray):
            return target.get_index(*idx_vals)
        elif isinstance(target, (int, float, complex, np.number, np.ndarray)):
            return KheraMATArray(target).get_index(*idx_vals)
        elif isinstance(target, (list, tuple)):
            if len(idx_vals) == 1:
                idx = idx_vals[0]
                py_idx = int(idx._array.item() if isinstance(idx, KheraMATArray) else idx) - 1
                elem = target[py_idx]
                return KheraMATArray(elem) if isinstance(elem, (int, float, complex, np.number, np.ndarray)) else elem
        raise InterpreterError("Indexing standard non-array object is invalid.")

    def visit_ExpressionStatementNode(self, node: ExpressionStatementNode) -> Optional[str]:
        val = self.visit(node.expr)
        if val is not None and not node.suppress_output:
            self.workspace.set("ans", val)
            import sympy as sp
            from ..toolbox.symbolic import clean_sym_str
            formatted_val = clean_sym_str(val) if isinstance(val, sp.Basic) else str(val)
            return f"\nans =\n\n{formatted_val}\n"
        return None

    def visit_IfNode(self, node: IfNode) -> Optional[str]:
        cond_val = self.visit(node.condition)
        is_true = bool(np.all(cond_val._array)) if isinstance(cond_val, KheraMATArray) else bool(cond_val)
        if is_true:
            return "\n".join(filter(None, self.eval_block(node.body)))
        elif node.else_body:
            return "\n".join(filter(None, self.eval_block(node.else_body)))
        return None

    def visit_ForNode(self, node: ForNode) -> Optional[str]:
        range_val = self.visit(node.range_expr)
        items = range_val._array.flatten() if isinstance(range_val, KheraMATArray) else range_val
        logs = []
        for item in items:
            self.workspace.set(node.var_name, KheraMATArray(item))
            try:
                res = self.eval_block(node.body)
                logs.extend(filter(None, res))
            except BreakSignal:
                break
            except ContinueSignal:
                continue
        return "\n".join(logs) if logs else None

    def visit_WhileNode(self, node: WhileNode) -> Optional[str]:
        logs = []
        while True:
            cond_val = self.visit(node.condition)
            is_true = bool(np.all(cond_val._array)) if isinstance(cond_val, KheraMATArray) else bool(cond_val)
            if not is_true:
                break
            try:
                res = self.eval_block(node.body)
                logs.extend(filter(None, res))
            except BreakSignal:
                break
            except ContinueSignal:
                continue
        return "\n".join(logs) if logs else None
