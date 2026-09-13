# Vectra Architecture Specification

## Overview

Vectra enforces strict separation between the scientific computing runtime and the desktop user interface.

```
                  VECTRA SOURCE / REPL
                           │
                           ▼
                        Lexer
                           │
                           ▼
                        Parser
                           │
                           ▼
                          AST
                           │
                           ▼
                        Runtime
                           │
          ┌────────────────┼────────────────┐
          ▼                ▼                ▼
       Workspace       Toolboxes         Graphics
          │                │                │
          └────────────────┼────────────────┘
                           ▼
                 NumPy / SciPy / SymPy
                           │
                           ▼
                       Results
                           │
                           ▼
                 Application Services
          (Execution, Workspace, Figures)
                           │
                           ▼
                      PySide6 GUI
```

## Layer Definitions

1. **Language Layer** (`src/kheramat/lang/`): Lexer, Token definitions, AST nodes, Parser. Converts raw MATLAB code strings into structured AST blocks.
2. **Runtime Layer** (`src/kheramat/runtime/`): Interpreter visitor engine, `KheraMATArray` (1-based ndarray wrapper), `Workspace` variable scope.
3. **Toolbox Layer** (`src/kheramat/toolbox/`): Core math, Signals, DSP, Communications, Electromagnetics, Control, and Symbolic functions wrapping NumPy/SciPy/SymPy.
4. **GUI Layer** (`src/kheramat/gui/`): Desktop PySide6 user interface consuming application services.
