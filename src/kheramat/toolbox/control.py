import numpy as np
import scipy.signal as signal
import matplotlib.pyplot as plt
from typing import Dict, Callable, Any
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
    
    def __repr__(self):
        return f"TransferFunction(num={self.num}, den={self.den})"

def km_tf(num, den) -> KheraMATSystem:
    return KheraMATSystem(num, den)

def km_step(sys_obj) -> (KheraMATArray, KheraMATArray):
    if not isinstance(sys_obj, KheraMATSystem):
        raise ValueError("Expected a transfer function system created with tf(num, den)")
    t, y = signal.step(sys_obj.sys)
    return KheraMATArray(y.reshape((1, -1))), KheraMATArray(t.reshape((1, -1)))

def km_impulse(sys_obj) -> (KheraMATArray, KheraMATArray):
    if not isinstance(sys_obj, KheraMATSystem):
        raise ValueError("Expected a transfer function system created with tf(num, den)")
    t, y = signal.impulse(sys_obj.sys)
    return KheraMATArray(y.reshape((1, -1))), KheraMATArray(t.reshape((1, -1)))

def km_bode(sys_obj):
    if not isinstance(sys_obj, KheraMATSystem):
        raise ValueError("Expected a transfer function system created with tf(num, den)")
    w, mag, phase = signal.bode(sys_obj.sys)
    fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
    ax1.semilogx(w, mag)
    ax1.set_title('Bode Diagram')
    ax1.set_ylabel('Magnitude (dB)')
    ax1.grid(True, which='both')
    
    ax2.semilogx(w, phase)
    ax2.set_xlabel('Frequency (rad/s)')
    ax2.set_ylabel('Phase (deg)')
    ax2.grid(True, which='both')
    plt.show()
    return None

CONTROL_FUNCTIONS: Dict[str, Callable] = {
    "tf": km_tf,
    "step": km_step,
    "impulse": km_impulse,
    "bode": km_bode,
}

