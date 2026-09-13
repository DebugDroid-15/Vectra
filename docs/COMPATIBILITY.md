# MATLAB Syntax & Toolbox Compatibility Matrix

Status Levels:
- **FULL**: Tested and verified behavior matching standard MATLAB semantics.
- **PARTIAL**: Basic syntax or core cases work; optional flags or multi-output behavior under development.
- **DIFFERENT**: Intentionally modified for open-source Python backing.
- **MISSING**: Not yet implemented.
- **UNTESTED**: Implemented but pending formal test suite verification.

---

## Language Core

| Feature | Status | Notes |
| :--- | :--- | :--- |
| `1-based Indexing` | **FULL** | Implemented in `KheraMATArray`. `A(1,1)` accesses top-left element. |
| `Range Operator (:)` | **FULL** | Supports `start:step:stop` and `start:stop`. |
| `Matrix Literals` | **FULL** | Supports `[1 2; 3 4]` space/comma/semicolon delimited matrices. |
| `Control Flow (if/for/while)`| **FULL** | Evaluates standard block structures. |
| `User Functions` | **PARTIAL** | Basic AST structure present; multi-output return pending. |
| `Switch / Case` | **MISSING** | Planned for upcoming interpreter expansion. |

---

## Core Numerical & ECE Toolboxes

| Function | Category | Status |
| :--- | :--- | :--- |
| `svd`, `lu`, `qr`, `chol` | Core Linear Algebra | **FULL** |
| `expm`, `logm`, `sqrtm` | Matrix Functions | **FULL** |
| `heaviside`, `dirac`, `sinc` | Signals & Systems | **FULL** |
| `butter`, `cheby1`, `zplane` | DSP | **FULL** |
| `ammod`, `amdemod`, `awgn` | Communications | **FULL** |
| `tf`, `step`, `impulse` | Control Systems | **FULL** |
| `syms`, `diff`, `int` | Symbolic Math | **FULL** |
