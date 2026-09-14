import numpy as np
from typing import Union, Any, Tuple

class KheraMATArray:
    """
    Wraps a NumPy ndarray to provide MATLAB-compatible matrix operations,
    1-based indexing semantics, and formatted string representations.
    """
    def __init__(self, data: Any):
        if isinstance(data, KheraMATArray):
            self._array = data._array.copy()
        elif isinstance(data, np.ndarray):
            self._array = data
        else:
            if isinstance(data, (complex, np.complexfloating)):
                self._array = np.array(data, dtype=np.complex128)
            elif isinstance(data, (str, bool)):
                self._array = np.array(data)
            else:
                self._array = np.array(data, dtype=np.float64)
        
        # Ensure minimum 2-D array representation (MATLAB matrices are at least 2D e.g. 1x1 or 1xN)
        if self._array.ndim == 0:
            self._array = self._array.reshape((1, 1))
        elif self._array.ndim == 1:
            self._array = self._array.reshape((1, -1))

    @property
    def shape(self) -> Tuple[int, ...]:
        return self._array.shape

    @property
    def size(self) -> int:
        return self._array.size

    @property
    def dtype(self):
        return self._array.dtype

    def to_numpy(self) -> np.ndarray:
        return self._array

    # 1-Based Indexing support
    def get_index(self, *indices: Any) -> 'KheraMATArray':
        if len(indices) == 1:
            idx = indices[0]
            if isinstance(idx, str) and idx == ":":
                return KheraMATArray(self._array.flatten(order='F').reshape((-1, 1)))
            elif isinstance(idx, KheraMATArray):
                if idx.dtype == np.bool_:
                    return KheraMATArray(self._array.flatten(order='F')[idx._array.flatten(order='F')])
                else:
                    py_idx = (idx._array.flatten(order='F') - 1).astype(int)
                    return KheraMATArray(self._array.flatten(order='F')[py_idx])
            else:
                py_idx = int(idx) - 1
                return KheraMATArray(self._array.flatten(order='F')[py_idx])
        elif len(indices) == 2:
            r, c = indices[0], indices[1]
            if isinstance(r, KheraMATArray):
                r_idx = slice(None) if (isinstance(r._array, np.ndarray) and r._array.dtype.kind in ('U','S') and r._array.size == 1 and r._array.item() == ":") else (int(r._array.item()) - 1 if r._array.size == 1 else (r._array.flatten().astype(int) - 1))
            else:
                r_idx = slice(None) if r == ":" else int(r) - 1

            if isinstance(c, KheraMATArray):
                c_idx = slice(None) if (isinstance(c._array, np.ndarray) and c._array.dtype.kind in ('U','S') and c._array.size == 1 and c._array.item() == ":") else (int(c._array.item()) - 1 if c._array.size == 1 else (c._array.flatten().astype(int) - 1))
            else:
                c_idx = slice(None) if c == ":" else int(c) - 1

            if isinstance(r_idx, np.ndarray) and isinstance(c_idx, np.ndarray):
                res = self._array[np.ix_(r_idx, c_idx)]
            elif isinstance(r_idx, np.ndarray) and not isinstance(r_idx, slice):
                res = self._array[r_idx[:, None], c_idx]
            elif isinstance(c_idx, np.ndarray) and not isinstance(c_idx, slice):
                res = self._array[r_idx, c_idx]
            else:
                res = self._array[r_idx, c_idx]

            return KheraMATArray(res)
        else:
            raise IndexError("Only 1D and 2D indexing currently supported.")

    def set_index(self, value: Any, *indices: Any):
        val_arr = value._array if isinstance(value, KheraMATArray) else value
        if len(indices) == 1:
            idx = indices[0]
            if isinstance(idx, KheraMATArray):
                if idx.dtype == np.bool_:
                    py_idx = idx._array.flatten()
                else:
                    py_idx = (idx._array.flatten() - 1).astype(int)
            else:
                py_idx = int(idx) - 1
            self._array.flat[py_idx] = val_arr
        elif len(indices) == 2:
            r, c = indices[0], indices[1]
            if isinstance(r, KheraMATArray):
                r_idx = slice(None) if (isinstance(r._array, np.ndarray) and r._array.dtype.kind in ('U','S') and r._array.size == 1 and r._array.item() == ":") else (int(r._array.item()) - 1 if r._array.size == 1 else (r._array.flatten().astype(int) - 1))
            else:
                r_idx = slice(None) if r == ":" else int(r) - 1

            if isinstance(c, KheraMATArray):
                c_idx = slice(None) if (isinstance(c._array, np.ndarray) and c._array.dtype.kind in ('U','S') and c._array.size == 1 and c._array.item() == ":") else (int(c._array.item()) - 1 if c._array.size == 1 else (c._array.flatten().astype(int) - 1))
            else:
                c_idx = slice(None) if c == ":" else int(c) - 1

            if isinstance(r_idx, np.ndarray) and isinstance(c_idx, np.ndarray):
                self._array[np.ix_(r_idx, c_idx)] = val_arr
            elif isinstance(r_idx, np.ndarray) and not isinstance(r_idx, slice):
                self._array[r_idx[:, None], c_idx] = val_arr
            else:
                self._array[r_idx, c_idx] = val_arr

    # Matrix vs Elementwise arithmetic
    def __add__(self, other):
        b = other._array if isinstance(other, KheraMATArray) else other
        return KheraMATArray(self._array + b)

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        b = other._array if isinstance(other, KheraMATArray) else other
        return KheraMATArray(self._array - b)

    def __rsub__(self, other):
        b = other._array if isinstance(other, KheraMATArray) else other
        return KheraMATArray(b - self._array)

    def matmul(self, other: 'KheraMATArray') -> 'KheraMATArray':
        """Matrix multiplication (* in MATLAB) with scalar expansion support"""
        b = other._array if isinstance(other, KheraMATArray) else np.array(other)
        if self._array.size == 1 or b.size == 1:
            return KheraMATArray(self._array * b)
        return KheraMATArray(np.matmul(self._array, b))

    def dot_mul(self, other: Any) -> 'KheraMATArray':
        """Elementwise multiplication (.* in MATLAB)"""
        b = other._array if isinstance(other, KheraMATArray) else other
        return KheraMATArray(self._array * b)

    def matdiv(self, other: Any) -> 'KheraMATArray':
        """Matrix right division (/ in MATLAB: A / B = A * inv(B)) with scalar expansion"""
        b = other._array if isinstance(other, KheraMATArray) else np.array(other)
        if b.size == 1:
            return KheraMATArray(self._array / b)
        if self._array.size == 1:
            return KheraMATArray(self._array * np.linalg.pinv(b))
        return KheraMATArray(np.matmul(self._array, np.linalg.pinv(b)))

    def dot_div(self, other: Any) -> 'KheraMATArray':
        """Elementwise division (./ in MATLAB)"""
        b = other._array if isinstance(other, KheraMATArray) else other
        return KheraMATArray(self._array / b)

    def matldiv(self, other: Any) -> 'KheraMATArray':
        """Matrix left division (\\ in MATLAB: A \\ B = inv(A) * B or least-squares)"""
        b = other._array if isinstance(other, KheraMATArray) else np.array(other)
        if self._array.size == 1:
            return KheraMATArray(b / self._array)
        if b.size == 1:
            return KheraMATArray(np.linalg.pinv(self._array) * b)
        if self._array.ndim == 2 and b.ndim in (1, 2) and self._array.shape[0] == self._array.shape[1]:
            try:
                return KheraMATArray(np.linalg.solve(self._array, b))
            except np.linalg.LinAlgError:
                return KheraMATArray(np.linalg.lstsq(self._array, b, rcond=None)[0])
        else:
            return KheraMATArray(np.linalg.lstsq(self._array, b, rcond=None)[0])

    def dot_ldiv(self, other: Any) -> 'KheraMATArray':
        """Elementwise left division (.\\ in MATLAB: A .\\ B = B ./ A)"""
        b = other._array if isinstance(other, KheraMATArray) else other
        return KheraMATArray(b / self._array)

    def matpow(self, other: Any) -> 'KheraMATArray':
        """Matrix power (^ in MATLAB)"""
        p = int(other._array if isinstance(other, KheraMATArray) else other)
        return KheraMATArray(np.linalg.matrix_power(self._array, p))

    def dot_pow(self, other: Any) -> 'KheraMATArray':
        """Elementwise power (.^ in MATLAB)"""
        b = other._array if isinstance(other, KheraMATArray) else other
        return KheraMATArray(self._array ** b)

    def transpose(self) -> 'KheraMATArray':
        """Conjugate transpose (' in MATLAB)"""
        return KheraMATArray(self._array.conj().T)

    def dot_transpose(self) -> 'KheraMATArray':
        """Non-conjugate transpose (.' in MATLAB)"""
        return KheraMATArray(self._array.T)

    def __neg__(self):
        return KheraMATArray(-self._array)

    # Comparisons
    def __eq__(self, other):
        b = other._array if isinstance(other, KheraMATArray) else other
        return KheraMATArray(self._array == b)

    def __ne__(self, other):
        b = other._array if isinstance(other, KheraMATArray) else other
        return KheraMATArray(self._array != b)

    def __lt__(self, other):
        b = other._array if isinstance(other, KheraMATArray) else other
        return KheraMATArray(self._array < b)

    def __le__(self, other):
        b = other._array if isinstance(other, KheraMATArray) else other
        return KheraMATArray(self._array <= b)

    def __gt__(self, other):
        b = other._array if isinstance(other, KheraMATArray) else other
        return KheraMATArray(self._array > b)

    def __ge__(self, other):
        b = other._array if isinstance(other, KheraMATArray) else other
        return KheraMATArray(self._array >= b)

    def __and__(self, other):
        b = other._array if isinstance(other, KheraMATArray) else other
        return KheraMATArray(np.logical_and(self._array, b))

    def __rand__(self, other):
        b = other._array if isinstance(other, KheraMATArray) else other
        return KheraMATArray(np.logical_and(b, self._array))

    def __or__(self, other):
        b = other._array if isinstance(other, KheraMATArray) else other
        return KheraMATArray(np.logical_or(self._array, b))

    def __ror__(self, other):
        b = other._array if isinstance(other, KheraMATArray) else other
        return KheraMATArray(np.logical_or(b, self._array))

    def __str__(self) -> str:
        if self._array.size == 0:
            r, c = self._array.shape
            return f"   Empty matrix: {r}-by-{c}"
        if self._array.shape == (1, 1):
            val = self._array[0, 0]
            if isinstance(val, (float, np.floating)):
                if np.isnan(val) or np.isinf(val):
                    return f"     {val}"
                if val == 0:
                    return "     0"
                return f"    {val:.4g}"
            return f"     {val}"
        
        # Matrix output formatting
        lines = []
        rows, cols = self._array.shape
        for r in range(min(rows, 50)): # Cap output formatting lines for performance
            row_items = []
            for c in range(min(cols, 20)):
                v = self._array[r, c]
                if isinstance(v, (float, np.floating)):
                    if np.isnan(v) or np.isinf(v):
                        row_items.append(f"{v}")
                    elif v == 0:
                        row_items.append("   0")
                    else:
                        # MATLAB uses %g-like formatting with precision 4 or 5
                        # We use .4g which gives 4 significant digits
                        fmt_v = f"{v:.4g}"
                        # Try to align it a bit
                        row_items.append(fmt_v.rjust(6))
                else:
                    row_items.append(str(v))
            row_str = "    " + "  ".join(row_items)
            lines.append(row_str)
        if rows > 50 or cols > 20:
            lines.append("    ... [Output truncated]")
        return "\n".join(lines)

    def __repr__(self) -> str:
        r, c = self._array.shape
        return f"KheraMATArray({r}x{c} {self._array.dtype})"
