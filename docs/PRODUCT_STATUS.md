# Vectra Product Status

**Product**: VECTRA  
**Tagline**: Compute. Simulate. Innovate.  
**Version**: 1.0.0 (Development / Refactoring Baseline)  
**Status Date**: 2026-09-13  

---

## 1. Executive Summary

Vectra is an independent, free, open-source scientific computing and engineering desktop environment designed as a practical alternative to MATLAB. This document establishes the empirical baseline of the existing codebase.

---

## 2. Capability Audit

| Module / Component | State | Status Description |
| :--- | :--- | :--- |
| **Lexer & Tokens** | ✅ Functional | Tokenizes numbers, identifiers, matrix brackets `[]`, ranges `:`, strings, math ops. |
| **Parser & AST** | ⚠️ Partial | Parses assignments, function calls, binary ops, matrix literals. Lacks `function` definitions, `switch/case`, `try/catch`. |
| **Interpreter Core** | ⚠️ Partial | Evaluates AST nodes using visitor pattern. Implements basic `for`, `while`, `if`. |
| **Matrix Array (`KheraMATArray`)**| ⚠️ Partial | Wraps `np.ndarray`. Implements 1-based indexing, range slicing, matrix arithmetic overloads. |
| **Workspace Inspector** | ✅ Functional | Real-time table viewing variable shapes, types, and values. |
| **Script Editor** | ✅ Functional | PySide6 QPlainTextEdit with line numbers, syntax highlighting, active line highlight. |
| **Command Window REPL** | ✅ Functional | Prompt `>>`, history navigation (`Up`/`Down`), output redirection. |
| **Figure Window** | ⚠️ Partial | Matplotlib Qt canvas integration with navigation toolbar. Uses global singleton canvas. |
| **ECE Toolboxes** | ⚠️ Partial | Supports basic SS, DSP, Communications, Control (`tf`, `step`), Symbolic functions. |
| **Logging & Crash Handler** | ✅ Functional | Thread-safe rotating logger (`vectra_app.log`) and crash exception hook (`vectra_crash.log`). |
| **Launcher (`Vectra.bat`)** | ✅ Functional | Universal Python auto-scanner, isolated `.venv` setup, PATH sanitization. |
| **Packaging / Installer** | ❌ Missing | Relies on runtime virtualenv creation; lacks standalone frozen binary installer (`VectraSetup.exe`). |

---

## 3. Verified Metrics

- **Automated Tests**: 27 unit test suites in `tests/` passing 100% via `pytest`.
- **Supported OS**: Windows (tested), Linux (CI headless test passing), macOS (untested).
