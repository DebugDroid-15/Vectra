import pytest
import os
import sys
from kheramat.cli import run_cli

def test_cli_eval(capsys):
    ret = run_cli(["--eval", "x = 10; y = x * 3;"])
    assert ret == 0

def test_cli_run_script(tmp_path, capsys):
    script_file = tmp_path / "test_script.m"
    script_file.write_text("a = 5;\nb = a + 10;\n", encoding="utf-8")
    
    ret = run_cli(["--run", str(script_file)])
    assert ret == 0

def test_cli_file_not_found(capsys):
    ret = run_cli(["--run", "non_existent_file.m"])
    assert ret == 1
