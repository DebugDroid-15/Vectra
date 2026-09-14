# Vectra Capability Matrix

| Category | Capability | Status | Implementation Backend | Test Coverage |
| :--- | :--- | :--- | :--- | :--- |
| **Language** | Control Flow (`if`, `for`, `while`, `try/catch`, `switch`) | FULL | Native AST Visitor | Passed (100%) |
| **Language** | 1-Based Column-Major Array Indexing | FULL | `KheraMATArray` / NumPy | Passed (100%) |
| **Math** | Linear Algebra (`inv`, `det`, `lu`, `qr`, `svd`, `eig`, `pinv`) | FULL | SciPy / NumPy | Passed (100%) |
| **Math** | Reductions (`sum`, `mean`, `min`, `max`, `std`, `var`) | FULL | Dimension-aware NumPy | Passed (100%) |
| **Math** | Polynomials (`poly`, `roots`, `polyval`, `polyfit`) | FULL | NumPy Polynomial | Passed (100%) |
| **Symbolic** | Algebra & Calculus (`diff`, `int`, `solve`, `simplify`) | FULL | SymPy Bridge | Passed (100%) |
| **DSP** | Transforms & Filtering (`fft`, `ifft`, `freqz`, `filter`, `bode`) | FULL | SciPy Signal | Passed (100%) |
| **Comms** | Modulation & Demodulation (`qammod`, `bpsk`, `awgn`, BER) | FULL | Native DSP Vector Engine | Passed (100%) |
| **Controls** | LTI Systems (`tf`, `ss`, `step`, `impulse`, `bode`, `pole`) | FULL | SciPy Signal / LTI | Passed (100%) |
| **Graphics** | 2D/3D Plotting (`surf`, `mesh`, `contour`, `subplot`, `legend`) | FULL | Matplotlib Engine | Passed (100%) |
| **GUI** | PySide6 Desktop Environment & Debugger | FULL | PySide6 | Passed (100%) |
