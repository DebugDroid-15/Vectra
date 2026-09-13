import pytest
import os
from kheramat.services import ExecutionService, WorkspaceService
from kheramat.runtime.interpreter import Interpreter

def test_execution_service_command():
    service = ExecutionService()
    logs = service.execute_command("x = 10; y = x * 2;")
    assert service.interpreter.workspace.get("y")._array.item() == 20

def test_workspace_service():
    interp = Interpreter()
    exec_serv = ExecutionService(interp)
    ws_serv = WorkspaceService(interp.workspace)
    
    exec_serv.execute_command("A = [1 2; 3 4];")
    assert ws_serv.get_variable("A")._array.shape == (2, 2)
    var_names = [v.name for v in ws_serv.list_variables()]
    assert "A" in var_names
    
    ws_serv.delete_variable("A")
    assert not interp.workspace.has("A")
