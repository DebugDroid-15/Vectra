"""
Application Service Abstraction Layer for Vectra

Decouples GUI elements from internal interpreter and workspace state.
"""

from typing import List, Any, Optional, Dict
import os
from .runtime.interpreter import Interpreter
from .runtime.workspace import Workspace, VariableInfo
from .logger import get_logger

class ExecutionService:
    def __init__(self, interpreter: Optional[Interpreter] = None):
        self.logger = get_logger("services.execution")
        self.interpreter = interpreter or Interpreter()

    def execute_command(self, code: str) -> List[str]:
        self.logger.debug(f"Executing command via ExecutionService: {code}")
        return self.interpreter.eval_code(code)

    def run_script_file(self, file_path: str) -> List[str]:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Script file not found: {file_path}")
        with open(file_path, "r", encoding="utf-8") as f:
            code = f.read()
        self.logger.info(f"Running script file: {file_path}")
        return self.execute_command(code)

class WorkspaceService:
    def __init__(self, workspace: Workspace):
        self.workspace = workspace

    def list_variables(self) -> List[VariableInfo]:
        return self.workspace.get_info_list()

    def get_variable(self, name: str) -> Any:
        return self.workspace.get(name)

    def delete_variable(self, name: str):
        self.workspace.clear(name)

    def clear_workspace(self):
        self.workspace.clear()
