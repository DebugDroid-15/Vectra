# Vectra Production Roadmap

This roadmap outlines the systematic phases required to evolve Vectra into a production-grade desktop scientific-computing application.

---

## Roadmap Phases

### Phase 1: Baseline & Core Architecture (Completed / In Progress)
- Audit codebase and generate baseline status documentation (`PRODUCT_STATUS.md`, `ARCHITECTURE.md`, `COMPATIBILITY.md`, etc.).
- Maintain zero-regression quality gate across existing 27 pytest test suites.

### Phase 2: Runtime Isolation & Service Layer
- Decouple scientific interpreter and workspace runtime from PySide6 GUI widgets.
- Introduce `ExecutionService`, `WorkspaceService`, `FigureManager`, and `DiagnosticsService`.

### Phase 3: Language & Interpreter Hardening
- Expand AST parser for user functions (`function [a,b] = f(x)`), anonymous functions (`@`), `switch/case`, and `try/catch`.
- Improve error formatting with code snippet line pointers.

### Phase 4: Graphics & Figure Manager
- Implement multi-figure support (`figure(1)`, `figure(2)`, `gcf`, `gca`, `close all`) separating figure windows from global GUI canvas.

### Phase 5: Testing Architecture Expansion
- Restructure `tests/` into `unit/`, `integration/`, `regression/`, `compatibility/`, and `gui/`.

### Phase 6: Standalone Packaging & Distribution
- Configure PyInstaller / Nuitka frozen binary build pipeline to generate standalone `VectraSetup.exe` without requiring Python installation on target machines.
