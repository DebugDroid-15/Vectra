import numpy as np
import scipy.signal as signal
import matplotlib.pyplot as plt
from typing import Dict, Callable, Any, Tuple
from ..runtime.kheramat_array import KheraMATArray

def _to_arr(val: Any) -> np.ndarray:
    if isinstance(val, KheraMATArray):
        return val._array
    return np.array(val)

class KheraMATSystem:
    def __init__(self, num, den):
        self.num = _to_arr(num).flatten()
        self.den = _to_arr(den).flatten()
        self.sys = signal.TransferFunction(self.num, self.den)
    
    def __str__(self):
        def poly_str(coeffs):
            parts = []
            deg = len(coeffs) - 1
            for i, c in enumerate(coeffs):
                if c == 0: continue
                d = deg - i
                abs_c = abs(c)
                sign = " - " if c < 0 else (" + " if parts else "")
                
                if d == 0:
                    term = f"{abs_c:g}"
                else:
                    coeff_str = "" if abs_c == 1.0 else f"{abs_c:g} "
                    var_str = "s" if d == 1 else f"s^{d}"
                    term = coeff_str + var_str
                
                parts.append(sign + term)
            if not parts: return "0"
            return "".join(parts).strip()
            
        n_str = poly_str(self.num)
        d_str = poly_str(self.den)
        
        # Center the strings
        width = max(len(n_str), len(d_str))
        sep = "-" * width
        return f"\n  {n_str.center(width)}\n  {sep}\n  {d_str.center(width)}\n\nContinuous-time transfer function."

    def __repr__(self):
        return self.__str__()

def km_tf(num, den) -> KheraMATSystem:
    return KheraMATSystem(num, den)

def km_step(sys_obj, nargout=1) -> Any:
    if not isinstance(sys_obj, KheraMATSystem):
        raise ValueError("Expected a transfer function system created with tf(num, den)")
    t, y = signal.step(sys_obj.sys)
    if nargout > 1:
        return KheraMATArray(y.reshape((1, -1))), KheraMATArray(t.reshape((1, -1)))
    return KheraMATArray(y.reshape((1, -1)))

def km_impulse(sys_obj, nargout=1) -> Any:
    if not isinstance(sys_obj, KheraMATSystem):
        raise ValueError("Expected a transfer function system created with tf(num, den)")
    t, y = signal.impulse(sys_obj.sys)
    if nargout > 1:
        return KheraMATArray(y.reshape((1, -1))), KheraMATArray(t.reshape((1, -1)))
    return KheraMATArray(y.reshape((1, -1)))

def km_bode(sys_obj, nargout=1) -> Any:
    if not isinstance(sys_obj, KheraMATSystem):
        raise ValueError("Expected a transfer function system created with tf(num, den)")
    w, mag, phase = signal.bode(sys_obj.sys)
    if nargout > 2:
        return (KheraMATArray(mag.reshape((1, -1))), 
                KheraMATArray(phase.reshape((1, -1))), 
                KheraMATArray(w.reshape((1, -1))))
    elif nargout == 2:
        return KheraMATArray(mag.reshape((1, -1))), KheraMATArray(phase.reshape((1, -1)))
    return KheraMATArray(mag.reshape((1, -1)))

def km_pole(sys_obj) -> KheraMATArray:
    if not isinstance(sys_obj, KheraMATSystem):
        raise ValueError("Expected a transfer function system created with tf(num, den)")
    poles = sys_obj.sys.poles
    return KheraMATArray(poles.reshape((-1, 1)))

def km_zero(sys_obj) -> KheraMATArray:
    if not isinstance(sys_obj, KheraMATSystem):
        raise ValueError("Expected a transfer function system created with tf(num, den)")
    zeros = sys_obj.sys.zeros
    if zeros.size == 0:
        return KheraMATArray(np.empty((0, 1)))
    return KheraMATArray(zeros.reshape((-1, 1)))

CONTROL_FUNCTIONS: Dict[str, Callable] = {
    "tf": km_tf,
    "step": km_step,
    "impulse": km_impulse,
    "bode": km_bode,
    "pole": km_pole,
    "zero": km_zero,
}

