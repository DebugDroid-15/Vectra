import pytest
import numpy as np
from kheramat.runtime.interpreter import Interpreter

def test_matrix_decompositions():
    interp = Interpreter()
    interp.eval_code("""
    A = [1 2; 3 4];
    [U, S, V] = svd(A);
    [L, U2, P] = lu(A);
    [Q, R] = qr(A);
    c = cond(A);
    E = expm(A);
    """)
    assert interp.workspace.get("U")._array.shape == (2, 2)
    assert interp.workspace.get("Q")._array.shape == (2, 2)
    assert interp.workspace.get("E")._array.shape == (2, 2)

def test_polynomials_and_multidimensional():
    interp = Interpreter()
    interp.eval_code("""
    y = polyval([1 0 1], 2);
    C = conv2([1 2; 3 4], [1 0; 0 1]);
    cs = cumsum([1 2 3]);
    f = fliplr([1 2 3]);
    r = rot90([1 2; 3 4]);
    """)
    assert interp.workspace.get("y")._array.item() == 5
    assert interp.workspace.get("C")._array.shape == (3, 3)
    assert interp.workspace.get("f")._array[0, 0] == 3

def test_dynamic_fallback():
    interp = Interpreter()
    # Sinc and hypot via dynamic NumPy fallback dispatch
    interp.eval_code("""
    h = hypot(3, 4);
    """)
    assert interp.workspace.get("h")._array.item() == 5.0

