import pytest
import numpy as np
from kheramat.runtime.interpreter import Interpreter

def test_user_defined_function():
    interp = Interpreter()
    interp.eval_code("""
    function y = square_it(x)
        y = x.^2;
    end
    res = square_it(5);
    """)
    assert interp.workspace.get("res")._array.item() == 25

def test_function_multiple_returns():
    interp = Interpreter()
    interp.eval_code("""
    function [a, b] = calc_stats(x)
        a = sum(x);
        b = mean(x);
    end
    [s, m] = calc_stats([1 2 3 4 5]);
    """)
    assert interp.workspace.get("s")._array.item() == 15
    assert interp.workspace.get("m")._array.item() == 3

def test_break_continue():
    interp = Interpreter()
    interp.eval_code("""
    acc = 0;
    for i = 1:10
        if i == 5
            break;
        end
        acc = acc + i;
    end
    """)
    assert interp.workspace.get("acc")._array.item() == 10

