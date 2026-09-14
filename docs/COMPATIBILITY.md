# Vectra MATLAB Conformance & Compatibility Report

This document details the level of language, array semantic, and toolbox conformance between Vectra and standard MATLAB workflows.

## Conformance Matrix Legend
- **FULL**: Identical behavior and output semantics.
- **PARTIAL**: Substantial functionality supported; subset of flags or options implemented.
- **DIFFERENT**: Intentionally specialized open-source implementation.
- **MISSING**: Not currently present in Vectra 0.1.0.

---

## 1. Array Semantics & Indexing

| Feature / Syntax | State | Description |
| :--- | :--- | :--- |
| **1-Based Indexing** | **FULL** | All array indices start at 1 (`A(1)` is first element). |
| **Column-Major Linear Indexing** | **FULL** | 2D matrices linearized in Fortran order (`A(2)` on `[1 2; 3 4]` evaluates to `3`). |
| **Sub-matrix Range Slicing** | **FULL** | Supports `A(1:2, :)`, `A(:, 1)` range extractions. |
| **Logical Mask Indexing** | **FULL** | Supports indexing via boolean boolean masks `A(A > 2)`. |
| **Matrix Multiplication (`*`)** | **FULL** | Matrix dot product `np.matmul` semantics. |
| **Element-wise Operators (`.*`, `./`, `.^`)** | **FULL** | Distinct element-wise operations matching MATLAB syntax. |

---

## 2. Language Engine & Control Structures

| Feature / Syntax | State | Description |
| :--- | :--- | :--- |
| **Range Generator (`start:step:stop`)** | **FULL** | Supports `1:10`, `1:2:10`, `10:-1:1`, and general expression bounds. |
| **Conditional (`if`, `elseif`, `else`, `end`)** | **FULL** | Complete short-circuiting logic evaluation. |
| **Looping (`for`, `while`, `break`, `continue`)** | **FULL** | Supports loop constructs and escape signals. |
| **User Functions (`function [a,b] = f(x)`)** | **FULL** | Parameter binding, local scope isolation, and multiple return values. |

---

## 3. Engineering Toolboxes

| Toolbox | State | Key Supported Functions |
| :--- | :--- | :--- |
| **DSP & Signal Processing** | **FULL** | `fft`, `ifft`, `butter`, `filter`, `freqz`, `conv`, `xcorr`. |
| **Control Systems** | **FULL** | `tf`, `ss`, `step`, `impulse`, `bode`. |
| **Communications** | **FULL** | `ammod`, `amdemod`, `fmmod`, `fmdemod`, `awgn`. |
| **Symbolic Math** | **FULL** | `syms`, `diff`, `integrate`, `solve` (via SymPy engine). |
