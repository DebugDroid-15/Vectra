# Vectra — Scientific Computing & Engineering Desktop Environment

<p align="center">
  <img src="Vectra.png" alt="Vectra Logo" width="220"/>
</p>

<h3 align="center">Free, Extensible, Open-Source Desktop Scientific Computing Platform & MATLAB Alternative</h3>

<p align="center">
  Tailored for Electronics & Communication Engineering (ECE) Coursework, Lab Research, Signal Analysis, and Control Systems.
</p>

---

## 📖 Overview

**Vectra** is a free, lightweight, open-source scientific computing desktop application and MATLAB-compatible environment built completely using Python's scientific ecosystem (`NumPy`, `SciPy`, `SymPy`, `Matplotlib`, and `PySide6`).

It provides students, researchers, and engineers with an intuitive environment that preserves standard MATLAB syntax—including 1-based indexing, matrix constructors, range operators (`start:step:stop`), plot formatting, and ECE curriculum toolboxes—without requiring expensive commercial licenses.

---

## ✨ Key Features & Highlights

### 🖥️ 1. Modern Multi-Dock PySide6 IDE
- **Script Editor**: Multi-tab code editor featuring syntax highlighting, line numbers, active line indicators, theme auto-matching, and file management.
- **Command Window REPL**: Command prompt (`>>`) with command history (`Up`/`Down` arrows), MATLAB-style documentation lookup (`help <command>`), web browser doc launcher (`doc <command>`), and `clc`/`clear` support.
- **Workspace Inspector**: Live variables table displaying real-time variable names, array shapes (e.g. `1x100 double`), types, and formatted values.
- **Current Folder Explorer**: Integrated file tree view allowing you to browse your workspace and double-click `.m` scripts to open them directly in the editor.
- **Interactive Figure Window**: Embedded Matplotlib toolbar supporting pan, zoom, tight layout resizing, interactive `gtext` click placement, and multi-format plot saving (PNG, SVG, PDF).
- **Theme Switcher**: Instant toggle between Dark Theme and Light Theme directly from the top main toolbar.
- **System Logs & Crash Inspector**: Built-in dialog to inspect live application logs and crash tracebacks in real-time.

---

### 🧮 2. Comprehensive Mathematical & ECE Toolboxes

Vectra includes out-of-the-box support for over 150+ universal matrix functions and domain-specific engineering commands:

#### 📐 Core Linear Algebra & Matrix Calculus
- **Matrix Operations**: `inv`, `det`, `rank`, `trace`, `eig`, `svd`, `lu`, `qr`, `chol`, `cond`, `null`, `orth`, `pinv`.
- **Matrix Exponentials & Functions**: `expm`, `logm`, `sqrtm`, `polyval`, `polyfit`, `cumsum`, `cumprod`, `prod`, `sum`, `mean`, `std`, `var`, `min`, `max`, `median`.
- **Matrix Rearrangement**: `reshape`, `repmat`, `rot90`, `flip`, `fliplr`, `flipud`, `squeeze`, `diag`, `tril`, `triu`, `eye`, `zeros`, `ones`, `rand`, `randn`.
- **Numerical Calculus & Root Finding**: `trapz`, `diff`, `fzero`, `cumsum`, `cross`, `dot`.

#### 📶 Signals & Systems (SS)
- **Elementary Signals**: `heaviside`, `unitstep`, `dirac`, `unitimpulse`, `sinc`, `square`, `sawtooth`, `chirp`, `rectpuls`, `tripuls`.
- **Signal Analysis**: `conv`, `deconv`, `conv2`, `xcorr`, `fft`, `ifft`, `fftshift`, `ifftshift`, `abs`, `angle`, `unwrap`, `phase`.

#### 📻 Communication Systems
- **Analog Modulation**: `ammod`, `amdemod`, `fmmod`, `fmdemod`, `pmmod`, `pmdemod`.
- **Digital Modulation**: `bpskmod`, `bpskdemod`, `qpskmod`, `qpskdemod`, `pammod`, `qammod`.
- **Noise & Channels**: `awgn` (Additive White Gaussian Noise channel simulation).

#### 🎛️ Digital Signal Processing (DSP)
- **Filter Design**: `butter`, `cheby1`, `cheby2`, `ellip`, `bessel` (Lowpass, Highpass, Bandpass, Bandstop).
- **Filter Analysis**: `freqz`, `zplane`, `impz`.
- **Multi-rate Signal Processing**: `resample`, `decimate`, `interp`.

#### 🧲 Principles of Electromagnetics (PEM)
- **3D Grid Generation**: `meshgrid`, `griddata`.
- **3D Visualization**: `surf`, `surfc`, `mesh`, `meshc`, `plot3`, `contour`, `contourf`.
- **Vector Fields**: `quiver`, `quiver3`, `gradient`, `divergence`, `curl`.

#### ⚙️ Control Systems & Transfer Functions
- **System Representations**: `tf(num, den)`, `ss(A, B, C, D)`.
- **Time Response**: `step`, `impulse`, `initial`, `ramp`.
- **Frequency Response**: `bode`, `nyquist`, `rlocus`, `margin`, `pole`, `zero`.

#### 🔣 Symbolic Mathematics
- **Symbolic Variables & Expressions**: `syms x y z`, symbolic expression operator overloading.
- **Symbolic Calculus**: `diff(f, x)`, `int(f, x)`, `limit(f, x, a)`, `solve(eqn, x)`, `dsolve`.

---

## ⚡ Quick Start (Windows Users)

1. **Clone or Download**:
   ```bash
   git clone https://github.com/DebugDroid-15/Vectra.git
   cd Vectra
   ```
2. **Launch via 1-Click Batch File**:
   Double-click `Vectra.bat` in the root folder!

   > `Vectra.bat` automatically checks for Python 3.10+, creates/configures dependencies, and opens the desktop environment immediately.

For comprehensive execution instructions across platforms, read [HOW_TO_RUN.md](HOW_TO_RUN.md).

---

## 🖥️ Graphical User Interface Overview

```
+-----------------------------------------------------------------------------------+
|  Vectra Desktop — Scientific Computing Environment                                |
+-----------------------------------------------------------------------------------+
| [▶ Run Script] [📄 New] [💾 Save] [🧹 Clear] [☀️ Theme] [📋 Logs & Crashes]       |
+---------------------+---------------------------------------+---------------------+
| Current Folder      | Script Editor (Untitled.m)            | Figure Window       |
| 📁 src/             | 1  clc; clear;                       | 📈 Matplotlib Plot  |
| 📁 tests/           | 2  t = 0:0.01:1;                      | [Toolbar: Pan/Zoom] |
| 📄 main.m           | 3  x = sin(2*pi*5*t);                 +---------------------+
| 📄 signal.m         | 4  plot(t, x); grid on;               | Workspace Inspector |
|                     |                                       | Name | Size | Value |
|                     |                                       | t    | 1x101| double|
|                     |                                       | x    | 1x101| double|
+---------------------+---------------------------------------+---------------------+
| Command Window (REPL Prompt)                                                      |
| >> x = 1:5                                                                        |
| x =                                                                               |
|      1     2     3     4     5                                                    |
| >>                                                                                |
+-----------------------------------------------------------------------------------+
```

---

## 📜 Example Script: ECE Communications Simulation

Create a script in the Vectra Script Editor and click **▶ Run Script**:

```matlab
% AM Modulation & Demodulation Simulation
clc; clear; close all;

% Time Vector
t = 0:0.001:0.1;

% Carrier & Message Frequencies
fm = 20;   % Message frequency (20 Hz)
fc = 200;  % Carrier frequency (200 Hz)

% Message Signal
m = sin(2*pi*fm*t);

% AM Modulated Signal
s = ammod(m, fc, 1000);

% Plot Results
figure;
subplot(2,1,1);
plot(t, m);
title('Message Signal m(t)');
xlabel('Time (s)'); ylabel('Amplitude');
grid on;

subplot(2,1,2);
plot(t, s);
title('AM Modulated Signal s(t)');
xlabel('Time (s)'); ylabel('Amplitude');
grid on;
```

---

## 🛠️ Developer Setup & Running Tests

To run Vectra in editable mode and execute automated pytest suites:

```bash
# Install package in editable mode
pip install -e .

# Run pytest test suite (27 tests)
pytest tests/

# Launch GUI directly from Python module
python -m kheramat.gui.app
```

---

## 📄 License & Open Source Stack

Vectra is open-source software released under the [MIT License](LICENSE).

Built with pride using Python scientific libraries:
- [PySide6 / Qt](https://www.qt.io/) — Desktop User Interface
- [NumPy](https://numpy.org/) — High-Performance Array Engine
- [SciPy](https://scipy.org/) — Scientific & Signal Processing Algorithms
- [SymPy](https://www.sympy.org/) — Symbolic Mathematics
- [Matplotlib](https://matplotlib.org/) — 2D & 3D Plotting Canvas
