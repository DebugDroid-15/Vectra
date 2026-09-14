import sys
import numpy as np
from typing import Dict, Callable, Any
from ..runtime.kheramat_array import KheraMATArray

def _to_arr(val: Any) -> np.ndarray:
    if isinstance(val, KheraMATArray):
        return val._array
    return np.array(val)

def _parse_dims(*args) -> tuple:
    if not args:
        return (1, 1)
    if len(args) == 1:
        a = _to_arr(args[0])
        if a.size > 1:
            shape = tuple(a.flatten().astype(int))
            return shape if len(shape) >= 2 else (1, shape[0])
        else:
            dim = int(a.item())
            return (dim, dim)
    dims = [int(_to_arr(a).item()) for a in args]
    return tuple(dims)

def km_zeros(*args) -> KheraMATArray:
    shape = _parse_dims(*args)
    return KheraMATArray(np.zeros(shape))

def km_ones(*args) -> KheraMATArray:
    shape = _parse_dims(*args)
    return KheraMATArray(np.ones(shape))

def km_eye(*args) -> KheraMATArray:
    if len(args) == 1:
        a = _to_arr(args[0])
        if a.size > 1:
            shape = a.flatten().astype(int)
            return KheraMATArray(np.eye(shape[0], shape[1] if len(shape) > 1 else shape[0]))
        return KheraMATArray(np.eye(int(a.item())))
    r, c = int(_to_arr(args[0]).item()), int(_to_arr(args[1]).item())
    return KheraMATArray(np.eye(r, c))

def km_rand(*args) -> KheraMATArray:
    shape = _parse_dims(*args)
    return KheraMATArray(np.random.rand(*shape))

def km_randn(*args) -> KheraMATArray:
    shape = _parse_dims(*args)
    return KheraMATArray(np.random.randn(*shape))

def km_linspace(start, stop, num=100) -> KheraMATArray:
    st = float(_to_arr(start).item() if isinstance(start, KheraMATArray) else start)
    sp = float(_to_arr(stop).item() if isinstance(stop, KheraMATArray) else stop)
    n = int(_to_arr(num).item() if isinstance(num, KheraMATArray) else num)
    return KheraMATArray(np.linspace(st, sp, n).reshape((1, -1)))

# Dimension & Inspection
def km_size(arr) -> KheraMATArray: return KheraMATArray(np.array(_to_arr(arr).shape))
def km_length(arr) -> KheraMATArray:
    a = _to_arr(arr)
    if a.size == 0:
        return KheraMATArray(0)
    return KheraMATArray(max(a.shape) if a.shape else 1)
def km_numel(arr) -> KheraMATArray: return KheraMATArray(_to_arr(arr).size)

# Linear Algebra
def km_det(arr) -> KheraMATArray: return KheraMATArray(np.linalg.det(_to_arr(arr)))
def km_inv(arr) -> KheraMATArray: return KheraMATArray(np.linalg.inv(_to_arr(arr)))
def km_pinv(arr) -> KheraMATArray: return KheraMATArray(np.linalg.pinv(_to_arr(arr)))
def km_eig(arr) -> tuple:
    a = _to_arr(arr)
    w, v = np.linalg.eig(a)
    V = KheraMATArray(v)
    D = KheraMATArray(np.diag(w))
    return (V, D)
def km_norm(arr) -> KheraMATArray: return KheraMATArray(np.linalg.norm(_to_arr(arr)))
def km_trace(arr) -> KheraMATArray: return KheraMATArray(np.trace(_to_arr(arr)))
def km_rank(arr) -> KheraMATArray: return KheraMATArray(np.linalg.matrix_rank(_to_arr(arr)))

def _math_op(np_func, sp_func, arr):
    import sympy as sp
    if isinstance(arr, sp.Basic):
        return sp_func(arr)
    return KheraMATArray(np_func(_to_arr(arr)))

# Elementwise Math
def km_sin(arr) -> Any:
    import sympy as sp
    return _math_op(np.sin, sp.sin, arr)
def km_cos(arr) -> Any:
    import sympy as sp
    return _math_op(np.cos, sp.cos, arr)
def km_tan(arr) -> Any:
    import sympy as sp
    return _math_op(np.tan, sp.tan, arr)
def km_exp(arr) -> Any:
    import sympy as sp
    return _math_op(np.exp, sp.exp, arr)
def km_log(arr) -> Any:
    import sympy as sp
    return _math_op(np.log, sp.log, arr)
def km_sqrt(arr) -> Any:
    import sympy as sp
    return _math_op(np.sqrt, sp.sqrt, arr)
def km_abs(arr) -> Any:
    import sympy as sp
    if isinstance(arr, sp.Basic):
        return sp.Abs(arr)
    return KheraMATArray(np.abs(_to_arr(arr)))
def km_floor(arr) -> KheraMATArray: return KheraMATArray(np.floor(_to_arr(arr)))
def km_ceil(arr) -> KheraMATArray: return KheraMATArray(np.ceil(_to_arr(arr)))
def km_round(arr) -> KheraMATArray: return KheraMATArray(np.round(_to_arr(arr)))

# Signal Processing Basics
def km_fft(arr) -> KheraMATArray: return KheraMATArray(np.fft.fft(_to_arr(arr)))
def km_ifft(arr) -> KheraMATArray: return KheraMATArray(np.fft.ifft(_to_arr(arr)))

def _first_nonsingleton_axis(arr: np.ndarray) -> int:
    if arr.ndim == 1:
        return 0
    for i, dim in enumerate(arr.shape):
        if dim > 1:
            return i
    return 0

# Reductions
def km_sum(arr) -> KheraMATArray: 
    a = _to_arr(arr)
    return KheraMATArray(np.sum(a, axis=_first_nonsingleton_axis(a), keepdims=True))

def km_mean(arr) -> KheraMATArray: 
    a = _to_arr(arr)
    return KheraMATArray(np.mean(a, axis=_first_nonsingleton_axis(a), keepdims=True))

def km_min(*args, nargout=1) -> Any:
    if len(args) == 1:
        a = _to_arr(args[0])
        ax = _first_nonsingleton_axis(a)
        val = np.min(a, axis=ax, keepdims=True)
        if nargout > 1:
            idx = np.argmin(a, axis=ax, keepdims=True) + 1
            return KheraMATArray(val), KheraMATArray(idx)
        return KheraMATArray(val)
    elif len(args) == 2:
        return KheraMATArray(np.minimum(_to_arr(args[0]), _to_arr(args[1])))
    else:
        raise ValueError("min takes 1 or 2 arguments in Vectra")

def km_max(*args, nargout=1) -> Any:
    if len(args) == 1:
        a = _to_arr(args[0])
        ax = _first_nonsingleton_axis(a)
        val = np.max(a, axis=ax, keepdims=True)
        if nargout > 1:
            idx = np.argmax(a, axis=ax, keepdims=True) + 1
            return KheraMATArray(val), KheraMATArray(idx)
        return KheraMATArray(val)
    elif len(args) == 2:
        return KheraMATArray(np.maximum(_to_arr(args[0]), _to_arr(args[1])))
    else:
        raise ValueError("max takes 1 or 2 arguments in Vectra")

def _format_matlab(fmt: str, *args) -> str:
    fmt_str = str(fmt._array.item() if hasattr(fmt, "_array") else fmt)
    fmt_str = fmt_str.replace("\\n", "\n").replace("\\t", "\t")
    
    import re
    fmt_str = re.sub(r'%([0-9\.\-+]*)[iI]', r'%\1d', fmt_str)
    
    clean_args = []
    for arg in args:
        import sympy as sp
        if isinstance(arg, sp.Basic):
            from .symbolic import clean_sym_str
            clean_args.append(clean_sym_str(arg))
            continue
            
        if hasattr(arg, "_array"):
            arr = arg._array
            for item in arr.flatten(order='F'):
                clean_args.append(int(item) if isinstance(item, (np.integer, bool)) else (float(item) if isinstance(item, np.floating) else item))
        else:
            clean_args.append(arg)
            
    if not clean_args:
        return fmt_str.replace('%%', '%')
        
    num_specs = len(re.findall(r'%[-+ 0]*\d*(?:\.\d*)?[a-zA-Z]', fmt_str.replace('%%', '')))
    if num_specs == 0:
        return fmt_str.replace('%%', '%')
        
    result_parts = []
    parts = re.split(r'(%[-+ 0]*\d*(?:\.\d*)?[a-zA-Z])', fmt_str.replace('%%', '\0'))
    
    arg_idx = 0
    while arg_idx < len(clean_args):
        for part in parts:
            if part.startswith('%'):
                if arg_idx < len(clean_args):
                    try:
                        # If the arg is a string (like from sympy) and we need %s, it works.
                        # If the format is %d or %f and we got a sympy string, it will exception and fallback.
                        formatted = part % clean_args[arg_idx]
                        result_parts.append(formatted)
                    except Exception:
                        result_parts.append(str(clean_args[arg_idx]))
                    arg_idx += 1
                else:
                    break
            else:
                result_parts.append(part.replace('\0', '%'))
                
    return "".join(result_parts)

def km_sprintf(fmt: str, *args) -> KheraMATArray:
    res = _format_matlab(fmt, *args)
    return KheraMATArray(res)

def km_fprintf(fmt: str, *args):
    res = _format_matlab(fmt, *args)
    sys_stdout_write = getattr(sys.stdout, 'write', None)
    print(res, end='')
    return None

def km_disp(*args):
    import sympy as sp
    from .symbolic import clean_sym_str
    for item in args:
        if isinstance(item, sp.Basic):
            print(clean_sym_str(item))
        else:
            print(item)
    return None

def km_logspace(start, stop, num=50) -> KheraMATArray:
    st = float(_to_arr(start).item() if isinstance(start, KheraMATArray) else start)
    sp = float(_to_arr(stop).item() if isinstance(stop, KheraMATArray) else stop)
    n = int(_to_arr(num).item() if isinstance(num, KheraMATArray) else num)
    return KheraMATArray(np.logspace(st, sp, n).reshape((1, -1)))

def km_diag(v, k=0) -> KheraMATArray:
    arr = _to_arr(v)
    k_val = int(_to_arr(k).item() if isinstance(k, KheraMATArray) else k)
    if arr.ndim == 1 or (arr.ndim == 2 and (arr.shape[0] == 1 or arr.shape[1] == 1)):
        return KheraMATArray(np.diag(arr.flatten(), k=k_val))
    return KheraMATArray(np.diag(arr, k=k_val).reshape((1, -1)))

def km_cross(a, b) -> KheraMATArray:
    a_arr = _to_arr(a).flatten()
    b_arr = _to_arr(b).flatten()
    return KheraMATArray(np.cross(a_arr, b_arr).reshape((1, -1)))

def km_dot(a, b) -> KheraMATArray:
    a_arr = _to_arr(a).flatten()
    b_arr = _to_arr(b).flatten()
    return KheraMATArray(np.dot(a_arr, b_arr))

def km_reshape(a, *args) -> KheraMATArray:
    arr = _to_arr(a)
    shape = _parse_dims(*args)
    return KheraMATArray(arr.reshape(shape))

def km_repmat(a, m, n=None) -> KheraMATArray:
    arr = _to_arr(a)
    m_val = int(_to_arr(m).item() if isinstance(m, KheraMATArray) else m)
    n_val = int(_to_arr(n).item() if isinstance(n, KheraMATArray) else n) if n is not None else m_val
    return KheraMATArray(np.tile(arr, (m_val, n_val)))

def km_sort(a) -> KheraMATArray:
    arr = _to_arr(a)
    return KheraMATArray(np.sort(arr, axis=0 if arr.ndim > 1 else -1))

def km_sub2ind(siz, row, col) -> KheraMATArray:
    s = _to_arr(siz).flatten().astype(int)
    r = _to_arr(row).flatten().astype(int) - 1
    c = _to_arr(col).flatten().astype(int) - 1
    inds = np.ravel_multi_index((r, c), dims=s, order='F') + 1
    return KheraMATArray(inds.reshape((1, -1)))

def km_ind2sub(siz, ind, nargout=2) -> Any:
    s = _to_arr(siz).flatten().astype(int)
    i = _to_arr(ind).flatten().astype(int) - 1
    r, c = np.unravel_index(i, shape=s, order='F')
    if nargout > 1:
        return KheraMATArray((r + 1).reshape((1, -1))), KheraMATArray((c + 1).reshape((1, -1)))
    return KheraMATArray((r + 1).reshape((1, -1)))

def km_find(x) -> KheraMATArray:
    arr = _to_arr(x).flatten()
    inds = np.where(arr != 0)[0] + 1
    return KheraMATArray(inds.reshape((1, -1)))

# Trigonometric & Inverse Trig
def km_asin(arr) -> KheraMATArray: return KheraMATArray(np.arcsin(_to_arr(arr)))
def km_acos(arr) -> KheraMATArray: return KheraMATArray(np.arccos(_to_arr(arr)))
def km_atan(arr) -> KheraMATArray: return KheraMATArray(np.arctan(_to_arr(arr)))
def km_sec(arr) -> KheraMATArray: return KheraMATArray(1.0 / np.cos(_to_arr(arr)))
def km_csc(arr) -> KheraMATArray: return KheraMATArray(1.0 / np.sin(_to_arr(arr)))
def km_cot(arr) -> KheraMATArray: return KheraMATArray(1.0 / np.tan(_to_arr(arr)))
def km_asec(arr) -> KheraMATArray: return KheraMATArray(np.arccos(1.0 / _to_arr(arr)))
def km_acsc(arr) -> KheraMATArray: return KheraMATArray(np.arcsin(1.0 / _to_arr(arr)))
def km_acot(arr) -> KheraMATArray: return KheraMATArray(np.arctan(1.0 / _to_arr(arr)))

# Complex & Exponents
def km_log10(arr) -> KheraMATArray: return KheraMATArray(np.log10(_to_arr(arr)))
def km_log2(arr) -> KheraMATArray: return KheraMATArray(np.log2(_to_arr(arr)))
def km_sign(arr) -> KheraMATArray: return KheraMATArray(np.sign(_to_arr(arr)))
def km_rem(a, b) -> KheraMATArray: return KheraMATArray(np.fmod(_to_arr(a), _to_arr(b)))
def km_mod(a, b) -> KheraMATArray: return KheraMATArray(np.mod(_to_arr(a), _to_arr(b)))
def km_angle(arr) -> KheraMATArray: return KheraMATArray(np.angle(_to_arr(arr)))
def km_conj(arr) -> KheraMATArray: return KheraMATArray(np.conj(_to_arr(arr)))
def km_real(arr) -> KheraMATArray: return KheraMATArray(np.real(_to_arr(arr)))
def km_imag(arr) -> KheraMATArray: return KheraMATArray(np.imag(_to_arr(arr)))

# Statistics & Reductions
def km_median(arr) -> KheraMATArray:
    a = _to_arr(arr)
    return KheraMATArray(np.median(a, axis=_first_nonsingleton_axis(a), keepdims=True))

def km_std(arr) -> KheraMATArray:
    a = _to_arr(arr)
    return KheraMATArray(np.std(a, axis=_first_nonsingleton_axis(a), ddof=1, keepdims=True))

def km_var(arr) -> KheraMATArray:
    a = _to_arr(arr)
    return KheraMATArray(np.var(a, axis=_first_nonsingleton_axis(a), ddof=1, keepdims=True))

# Polynomials & Numerical Integration
def km_poly(r) -> KheraMATArray:
    arr = _to_arr(r).flatten()
    coeffs = np.poly(arr)
    return KheraMATArray(coeffs.reshape((1, -1)))

def km_roots(c) -> KheraMATArray:
    arr = _to_arr(c).flatten()
    r = np.roots(arr)
    return KheraMATArray(r.reshape((-1, 1)))

def km_trapz(*args) -> KheraMATArray:
    if not args: return KheraMATArray(0.0)
    if len(args) == 1:
        y_arr = _to_arr(args[0]).flatten()
        res = np.trapezoid(y_arr) if hasattr(np, 'trapezoid') else np.trapz(y_arr)
    else:
        # In MATLAB trapz(X, Y) or trapz(Y, dim)
        arg1 = _to_arr(args[0]).flatten()
        arg2 = _to_arr(args[1]).flatten()
        if len(arg1) == len(arg2):
            res = np.trapezoid(arg2, arg1) if hasattr(np, 'trapezoid') else np.trapz(arg2, arg1)
        else:
            res = np.trapezoid(arg1) if hasattr(np, 'trapezoid') else np.trapz(arg1)
    return KheraMATArray(res)

def km_diff(x, n=1) -> KheraMATArray:
    x_arr = _to_arr(x)
    n_val = int(_to_arr(n).item() if isinstance(n, KheraMATArray) else n)
    
    if x_arr.ndim == 0 or x_arr.size <= 1:
        return KheraMATArray(np.array([]).reshape((0, 0)))
        
    if x_arr.ndim == 1:
        res = np.diff(x_arr, n=n_val)
    elif x_arr.ndim == 2:
        if x_arr.shape[0] == 1:
            res = np.diff(x_arr, n=n_val, axis=1)
        elif x_arr.shape[1] == 1:
            res = np.diff(x_arr, n=n_val, axis=0)
        else:
            res = np.diff(x_arr, n=n_val, axis=0)
    else:
        # For N-D, MATLAB diffs along first non-singleton dimension
        # But we mostly deal with 2D.
        first_non_singleton = next((i for i, s in enumerate(x_arr.shape) if s > 1), 0)
        res = np.diff(x_arr, n=n_val, axis=first_non_singleton)
        
    return KheraMATArray(res)

# Advanced Linear Algebra & Matrix Decompositions
def km_eig(arr, nargout=1) -> Any:
    w, v = np.linalg.eig(_to_arr(arr))
    if nargout > 1:
        return KheraMATArray(v), KheraMATArray(np.diag(w))
    return KheraMATArray(w.reshape((-1, 1)))

def km_svd(a, nargout=1) -> Any:
    u, s, vh = np.linalg.svd(_to_arr(a))
    if nargout > 1:
        return KheraMATArray(u), KheraMATArray(np.diag(s)), KheraMATArray(vh.T)
    return KheraMATArray(s.reshape((-1, 1)))

def km_lu(a, nargout=1) -> Any:
    import scipy.linalg as la
    p, l, u = la.lu(_to_arr(a))
    if nargout > 1:
        return KheraMATArray(l), KheraMATArray(u), KheraMATArray(p)
    return KheraMATArray(l @ u) # if nargout=1, just returns something (MATLAB returns factored matrix? MATLAB actually returns L, U for 2 outputs, or just y for 1 which isn't typically used) but usually lu is multiple outputs. Let's just return L*U. Actually, MATLAB returns L+U-I.

def km_qr(a, nargout=1) -> Any:
    q, r = np.linalg.qr(_to_arr(a))
    if nargout > 1:
        return KheraMATArray(q), KheraMATArray(r)
    return KheraMATArray(r)

def km_chol(a) -> KheraMATArray:
    return KheraMATArray(np.linalg.cholesky(_to_arr(a)).T)

def km_cond(a) -> KheraMATArray:
    return KheraMATArray(np.linalg.cond(_to_arr(a)))

def km_null(a) -> KheraMATArray:
    import scipy.linalg as la
    return KheraMATArray(la.null_space(_to_arr(a)))

def km_orth(a) -> KheraMATArray:
    import scipy.linalg as la
    return KheraMATArray(la.orth(_to_arr(a)))

# Matrix Functions
def km_expm(a) -> KheraMATArray:
    import scipy.linalg as la
    return KheraMATArray(la.expm(_to_arr(a)))

def km_logm(a) -> KheraMATArray:
    import scipy.linalg as la
    return KheraMATArray(la.logm(_to_arr(a)))

def km_sqrtm(a) -> KheraMATArray:
    import scipy.linalg as la
    return KheraMATArray(la.sqrtm(_to_arr(a)))

# Polynomial & Multidimensional Array Operations
def km_polyval(p, x) -> KheraMATArray:
    p_arr = _to_arr(p).flatten()
    x_arr = _to_arr(x)
    return KheraMATArray(np.polyval(p_arr, x_arr))

def km_polyfit(x, y, n) -> KheraMATArray:
    x_arr = _to_arr(x).flatten()
    y_arr = _to_arr(y).flatten()
    deg = int(_to_arr(n).item() if isinstance(n, KheraMATArray) else n)
    return KheraMATArray(np.polyfit(x_arr, y_arr, deg).reshape((1, -1)))

def km_conv2(a, b) -> KheraMATArray:
    import scipy.signal as sig
    return KheraMATArray(sig.convolve2d(_to_arr(a), _to_arr(b), mode='full'))

def km_cumsum(a) -> KheraMATArray: return KheraMATArray(np.cumsum(_to_arr(a), axis=0 if _to_arr(a).ndim > 1 else -1))
def km_cumprod(a) -> KheraMATArray: return KheraMATArray(np.cumprod(_to_arr(a), axis=0 if _to_arr(a).ndim > 1 else -1))
def km_prod(a) -> KheraMATArray:
    arr = _to_arr(a)
    return KheraMATArray(np.prod(arr, axis=_first_nonsingleton_axis(arr), keepdims=True))

def km_all(a) -> KheraMATArray:
    arr = _to_arr(a)
    return KheraMATArray(np.all(arr, axis=_first_nonsingleton_axis(arr), keepdims=True).astype(int))

def km_any(a) -> KheraMATArray:
    arr = _to_arr(a)
    return KheraMATArray(np.any(arr, axis=_first_nonsingleton_axis(arr), keepdims=True).astype(int))
def km_squeeze(a) -> KheraMATArray: return KheraMATArray(np.squeeze(_to_arr(a)))
def km_flip(a) -> KheraMATArray: return KheraMATArray(np.flip(_to_arr(a)))
def km_fliplr(a) -> KheraMATArray: return KheraMATArray(np.fliplr(_to_arr(a)))
def km_flipud(a) -> KheraMATArray: return KheraMATArray(np.flipud(_to_arr(a)))
def km_rot90(a, k=1) -> KheraMATArray:
    k_val = int(_to_arr(k).item() if isinstance(k, KheraMATArray) else k)
    return KheraMATArray(np.rot90(_to_arr(a), k=k_val))

def km_fzero(func_name, x0) -> KheraMATArray:
    import scipy.optimize as opt
    fname = str(func_name._array.item() if hasattr(func_name, "_array") else func_name)
    x_val = float(_to_arr(x0).item())
    res = opt.fsolve(lambda x: eval(fname)(x), x_val)
    return KheraMATArray(res[0])

def km_assert(cond, msg="Assertion failed"):
    import sympy as sp
    if isinstance(cond, sp.Basic):
        c = bool(cond)
    elif isinstance(cond, KheraMATArray):
        c = bool(np.all(cond._array))
    else:
        c = bool(cond)
    if not c:
        msg_str = msg._array.item() if hasattr(msg, "_array") else str(msg)
        raise AssertionError(msg_str)

def km_strcmp(s1, s2) -> KheraMATArray:
    str1 = s1._array.item() if hasattr(s1, "_array") else str(s1)
    str2 = s2._array.item() if hasattr(s2, "_array") else str(s2)
    return KheraMATArray(str1 == str2)
    return None

CORE_MATH_FUNCTIONS: Dict[str, Callable] = {
    "zeros": km_zeros,
    "ones": km_ones,
    "eye": km_eye,
    "rand": km_rand,
    "randn": km_randn,
    "linspace": km_linspace,
    "logspace": km_logspace,
    "diag": km_diag,
    "cross": km_cross,
    "dot": km_dot,
    "reshape": km_reshape,
    "repmat": km_repmat,
    "sort": km_sort,
    "sub2ind": km_sub2ind,
    "ind2sub": km_ind2sub,
    "find": km_find,
    "size": km_size,
    "length": km_length,
    "numel": km_numel,
    "det": km_det,
    "inv": km_inv,
    "pinv": km_pinv,
    "eig": km_eig,
    "svd": km_svd,
    "lu": km_lu,
    "qr": km_qr,
    "chol": km_chol,
    "cond": km_cond,
    "null": km_null,
    "orth": km_orth,
    "expm": km_expm,
    "logm": km_logm,
    "sqrtm": km_sqrtm,
    "norm": km_norm,
    "trace": km_trace,
    "rank": km_rank,
    "sin": km_sin,
    "cos": km_cos,
    "tan": km_tan,
    "asin": km_asin,
    "acos": km_acos,
    "atan": km_atan,
    "sec": km_sec,
    "csc": km_csc,
    "cot": km_cot,
    "asec": km_asec,
    "acsc": km_acsc,
    "acot": km_acot,
    "exp": km_exp,
    "log": km_log,
    "log10": km_log10,
    "log2": km_log2,
    "sqrt": km_sqrt,
    "abs": km_abs,
    "sign": km_sign,
    "floor": km_floor,
    "ceil": km_ceil,
    "round": km_round,
    "rem": km_rem,
    "mod": km_mod,
    "angle": km_angle,
    "conj": km_conj,
    "real": km_real,
    "imag": km_imag,
    "fft": km_fft,
    "ifft": km_ifft,
    "sum": km_sum,
    "mean": km_mean,
    "median": km_median,
    "std": km_std,
    "var": km_var,
    "min": km_min,
    "max": km_max,
    "poly": km_poly,
    "roots": km_roots,
    "polyval": km_polyval,
    "polyfit": km_polyfit,
    "conv2": km_conv2,
    "cumsum": km_cumsum,
    "cumprod": km_cumprod,
    "prod": km_prod,
    "all": km_all,
    "any": km_any,
    "squeeze": km_squeeze,
    "flip": km_flip,
    "fliplr": km_fliplr,
    "flipud": km_flipud,
    "rot90": km_rot90,
    "trapz": km_trapz,
    "diff": km_diff,
    "fzero": km_fzero,
    "disp": km_disp,
    "fprintf": km_fprintf,
    "sprintf": km_sprintf,
    "assert": km_assert,
    "strcmp": km_strcmp,
}
