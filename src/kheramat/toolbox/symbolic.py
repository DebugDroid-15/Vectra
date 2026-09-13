import sympy as sp
from typing import Dict, Callable, Any
from ..runtime.kheramat_array import KheraMATArray

import re

def clean_sym_str(expr: Any) -> str:
    s = str(expr)
    s = re.sub(r'\*\*([0-9\.]+)', r'^\1', s)
    s = re.sub(r'\*\*', r'^', s)
    s = re.sub(r'([0-9]+)\.0(?![0-9])', r'\1', s)
    s = re.sub(r'(\d+)\*([a-zA-Z])', r'\1*\2', s)
    return s

def _to_sympy(expr: Any) -> Any:
    if isinstance(expr, KheraMATArray):
        arr = expr._array
        if arr.size == 1:
            val = arr.item()
            if isinstance(val, (int, float, complex)):
                return sp.sympify(val)
            return sp.Symbol(str(val))
        return sp.Matrix([[_to_sympy(x) for x in row] for row in arr])
    if isinstance(expr, str):
        return sp.sympify(expr)
    return expr

def km_syms(*args):
    symbols = []
    for arg in args:
        name = str(arg._array.item()) if hasattr(arg, "_array") else str(arg)
        symbols.append(sp.Symbol(name))
    if len(symbols) == 1:
        return symbols[0]
    return tuple(symbols)

def km_diff(expr, var=None, n=1):
    sp_expr = _to_sympy(expr)
    _n = int(n._array.item()) if isinstance(n, KheraMATArray) else int(n)
    if var is None:
        free_vars = list(sp_expr.free_symbols) if hasattr(sp_expr, "free_symbols") else []
        sp_var = free_vars[0] if free_vars else sp.Symbol('x')
    else:
        sp_var = _to_sympy(var)
    return sp.diff(sp_expr, sp_var, _n)

def km_int(expr, var=None):
    sp_expr = _to_sympy(expr)
    if var is None:
        free_vars = list(sp_expr.free_symbols) if hasattr(sp_expr, "free_symbols") else []
        sp_var = free_vars[0] if free_vars else sp.Symbol('x')
    else:
        sp_var = _to_sympy(var)
    return sp.integrate(sp_expr, sp_var)

def km_solve(equation, var=None):
    sp_eq = _to_sympy(equation)
    if var is None:
        free_vars = list(sp_eq.free_symbols) if hasattr(sp_eq, "free_symbols") else []
        sp_var = free_vars[0] if free_vars else sp.Symbol('x')
    else:
        sp_var = _to_sympy(var)
    res = sp.solve(sp_eq, sp_var)
    if isinstance(res, list):
        if len(res) > 0 and isinstance(res[0], (int, float, complex, sp.Number)):
            return KheraMATArray([float(x) if isinstance(x, sp.Number) else x for x in res])
        return KheraMATArray(res)
    return res

def km_simplify(expr):
    sp_expr = _to_sympy(expr)
    return sp.simplify(sp_expr)

def km_expand(expr):
    sp_expr = _to_sympy(expr)
    return sp.expand(sp_expr)

def km_factor(expr):
    sp_expr = _to_sympy(expr)
    return sp.factor(sp_expr)

SYMBOLIC_FUNCTIONS: Dict[str, Callable] = {
    "syms": km_syms,
    "diff": km_diff,
    "int": km_int,
    "solve": km_solve,
    "simplify": km_simplify,
    "expand": km_expand,
    "factor": km_factor,
}
