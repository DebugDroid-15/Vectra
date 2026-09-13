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

def km_surf(X, Y, Z=None):
    if Z is None:
        Z_arr = _to_arr(X)
        X_arr, Y_arr = np.meshgrid(np.arange(1, Z_arr.shape[1] + 1), np.arange(1, Z_arr.shape[0] + 1))
    else:
        X_arr = _to_arr(X)
        Y_arr = _to_arr(Y)
        Z_arr = _to_arr(Z)
    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    surf_obj = ax.plot_surface(X_arr, Y_arr, Z_arr, cmap='viridis', edgecolor='none')
    fig.colorbar(surf_obj, ax=ax, shrink=0.5, aspect=5)
    plt.show()
    return None

def km_mesh(X, Y, Z=None):
    if Z is None:
        Z_arr = _to_arr(X)
        X_arr, Y_arr = np.meshgrid(np.arange(1, Z_arr.shape[1] + 1), np.arange(1, Z_arr.shape[0] + 1))
    else:
        X_arr = _to_arr(X)
        Y_arr = _to_arr(Y)
        Z_arr = _to_arr(Z)
    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_wireframe(X_arr, Y_arr, Z_arr, color='blue', linewidth=0.5)
    plt.show()
    return None

def km_quiver(X, Y, U, V):
    plt.quiver(_to_arr(X), _to_arr(Y), _to_arr(U), _to_arr(V))
    plt.grid(True)
    plt.show()
    return None

def km_quiver3(X, Y, Z, U, V, W):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.quiver(_to_arr(X), _to_arr(Y), _to_arr(Z), _to_arr(U), _to_arr(V), _to_arr(W))
    plt.show()
    return None

def km_gradient(F, *args) -> KheraMATArray:
    f_arr = _to_arr(F)
    res = np.gradient(f_arr)
    if isinstance(res, list):
        return KheraMATArray(res[0])
    return KheraMATArray(res)

ELECTROMAGNETICS_FUNCTIONS: Dict[str, Callable] = {
    "meshgrid": km_meshgrid,
    "surf": km_surf,
    "mesh": km_mesh,
    "quiver": km_quiver,
    "quiver3": km_quiver3,
    "gradient": km_gradient,
}

