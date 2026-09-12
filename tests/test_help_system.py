import pytest
from kheramat.runtime.interpreter import Interpreter
from kheramat.help_docs import get_help_text, open_doc_url

def test_help_database_text():
    plot_help = get_help_text("plot")
    assert "2D line plot" in plot_help
    assert "https://www.mathworks.com/help/matlab/ref/plot.html" in plot_help

def test_interpreter_help_command():
    interp = Interpreter()
    res = interp.eval_code("help butter")
    assert len(res) > 0
    assert "Butterworth digital and analog filter design" in res[0]

def test_interpreter_help_ammod():
    interp = Interpreter()
    res = interp.eval_code("help ammod")
    assert len(res) > 0
    assert "Amplitude modulation" in res[0]

