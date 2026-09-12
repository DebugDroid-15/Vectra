import pytest
import numpy as np
from kheramat.runtime.interpreter import Interpreter
from kheramat.runtime.kheramat_array import KheraMATArray

def test_acceptance_test_1_matrix_math():
    interp = Interpreter()
    interp.eval_code("A = [1 2; 3 4];")
    interp.eval_code("B = A * A;")

    res_B = interp.workspace.get("B")
    expected = np.array([[7.0, 10.0], [15.0, 22.0]])
    np.testing.assert_allclose(res_B._array, expected)

def test_acceptance_test_2_colon_range_and_sin():
    interp = Interpreter()
    interp.eval_code("x = 0:0.1:10;")
    interp.eval_code("y = sin(x);")

    x_arr = interp.workspace.get("x")
    y_arr = interp.workspace.get("y")

    assert x_arr.shape == (1, 101)
    assert y_arr.shape == (1, 101)
    np.testing.assert_allclose(y_arr._array, np.sin(x_arr._array))

def test_det_and_inv():
    interp = Interpreter()
    interp.eval_code("A = [4 7; 2 6];")
    interp.eval_code("d = det(A);")
    interp.eval_code("A_inv = inv(A);")

    d_val = interp.workspace.get("d")._array.item()
    assert abs(d_val - 10.0) < 1e-5
    np.testing.assert_allclose(interp.workspace.get("A_inv")._array, np.linalg.inv([[4, 7], [2, 6]]))

def test_clc_clear_and_script():
    interp = Interpreter()
    script = (
        "clc;\n"
        "clear;\n"
        "x = 0:0.1:10;\n"
        "y = sin(x);\n"
        "figure;\n"
        "plot(x,y);\n"
        "xlabel('Time (s)');\n"
        "ylabel('Amplitude');\n"
        "title('Sine Wave Demonstration');\n"
        "grid on;\n"
    )
    logs = interp.eval_code(script)
    assert interp.workspace.has("x")
    assert interp.workspace.has("y")
    assert interp.workspace.get("x").shape == (1, 101)

def test_ct_and_dt_signals():
    interp = Interpreter()
    script = (
        "t = -5:0.1:5;\n"
        "u = heaviside(t);\n"
        "n = -5:5;\n"
        "delta = unitimpulse(n);\n"
        "x1 = [1 2 3];\n"
        "h1 = [1 1];\n"
        "y1 = conv(x1, h1);\n"
        "figure;\n"
        "subplot(2, 1, 1);\n"
        "plot(t, u);\n"
        "title('CT Unit Step');\n"
        "subplot(2, 1, 2);\n"
        "stem(n, delta);\n"
        "title('DT Unit Impulse');\n"
    )
    interp.eval_code(script)
    assert interp.workspace.has("u")
    assert interp.workspace.has("delta")
    assert interp.workspace.has("y1")
    np.testing.assert_allclose(interp.workspace.get("y1")._array, [[1, 3, 5, 3]])

def test_user_exact_script():
    interp = Interpreter()
    script = (
        "clc;\n"
        "clear;\n"
        "close all;\n\n"
        "t = -5:0.01:5;\n"
        "x = zeros(size(t));\n"
        "for i = 1:length(t)\n"
        "    if t(i) >= 0\n"
        "        x(i) = t(i);\n"
        "    end\n"
        "end\n"
        "plot(t, x, 'LineWidth', 2);\n"
        "xlabel('Time (t)');\n"
        "ylabel('Amplitude');\n"
        "title('Continuous Time Ramp Signal');\n"
        "gtext('Registration No.: 24E118016');\n"
        "grid on;\n"
    )
def test_ss_lab1_composite_signals():
    interp = Interpreter()
    script = (
        "clc; clear; close all;\n"
        "t = -2:0.001:2;\n"
        "x1 = zeros(size(t));\n"
        "x2 = zeros(size(t));\n"
        "x3 = zeros(size(t));\n"
        "for i = 1:length(t)\n"
        " x1(i) = sin(2*pi*t(i)) + cos(4*pi*t(i));\n"
        " x2(i) = exp(-t(i)/3) * sin(t(i));\n"
        " u = 0;\n"
        " if t(i) >= 0\n"
        " u = 1;\n"
        " end\n"
        " x3(i) = 2*sin(2*pi*t(i)) + 3*cos(4*pi*t(i)) + 2*u;\n"
        "end\n"
        "subplot(3, 1, 1);\n"
        "plot(t, x1);\n"
        "subplot(3, 1, 2);\n"
        "plot(t, x2);\n"
        "subplot(3, 1, 3);\n"
        "plot(t, x3);\n"
        "gtext('Registration No.: 24E118B16');\n"
        "grid on;\n"
    )
    interp.eval_code(script)
    assert interp.workspace.has("x1")
    assert interp.workspace.has("x2")
    assert interp.workspace.has("x3")
    assert interp.workspace.get("x1").shape == (1, 4001)

