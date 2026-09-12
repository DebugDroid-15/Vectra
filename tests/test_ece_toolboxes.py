import pytest
import numpy as np
from kheramat.runtime.interpreter import Interpreter

def test_dsp_butter():
    interp = Interpreter()
    interp.eval_code("[b, a] = butter(4, 0.2);")
    b = interp.workspace.get("b")
    a = interp.workspace.get("a")
    assert b._array.shape[1] > 0
    assert a._array.shape[1] > 0

def test_communications_ammod():
    interp = Interpreter()
    interp.eval_code("""
    t = 0:0.001:0.1;
    m = sin(2*pi*5*t);
    s = ammod(m, 100, 1000);
    """)
    s = interp.workspace.get("s")
    assert s._array.shape[1] == interp.workspace.get("t")._array.shape[1]

def test_control_tf_step():
    interp = Interpreter()
    interp.eval_code("""
    G = tf([1], [1, 2, 1]);
    [y, t] = step(G);
    """)
    y = interp.workspace.get("y")
    assert y._array.shape[1] > 0

def test_symbolic_diff():
    interp = Interpreter()
    interp.eval_code("""
    x = syms('x');
    f = x^2 + 3*x;
    """)
    assert interp.workspace.has("x")

