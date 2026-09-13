"""
Vectra Structured Diagnostics Engine
"""

from typing import Optional

class VectraDiagnostic:
    def __init__(
        self,
        code: str,
        message: str,
        line: int = 1,
        column: int = 1,
        file_path: Optional[str] = None,
        suggestion: Optional[str] = None
    ):
        self.code = code
        self.message = message
        self.line = line
        self.column = column
        self.file_path = file_path or "Command Window"
        self.suggestion = suggestion

    def format_user_facing(self) -> str:
        s = f"[{self.code}] {self.message}\n"
        s += f"File: {self.file_path} (Line {self.line}, Column {self.column})\n"
        if self.suggestion:
            s += f"Suggestion: {self.suggestion}\n"
        return s

    def __repr__(self) -> str:
        return f"VectraDiagnostic({self.code}, {self.message!r}, line={self.line}, col={self.column})"
