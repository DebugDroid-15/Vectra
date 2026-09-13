import numpy as np
import scipy.signal as signal
from typing import Dict, Callable, Any
from ..runtime.kheramat_array import KheraMATArray

def _to_arr(val: Any) -> np.ndarray:
    if isinstance(val, KheraMATArray):
        return val._array
    return np.array(val)

def km_heaviside(t) -> KheraMATArray:
    arr = _to_arr(t)
    res = np.where(arr >= 0, 1.0, 0.0)
    return KheraMATArray(res)

def km_unitstep(t) -> KheraMATArray:
    return km_heaviside(t)

def km_dirac(t) -> KheraMATArray:
    arr = _to_arr(t)
    res = np.where(arr == 0, 1.0, 0.0)
    return KheraMATArray(res)

def km_unitimpulse(n) -> KheraMATArray:
    return km_dirac(n)

def km_sinc(x) -> KheraMATArray:
    arr = _to_arr(x)
    return KheraMATArray(np.sinc(arr))

def km_square(t, duty=50) -> KheraMATArray:
    arr = _to_arr(t)
    d = float(_to_arr(duty).item() if isinstance(duty, KheraMATArray) else duty) / 100.0
    return KheraMATArray(signal.square(arr, duty=d))

def km_sawtooth(t, width=1.0) -> KheraMATArray:
    arr = _to_arr(t)
    w = float(_to_arr(width).item() if isinstance(width, KheraMATArray) else width)
    return KheraMATArray(signal.sawtooth(arr, width=w))

def km_chirp(t, f0=0, t1=1, f1=100) -> KheraMATArray:
    arr = _to_arr(t)
    _f0 = float(_to_arr(f0).item() if isinstance(f0, KheraMATArray) else f0)
    _t1 = float(_to_arr(t1).item() if isinstance(t1, KheraMATArray) else t1)
    _f1 = float(_to_arr(f1).item() if isinstance(f1, KheraMATArray) else f1)
    return KheraMATArray(signal.chirp(arr, f0=_f0, t1=_t1, f1=_f1))

def km_rectpuls(t, w=1.0) -> KheraMATArray:
    arr = _to_arr(t)
    width = float(_to_arr(w).item() if isinstance(w, KheraMATArray) else w)
    res = np.where(np.abs(arr) <= width / 2.0, 1.0, 0.0)
    return KheraMATArray(res)

def km_tripuls(t, w=1.0) -> KheraMATArray:
    arr = _to_arr(t)
    width = float(_to_arr(w).item() if isinstance(w, KheraMATArray) else w)
    res = np.maximum(0.0, 1.0 - np.abs(arr) / (width / 2.0))
    return KheraMATArray(res)

def km_conv(x, h) -> KheraMATArray:
    x_arr = _to_arr(x).flatten()
    h_arr = _to_arr(h).flatten()
    res = np.convolve(x_arr, h_arr)
    return KheraMATArray(res.reshape((1, -1)))

def km_deconv(y, c) -> (KheraMATArray, KheraMATArray):
    y_arr = _to_arr(y).flatten()
    c_arr = _to_arr(c).flatten()
    q, r = signal.deconvolve(y_arr, c_arr)
    return KheraMATArray(q.reshape((1, -1))), KheraMATArray(r.reshape((1, -1)))

def km_xcorr(x, y=None) -> KheraMATArray:
    x_arr = _to_arr(x).flatten()
    if y is None:
        res = np.correlate(x_arr, x_arr, mode='full')
    else:
        y_arr = _to_arr(y).flatten()
        res = np.correlate(x_arr, y_arr, mode='full')
    return KheraMATArray(res.reshape((1, -1)))

def km_filter(b, a, x) -> KheraMATArray:
    b_arr = _to_arr(b).flatten()
    a_arr = _to_arr(a).flatten()
    x_arr = _to_arr(x).flatten()
    res = signal.lfilter(b_arr, a_arr, x_arr)
    return KheraMATArray(res.reshape((1, -1)))

def km_freqz(b, a, worN=512, fs=None) -> (KheraMATArray, KheraMATArray):
    b_arr = _to_arr(b).flatten()
    a_arr = _to_arr(a).flatten()
    n = int(_to_arr(worN).item() if isinstance(worN, KheraMATArray) else worN)
    if fs is not None:
        fs_val = float(_to_arr(fs).item() if isinstance(fs, KheraMATArray) else fs)
        w, h = signal.freqz(b_arr, a_arr, worN=n, fs=fs_val)
    else:
        w, h = signal.freqz(b_arr, a_arr, worN=n)
    return KheraMATArray(h.reshape((-1, 1))), KheraMATArray(w.reshape((-1, 1)))

def km_impz(b, a, n=50) -> (KheraMATArray, KheraMATArray):
    b_arr = _to_arr(b).flatten()
    a_arr = _to_arr(a).flatten()
    n_pts = int(_to_arr(n).item() if isinstance(n, KheraMATArray) else n)
    imp = np.zeros(n_pts)
    imp[0] = 1.0
    res = signal.lfilter(b_arr, a_arr, imp)
    t = np.arange(n_pts)
    return KheraMATArray(res.reshape((1, -1))), KheraMATArray(t.reshape((1, -1)))

def km_fftshift(x) -> KheraMATArray:
    return KheraMATArray(np.fft.fftshift(_to_arr(x)))

def km_ifftshift(x) -> KheraMATArray:
    return KheraMATArray(np.fft.ifftshift(_to_arr(x)))

def km_unwrap(p) -> KheraMATArray:
    return KheraMATArray(np.unwrap(_to_arr(p)))

def km_nextpow2(n) -> KheraMATArray:
    val = abs(float(_to_arr(n).item() if isinstance(n, KheraMATArray) else n))
    if val == 0: return KheraMATArray(0)
    return KheraMATArray(int(np.ceil(np.log2(val))))

SIGNAL_FUNCTIONS: Dict[str, Callable] = {
    "heaviside": km_heaviside,
    "unitstep": km_unitstep,
    "dirac": km_dirac,
    "unitimpulse": km_unitimpulse,
    "sinc": km_sinc,
    "square": km_square,
    "sawtooth": km_sawtooth,
    "chirp": km_chirp,
    "rectpuls": km_rectpuls,
    "tripuls": km_tripuls,
    "conv": km_conv,
    "deconv": km_deconv,
    "xcorr": km_xcorr,
    "filter": km_filter,
    "freqz": km_freqz,
    "impz": km_impz,
    "fftshift": km_fftshift,
    "ifftshift": km_ifftshift,
    "unwrap": km_unwrap,
    "nextpow2": km_nextpow2,
}

