import sympy as sp
from typing import Dict, Callable, Any
from ..runtime.kheramat_array import KheraMATArray

def km_syms(*args):
    # Register symbols in sympy context if needed
    symbols = []
    for arg in args:
        name = str(arg._array.item()) if hasattr(arg, "_array") else str(arg)
        symbols.append(sp.Symbol(name))
    if len(symbols) == 1:
        return symbols[0]
    return symbols

def km_diff(expr, var=None, n=1) -> sp.Expr:
    _n = int(n._array.item()) if isinstance(n, KheraMATArray) else int(n)
    if var is None:
        free_vars = list(expr.free_symbols) if hasattr(expr, "free_symbols") else []
        var = free_vars[0] if free_vars else sp.Symbol('x')
    elif hasattr(var, "_array"):
        var = sp.Symbol(str(var._array.item()))
    return sp.diff(expr, var, _n)

def km_int(expr, var=None) -> sp.Expr:
    if var is None:
        free_vars = list(expr.free_symbols) if hasattr(expr, "free_symbols") else []
        var = free_vars[0] if free_vars else sp.Symbol('x')
    elif hasattr(var, "_array"):
        var = sp.Symbol(str(var._array.item()))
    return sp.integrate(expr, var)

SYMBOLIC_FUNCTIONS: Dict[str, Callable] = {
    "syms": km_syms,
    "diff": km_diff,
    "int": km_int,
}

