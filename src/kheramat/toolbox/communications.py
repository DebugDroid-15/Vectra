import numpy as np
import scipy.signal as signal
from typing import Dict, Callable, Any
from ..runtime.kheramat_array import KheraMATArray

def _to_arr(val: Any) -> np.ndarray:
    if isinstance(val, KheraMATArray):
        return val._array
    return np.array(val)

def km_ammod(x, fc, fs, k_a=1.0) -> KheraMATArray:
    m = _to_arr(x).flatten()
    _fc = float(_to_arr(fc).item())
    _fs = float(_to_arr(fs).item())
    _ka = float(_to_arr(k_a).item())
    t = np.arange(len(m)) / _fs
    carrier = np.cos(2 * np.pi * _fc * t)
    s = (1.0 + _ka * m) * carrier
    return KheraMATArray(s.reshape((1, -1)))

def km_amdemod(y, fc, fs) -> KheraMATArray:
    s = _to_arr(y).flatten()
    _fc = float(_to_arr(fc).item())
    _fs = float(_to_arr(fs).item())
    t = np.arange(len(s)) / _fs
    carrier = np.cos(2 * np.pi * _fc * t)
    demod = s * carrier * 2.0
    b, a = signal.butter(5, _fc / (_fs / 2.0))
    m_hat = signal.lfilter(b, a, demod)
    return KheraMATArray(m_hat.reshape((1, -1)))

def km_fmmod(x, fc, fs, freqdev=1.0) -> KheraMATArray:
    m = _to_arr(x).flatten()
    _fc = float(_to_arr(fc).item())
    _fs = float(_to_arr(fs).item())
    _dev = float(_to_arr(freqdev).item())
    t = np.arange(len(m)) / _fs
    integral_m = np.cumsum(m) / _fs
    s = np.cos(2 * np.pi * _fc * t + 2 * np.pi * _dev * integral_m)
    return KheraMATArray(s.reshape((1, -1)))

def km_fmdemod(y, fc, fs, freqdev=1.0) -> KheraMATArray:
    s = _to_arr(y).flatten()
    _fs = float(_to_arr(fs).item())
    _dev = float(_to_arr(freqdev).item())
    analytic = signal.hilbert(s)
    inst_phase = np.unwrap(np.angle(analytic))
    t = np.arange(len(s)) / _fs
    _fc = float(_to_arr(fc).item())
    demod = np.diff(inst_phase) * _fs / (2 * np.pi * _dev)
    demod = np.pad(demod, (1, 0), mode='edge')
    return KheraMATArray(demod.reshape((1, -1)))

def km_awgn(x, snr_db) -> KheraMATArray:
    arr = _to_arr(x)
    snr = float(_to_arr(snr_db).item())
    sig_power = np.mean(np.abs(arr) ** 2)
    sig_power_db = 10 * np.log10(sig_power)
    noise_power_db = sig_power_db - snr
    noise_power = 10 ** (noise_power_db / 10.0)
    noise = np.random.normal(0, np.sqrt(noise_power), arr.shape)
    return KheraMATArray(arr + noise)

def km_bpskmod(bits) -> KheraMATArray:
    b = _to_arr(bits).flatten()
    symbols = np.where(b > 0, 1.0 + 0j, -1.0 + 0j)
    return KheraMATArray(symbols.reshape((1, -1)))

def km_qpskmod(bits) -> KheraMATArray:
    b = _to_arr(bits).flatten()
    if len(b) % 2 != 0:
        b = np.append(b, 0)
    b_pairs = b.reshape((-1, 2))
    lut = {
        (0, 0): (1 + 1j) / np.sqrt(2),
        (0, 1): (-1 + 1j) / np.sqrt(2),
        (1, 1): (-1 - 1j) / np.sqrt(2),
        (1, 0): (1 - 1j) / np.sqrt(2),
    }
    symbols = np.array([lut[(int(p[0]), int(p[1]))] for p in b_pairs])
    return KheraMATArray(symbols.reshape((1, -1)))

COMMUNICATION_FUNCTIONS: Dict[str, Callable] = {
    "ammod": km_ammod,
    "amdemod": km_amdemod,
    "fmmod": km_fmmod,
    "fmdemod": km_fmdemod,
    "awgn": km_awgn,
    "bpskmod": km_bpskmod,
    "qpskmod": km_qpskmod,
}

