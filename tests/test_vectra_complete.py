import os
import pytest
from kheramat.services import ExecutionService
from kheramat.runtime.interpreter import Interpreter
from kheramat.runtime.kheramat_array import KheraMATArray

def test_ultimate_vectra_acceptance_workload():
    script_path = os.path.join(os.path.dirname(__file__), "regression", "VECTRA_COMPLETE_TEST.m")
    with open(script_path, "r", encoding="utf-8") as f:
        code = f.read()

    interp = Interpreter()
    exec_service = ExecutionService(interp)
    
    logs = exec_service.execute_code(code)

    # 1. Column-Major Indexing: A = [1 2; 3 4] -> A(2) == 3
    assert interp.workspace.get("linear_val")._array.item() == 3

    # 2. Signal Shapes
    assert interp.workspace.get("t")._array.shape == (1, 2001)
    assert interp.workspace.get("x_noisy")._array.shape == (1, 2001)
    assert interp.workspace.get("filtered")._array.shape == (1, 2001)

    # 3. Linear Algebra
    assert interp.workspace.get("det_val")._array.item() == pytest.approx(-2.0)

    # 4. Symbolic Math Integration
    assert "z" in str(interp.workspace.get("d_expr"))
