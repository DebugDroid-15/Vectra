# Vectra Architecture Specification

## System Architecture

```
[ MATLAB-Style Script (.m) / REPL Input ]
                    │
                    ▼
          [ Lexer (lexer.py) ]
                    │ Token Stream
                    ▼
         [ Parser (parser.py) ]
                    │ AST Nodes
                    ▼
     [ Interpreter (interpreter.py) ] ◄──────► [ Scope / Workspace (workspace.py) ]
                    │
        ┌───────────┴───────────┐
        ▼                       ▼
[ KheraMATArray ]        [ Function Registry ]
(Column-Major Array)     (Toolboxes)
        │                       │
        ▼                       ▼
 [ NumPy Backend ]       [ Core Math / Plotting / Controls / Signal / Comms / Symbolic ]
```

## Subsystem Isolation

1. **Numerical Engine Isolation**: The interpreter (`interpreter.py`) and array implementation (`kheramat_array.py`) are strictly headlessly executable and maintain zero dependencies on PySide6 or any GUI widgets.
2. **Graphics Context Isolation**: Plotting commands route through `plotting.py` using Matplotlib backend rendering without forcing synchronous GUI thread execution.
3. **Workspace Isolation**: Scope variables are managed inside `Workspace` instances, supporting isolated function evaluation stack frames.
