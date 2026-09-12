import pytest
import numpy as np
from kheramat.runtime.interpreter import Interpreter

def test_pdf_array_commands():
    interp = Interpreter()
    interp.eval_code("""
    x = logspace(1, 3, 5);
    D = diag([1 2 3]);
    c = cross([1 0 0], [0 1 0]);
    d = dot([1 2], [3 4]);
    R = reshape(1:6, 2, 3);
    T = repmat([1 2], 2, 2);
    S = sort([3 1 2]);
    """)
    assert interp.workspace.get("D")._array.shape == (3, 3)
    assert interp.workspace.get("c")._array[0, 2] == 1
    assert interp.workspace.get("d")._array.item() == 11

def test_pdf_sub2ind_ind2sub_find():
    interp = Interpreter()
    interp.eval_code("""
    idx = sub2ind([3, 3], 2, 2);
    [r, c] = ind2sub([3, 3], 5);
    pos = find([0 5 0 10]);
    """)
    assert interp.workspace.get("idx")._array.item() == 5
    assert interp.workspace.get("r")._array.item() == 2
    assert interp.workspace.get("c")._array.item() == 2

def test_pdf_poly_roots_trapz():
    interp = Interpreter()
    interp.eval_code("""
    p = poly([1, 2]);
    r = roots(p);
    t = 0:0.1:1;
    y = t.^2;
    area = trapz(t, y);
    """)
    assert len(interp.workspace.get("p")._array.flatten()) == 3
    assert abs(interp.workspace.get("area")._array.item() - 0.335) < 0.05

