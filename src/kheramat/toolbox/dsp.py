import numpy as np
import scipy.signal as signal
from typing import Dict, Callable, Any
from ..runtime.kheramat_array import KheraMATArray

def _to_arr(val: Any) -> np.ndarray:
    if isinstance(val, KheraMATArray):
        return val._array
    return np.array(val)

def km_butter(N, Wn, btype='low', analog=False) -> (KheraMATArray, KheraMATArray):
    n = int(_to_arr(N).item())
    wn = _to_arr(Wn)
    if wn.size == 1:
        wn = float(wn.item())
    else:
        wn = wn.flatten().tolist()
    btype_str = str(btype)
    b, a = signal.butter(n, wn, btype=btype_str, analog=bool(analog))
    return KheraMATArray(b.reshape((1, -1))), KheraMATArray(a.reshape((1, -1)))

def km_cheby1(N, Rp, Wn, btype='low', analog=False) -> (KheraMATArray, KheraMATArray):
    n = int(_to_arr(N).item())
    rp = float(_to_arr(Rp).item())
    wn = _to_arr(Wn)
    if wn.size == 1:
        wn = float(wn.item())
    else:
        wn = wn.flatten().tolist()
    btype_str = str(btype)
    b, a = signal.cheby1(n, rp, wn, btype=btype_str, analog=bool(analog))
    return KheraMATArray(b.reshape((1, -1))), KheraMATArray(a.reshape((1, -1)))

def km_cheby2(N, Rs, Wn, btype='low', analog=False) -> (KheraMATArray, KheraMATArray):
    n = int(_to_arr(N).item())
    rs = float(_to_arr(Rs).item())
    wn = _to_arr(Wn)
    if wn.size == 1:
        wn = float(wn.item())
    else:
        wn = wn.flatten().tolist()
    btype_str = str(btype)
    b, a = signal.cheby2(n, rs, wn, btype=btype_str, analog=bool(analog))
    return KheraMATArray(b.reshape((1, -1))), KheraMATArray(a.reshape((1, -1)))

def km_ellip(N, Rp, Rs, Wn, btype='low', analog=False) -> (KheraMATArray, KheraMATArray):
    n = int(_to_arr(N).item())
    rp = float(_to_arr(Rp).item())
    rs = float(_to_arr(Rs).item())
    wn = _to_arr(Wn)
    if wn.size == 1:
        wn = float(wn.item())
    else:
        wn = wn.flatten().tolist()
    btype_str = str(btype)
    b, a = signal.ellip(n, rp, rs, wn, btype=btype_str, analog=bool(analog))
    return KheraMATArray(b.reshape((1, -1))), KheraMATArray(a.reshape((1, -1)))

def km_bessel(N, Wn, btype='low', analog=False) -> (KheraMATArray, KheraMATArray):
    n = int(_to_arr(N).item())
    wn = _to_arr(Wn)
    if wn.size == 1:
        wn = float(wn.item())
    else:
        wn = wn.flatten().tolist()
    btype_str = str(btype)
    b, a = signal.bessel(n, wn, btype=btype_str, analog=bool(analog))
    return KheraMATArray(b.reshape((1, -1))), KheraMATArray(a.reshape((1, -1)))

def km_zplane(b, a=1):
    import matplotlib.pyplot as plt
    b_arr = _to_arr(b).flatten()
    a_arr = _to_arr(a).flatten()
    z, p, k = signal.tf2zpk(b_arr, a_arr)
    
    fig, ax = plt.subplots()
    unit_circle = plt.Circle((0,0), 1, color='gray', fill=False, linestyle='--')
    ax.add_artist(unit_circle)
    ax.plot(np.real(z), np.imag(z), 'ob', fillstyle='none', ms=8, label='Zeros')
    ax.plot(np.real(p), np.imag(p), 'xr', ms=8, label='Poles')
    ax.axhline(0, color='black', lw=0.5)
    ax.axvline(0, color='black', lw=0.5)
    ax.set_aspect('equal', 'box')
    ax.grid(True)
    ax.set_title('Pole-Zero Plot (zplane)')
    ax.set_xlabel('Real Part')
    ax.set_ylabel('Imaginary Part')
    ax.legend()
    plt.show()
    return None

def km_resample(x, p, q) -> KheraMATArray:
    x_arr = _to_arr(x).flatten()
    up = int(_to_arr(p).item())
    down = int(_to_arr(q).item())
    res = signal.resample_poly(x_arr, up, down)
    return KheraMATArray(res.reshape((1, -1)))

def km_decimate(x, r) -> KheraMATArray:
    x_arr = _to_arr(x).flatten()
    factor = int(_to_arr(r).item())
    res = signal.decimate(x_arr, factor)
    return KheraMATArray(res.reshape((1, -1)))

def km_interp(x, r) -> KheraMATArray:
    x_arr = _to_arr(x).flatten()
    factor = int(_to_arr(r).item())
    res = signal.resample(x_arr, len(x_arr) * factor)
    return KheraMATArray(res.reshape((1, -1)))

DSP_FUNCTIONS: Dict[str, Callable] = {
    "butter": km_butter,
    "cheby1": km_cheby1,
    "cheby2": km_cheby2,
    "ellip": km_ellip,
    "bessel": km_bessel,
    "zplane": km_zplane,
    "resample": km_resample,
    "decimate": km_decimate,
    "interp": km_interp,
}

