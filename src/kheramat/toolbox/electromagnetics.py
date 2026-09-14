import numpy as np
import matplotlib.pyplot as plt
from typing import Dict, Callable, Any
from ..runtime.kheramat_array import KheraMATArray

def _to_arr(val: Any) -> np.ndarray:
    if isinstance(val, KheraMATArray):
        return val._array
    return np.array(val)

def km_meshgrid(x, y=None) -> (KheraMATArray, KheraMATArray):
    x_arr = _to_arr(x).flatten()
    if y is None:
        y_arr = x_arr
    else:
        y_arr = _to_arr(y).flatten()
    X, Y = np.meshgrid(x_arr, y_arr)
    return KheraMATArray(X), KheraMATArray(Y)

def km_gradient(F, *args) -> KheraMATArray:
    f_arr = _to_arr(F)
    res = np.gradient(f_arr)
    if isinstance(res, list):
        return KheraMATArray(res[0])
    return KheraMATArray(res)

ELECTROMAGNETICS_FUNCTIONS: Dict[str, Callable] = {
    "meshgrid": km_meshgrid,
    "gradient": km_gradient,
}

