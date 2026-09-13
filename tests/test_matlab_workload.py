import os
import pytest
from kheramat.services import ExecutionService
from kheramat.runtime.interpreter import Interpreter

def test_full_matlab_engineering_workload():
    script_path = os.path.join(os.path.dirname(__file__), "regression", "vectra_matlab_functionality_test.m")
    with open(script_path, "r", encoding="utf-8") as f:
        code = f.read()

    interp = Interpreter()
    exec_service = ExecutionService(interp)
    
    logs = exec_service.execute_code(code)
    
    # 1. Assert Column-Major Indexing: A = [1 2; 3 4] -> A(2) == 3
    assert interp.workspace.get("linear_val")._array.item() == 3

    # 2. Assert Signal Shapes
    assert interp.workspace.get("t")._array.shape == (1, 2001)
    assert interp.workspace.get("x_noisy")._array.shape == (1, 2001)
    assert interp.workspace.get("filtered")._array.shape == (1, 2001)

    # 3. Assert Matrix SVD Results
    S = interp.workspace.get("S")._array
    assert S.shape == (2, 2)
