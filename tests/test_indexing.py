import pytest
import numpy as np
from kheramat.runtime.interpreter import Interpreter

def test_column_major_linear_indexing():
    interp = Interpreter()
    interp.eval_code("""
    A = [1 2; 3 4];
    v2 = A(2);
    v3 = A(3);
    """)
    assert interp.workspace.get("v2")._array.item() == 3
    assert interp.workspace.get("v3")._array.item() == 2

