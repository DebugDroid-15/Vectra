# VECTRA

<div align="center">

```
  ___ ___ ____________ ________ _________    _____   
 /   |   \\______   \\_____  \\______   \  /  _  \  
/    ~    \|    |  _/ /   |   \|    |  _/ /  /_\  \ 
\    Y    /|    |   \/    |    \    |   \/    |    \
 \___|_  / |______  /\_______  /______  /\____|__  /
       \/         \/         \/       \/         \/ 
```

### **Compute. Simulate. Innovate.**

**An Independent, Open-Source Scientific Computing and Engineering Desktop Environment**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python: 3.10+](https://img.shields.io/badge/Python-3.10%2B-brightgreen.svg)](https://python.org)
[![PySide6](https://img.shields.io/badge/GUI-PySide6-41CD52.svg)](https://qt.io)
[![Build Status](https://img.shields.io/badge/Tests-38%20Passed-success.svg)](tests/)

---

[Key Features](#-key-features) •
[Architecture](#-architecture-overview) •
[Installation](#-installation--quick-start) •
[Language Specifications](#-language--syntax-reference) •
[Toolbox Reference](#-toolbox-ecosystem) •
[Headless Execution](#-headless-cli--automation) •
[Contributing](#-contributing--development)

</div>

---

## ───────── Executive Overview ─────────

**Vectra** is a standalone, free, open-source scientific computing engine and graphical desktop platform designed for engineers, researchers, educators, and students. Developed as a modern Python-powered alternative to proprietary matrix environments like MATLAB, Vectra provides an intuitive syntax, matrix-first language runtime, and dedicated toolboxes across Digital Signal Processing (DSP), Control Systems, Communications, Symbolic Math, and State-Space modeling.

Whether running as an interactive desktop environment or headlessly via `vectra-cli`, Vectra gives engineers a zero-dependency setup with native support for matrix math, 1-based Fortran column-major linear indexing, custom user functions, and rich graphical visualization.

---

## 🚀 Key Features

### 🧠 Modern AST Language Engine
* **Matrix-First Semantics**: Native 2D matrix literal constructions `[1 2 3; 4 5 6]`, range generators `1:0.1:10`, element-wise operator overloads (`.*`, `./`, `.^`), and matrix multiplications (`*`).
* **Fortran Column-Major Indexing**: Authentic 1-based linear indexing (`A(2)` on `[1 2; 3 4]` yields `3`), matrix sub-slicing (`A(1:2, :)`), and matrix resizing.
* **Control Flows & Functions**: Full support for `if/elseif/else`, `for` loops, `while` loops, loop signals (`break`, `continue`, `return`), and custom functions (`function [a, b] = myFunc(x, y)`).

### 🎨 Modern Desktop Interface
* **Catppuccin & Fluent Styling**: Aesthetic dark and light themes with rounded tab bars, custom scrollbars, styled action toolbars, and responsive dock panel splitting.
* **Interactive Command Window REPL**: Direct command input with prompt history (`Up`/`Down` key navigation), error formatting, and real-time workspace updates.
* **Multi-Tab Script Editor**: Advanced code editor with active line pointers, line numbers, and custom MATLAB syntax highlighting.
* **Live Workspace Inspector**: Real-time inspection table displaying active variable names, array shapes (`MxN`), data types, and current values.
* **Interactive Figure Window**: Built-in Matplotlib canvas toolbar enabling zooming, panning, grid toggling, and multi-subplot generation (`figure`, `subplot`, `plot`, `stem`).

### 📦 Comprehensive Engineering Toolboxes
* **Control Systems**: Transfer function creation (`tf(num, den)`), step response plotting (`step(sys)`), and impulse evaluation.
* **Digital Signal Processing (DSP)**: Fast Fourier Transforms (`fft`, `ifft`), frequency responses (`freqz`), digital filtering (`filter`), and windowing functions (`hamming`, `hann`).
* **Communications Engineering**: Analog and digital modulation schemes (`ammod`, `amdemod`, `fmmod`, `fmdemod`), and Bit Error Rate analysis tools.
* **State-Space Modeling**: State-Space matrices (`ss(A,B,C,D)`), controllability (`ctrb`), and observability (`obsv`) matrices.
* **Symbolic Math Engine**: Symbolic variable creation (`syms x y`), differentiation (`diff`), integration (`integrate`), and equation solving (`solve`).

---

## 🏗️ Architecture Overview

Vectra is structured as a layered system separating core language parsing, runtime execution context, domain-specific engineering toolboxes, and presentation GUI widgets:

```
                  ┌─────────────────────────────────────┐
                  │          Vectra Desktop GUI         │
                  │   (PySide6 / MainWindow / Dock)     │
                  └──────────────────┬──────────────────┘
                                     │
                 ┌───────────────────┴───────────────────┐
                 │          ExecutionService             │
                 │   (Decoupled App Execution Layer)     │
                 └───────────────────┬───────────────────┘
                                     │
          ┌──────────────────────────┼──────────────────────────┐
          │                          │                          │
┌─────────┴──────────┐     ┌─────────┴──────────┐     ┌─────────┴──────────┐
│  Parser & Tokens   │     │  Interpreter Core  │     │ Workspace Context  │
│(Lexer/AST/Grammar) │     │ (Visitor Pattern)  │     │(Variables/Symbols) │
└────────────────────┘     └────────────────────┘     └────────────────────┘
                                     │
                 ┌───────────────────┴───────────────────┐
                 │       Toolboxes & KheraMATArray       │
                 │(DSP / Control / Syms / Matplotlib Canvas)│
                 └───────────────────────────────────────┘
```

---

## 📥 Installation & Quick Start

### Prerequisites
* **Operating System**: Windows 10/11, Linux, or macOS.
* **Python**: Python 3.10, 3.11, 3.12, or 3.13.

### Quick Setup

1. **Clone the Repository**:
   ```bash
   git clone https.github.com/DebugDroid-15/Vectra.git
   cd Vectra
   ```

2. **Launch via Universal Automated Script (Windows)**:
   Simply run the root executable script:
   ```cmd
   Vectra.bat
   ```
   *`Vectra.bat` automatically isolates PATH DLL conflicts, creates/updates a local `.venv`, installs missing dependencies via `pyproject.toml`, and launches the Desktop App.*

3. **Manual Virtual Environment Setup**:
   ```bash
   python -m venv .venv
   # Windows:
   .venv\Scripts\activate
   # Linux/macOS:
   source .venv/bin/activate

   pip install -e .
   ```

4. **Start Desktop Application**:
   ```bash
   python -m kheramat.gui.app
   ```

---

## 📖 Language & Syntax Reference

Vectra provides intuitive scientific syntax matching matrix conventions:

### Matrix Operations & Linear Indexing
```matlab
% Matrix Literal Creation
A = [1, 2, 3; 4, 5, 6; 7, 8, 9];

% Range Vector Generation
t = 0:0.01:1;

% Fortran Column-Major 1-Based Indexing
val = A(2);      % Returns 4 (Column 1, Row 2)
sub = A(1:2, :); % Returns top two rows

% Element-wise Operations
B = A .* 2;
C = A .^ 2;
```

### Control Flow Constructs
```matlab
% Conditionals
x = 15;
if x > 20
    disp('High');
elseif x > 10
    disp('Medium');
else
    disp('Low');
end

% Loops with Break / Continue
acc = 0;
for i = 1:10
    if i == 5
        continue;
    end
    if i == 8
        break;
    end
    acc = acc + i;
end
```

### Custom Function Definitions
```matlab
function [out1, out2] = computeStats(data)
    out1 = mean(data);
    out2 = std(data);
end
```

---

## 🛠️ Toolbox Ecosystem

| Toolbox Module | Key Functions | Description |
| :--- | :--- | :--- |
| **Control Systems** | `tf(num, den)`, `step(sys)`, `impulse(sys)` | Transfer function modeling & dynamic step response analysis. |
| **DSP Toolbox** | `fft(x)`, `ifft(x)`, `freqz(b, a)`, `filter(b, a, x)` | Spectral analysis, digital filtering, and z-transform analysis. |
| **Communications** | `ammod`, `amdemod`, `fmmod`, `fmdemod` | Analog amplitude/frequency modulation and demodulation pipelines. |
| **State-Space** | `ss(A,B,C,D)`, `ctrb(A,B)`, `obsv(A,C)` | Linear time-invariant state space system analysis. |
| **Symbolic Math** | `syms`, `diff`, `integrate`, `solve` | Algebraic differentiation, integration, and symbolic solver engine. |

---

## 💻 Headless CLI & Automation

Vectra includes a standalone CLI interface for headless server script execution, continuous integration pipelines, and batch computing:

```bash
# Evaluate an inline expression
vectra-cli --eval "A = [1 2; 3 4]; B = A * 2; disp(B);"

# Run a script file headlessly
vectra-cli --run scripts/dsp_simulation.m
```

---

## 🧪 Testing & Verification

Vectra includes automated test suites covering AST parsing, array indexing, matrix arithmetic, toolbox solvers, and project management.

To run the complete test suite:
```bash
pytest tests/
```

```text
============================= test session starts =============================
collected 38 items

tests/test_cli.py ..                                                    [ 5%]
tests/test_diagnostics.py .                                             [ 7%]
tests/test_indexing.py .                                                [10%]
tests/test_interpreter.py ........                                      [31%]
tests/test_projects.py .                                               [34%]
tests/test_toolboxes.py ..................                             [81%]
tests/test_user_functions.py ......                                    [100%]

============================== 38 passed in 6.50s ==============================
```

---

## 🤝 Contributing & Development

Contributions are welcome! Please follow these guidelines:
1. **Fork the Repository**: Create your feature branch (`git checkout -b feature/AmazingFeature`).
2. **Ensure Clean Code & Tests**: Verify all existing tests pass (`pytest tests/`).
3. **Commit Your Changes**: (`git commit -m 'feat(toolbox): add bode plot generator'`).
4. **Push to Remote Branch**: (`git push origin feature/AmazingFeature`).
5. **Open a Pull Request**.

---

<div align="center">

**Vectra — Compute. Simulate. Innovate.**  
Licensed under the [MIT License](LICENSE).

</div>
