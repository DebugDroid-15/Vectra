import numpy as np
from typing import Dict, Any, List
from .kheramat_array import KheraMATArray

class VariableInfo:
    def __init__(self, name: str, value: Any):
        self.name = name
        self.value = value

    @property
    def size_str(self) -> str:
        if isinstance(self.value, KheraMATArray):
            r, c = self.value.shape
            return f"{r}×{c}"
        elif isinstance(self.value, (int, float, str, bool, complex)):
            return "1×1"
        elif isinstance(self.value, list):
            return f"1×{len(self.value)}"
        return "1×1"

    @property
    def type_str(self) -> str:
        if isinstance(self.value, KheraMATArray):
            return f"double ({self.value.dtype})"
        return type(self.value).__name__

    @property
    def value_str(self) -> str:
        s = str(self.value).strip()
        if len(s) > 40:
            return s[:37] + "..."
        return s

class Workspace:
    def __init__(self):
        self.variables: Dict[str, Any] = {}
        self.history: List[str] = []
        self._load_constants()

    def _load_constants(self):
        self.variables["pi"] = KheraMATArray(np.pi)
        self.variables["e"] = KheraMATArray(np.e)
        self.variables["eps"] = KheraMATArray(np.finfo(float).eps)
        self.variables["inf"] = KheraMATArray(np.inf)
        self.variables["nan"] = KheraMATArray(np.nan)
        self.variables["i"] = KheraMATArray(1j)
        self.variables["j"] = KheraMATArray(1j)

    def set(self, name: str, value: Any):
        if not isinstance(value, KheraMATArray) and not isinstance(value, str):
            if isinstance(value, (int, float, complex, bool, list, np.ndarray)):
                value = KheraMATArray(value)
        self.variables[name] = value

    def get(self, name: str) -> Any:
        if name in self.variables:
            return self.variables[name]
        raise KeyError(f"Undefined variable or function '{name}'.")

    def has(self, name: str) -> bool:
        return name in self.variables

    def clear(self, name: str = None):
        if name:
            self.variables.pop(name, None)
        else:
            self.variables.clear()
            self._load_constants()

    def get_info_list(self) -> List[VariableInfo]:
        return [VariableInfo(k, v) for k, v in self.variables.items()]
