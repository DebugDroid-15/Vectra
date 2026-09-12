"""
Vectra — Scientific Computing Engine & MATLAB-Compatible IDE
"""

from .runtime.interpreter import Interpreter
from .runtime.kheramat_array import KheraMATArray
from .runtime.workspace import Workspace
from .logger import setup_logging, get_logger

__version__ = "1.0.0"
__all__ = ["Interpreter", "KheraMATArray", "Workspace", "setup_logging", "get_logger", "__version__"]
