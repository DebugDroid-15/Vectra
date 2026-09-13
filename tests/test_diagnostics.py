import pytest
from kheramat.diagnostics import VectraDiagnostic

def test_vectra_diagnostic_formatting():
    diag = VectraDiagnostic(
        code="VEC-INDEX-001",
        message="Array index out of bounds",
        line=12,
        column=5,
        file_path="script.m",
        suggestion="Ensure index is within 1:length(A)"
    )
    formatted = diag.format_user_facing()
    assert "VEC-INDEX-001" in formatted
    assert "Line 12, Column 5" in formatted
    assert "Ensure index is within" in formatted

