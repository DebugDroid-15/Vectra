import webbrowser
from typing import Dict, Any

HELP_DATABASE: Dict[str, Dict[str, str]] = {
    "plot": {
        "syntax": "plot(X, Y) or plot(Y) or plot(X, Y, LineSpec)",
        "summary": "2D line plot",
        "description": "plot(X,Y) creates a 2D line plot of the data in Y versus the corresponding values in X.\nSupported specifiers: 'LineWidth', 'Color', 'LineStyle', 'Marker'.",
        "url": "https://www.mathworks.com/help/matlab/ref/plot.html"
    },
    "subplot": {
        "syntax": "subplot(m, n, p)",
        "summary": "Create axes in tiled positions",
        "description": "subplot(m,n,p) divides the current figure into an m-by-n grid and creates axes in the position specified by p.",
        "url": "https://www.mathworks.com/help/matlab/ref/subplot.html"
    },
    "stem": {
        "syntax": "stem(Y) or stem(X, Y)",
        "summary": "Plot discrete sequence data",
        "description": "stem(Y) plots the discrete sequence data Y as stems extending from a baseline along the x-axis.",
        "url": "https://www.mathworks.com/help/matlab/ref/stem.html"
    },
    "heaviside": {
        "syntax": "y = heaviside(t)",
        "summary": "Step function (Continuous Time Unit Step)",
        "description": "heaviside(t) evaluates the unit step function at time t. Returns 1 for t >= 0 and 0 for t < 0.",
        "url": "https://www.mathworks.com/help/symbolic/heaviside.html"
    },
    "unitstep": {
        "syntax": "y = unitstep(t)",
        "summary": "Unit step signal function",
        "description": "unitstep(t) generates a continuous unit step signal.",
        "url": "https://www.mathworks.com/help/symbolic/heaviside.html"
    },
    "dirac": {
        "syntax": "y = dirac(t)",
        "summary": "Dirac delta function",
        "description": "dirac(t) represents the Dirac delta distribution.",
        "url": "https://www.mathworks.com/help/symbolic/dirac.html"
    },
    "unitimpulse": {
        "syntax": "y = unitimpulse(n)",
        "summary": "Discrete unit impulse signal",
        "description": "unitimpulse(n) generates a discrete-time unit impulse signal delta[n].",
        "url": "https://www.mathworks.com/help/symbolic/dirac.html"
    },
    "conv": {
        "syntax": "C = conv(A, B)",
        "summary": "Convolution and polynomial multiplication",
        "description": "conv(A,B) returns the convolution of vectors A and B.",
        "url": "https://www.mathworks.com/help/matlab/ref/conv.html"
    },
    "fft": {
        "syntax": "Y = fft(X)",
        "summary": "Fast Fourier Transform",
        "description": "fft(X) computes the Discrete Fourier Transform (DFT) of vector X using a fast Fourier transform algorithm.",
        "url": "https://www.mathworks.com/help/matlab/ref/fft.html"
    },
    "butter": {
        "syntax": "[b, a] = butter(n, Wn) or [b, a] = butter(n, Wn, ftype)",
        "summary": "Butterworth digital and analog filter design",
        "description": "butter(n, Wn) designs an nth-order lowpass digital Butterworth filter with normalized cutoff frequency Wn.",
        "url": "https://www.mathworks.com/help/signal/ref/butter.html"
    },
    "zplane": {
        "syntax": "zplane(b, a)",
        "summary": "Zero-pole plot for discrete-time systems",
        "description": "zplane(b,a) plots the poles and zeros of the transfer function defined by numerator coefficients b and denominator coefficients a.",
        "url": "https://www.mathworks.com/help/signal/ref/zplane.html"
    },
    "ammod": {
        "syntax": "y = ammod(x, Fc, Fs)",
        "summary": "Amplitude modulation",
        "description": "ammod(x, Fc, Fs) uses the message signal x to modulate a carrier signal with frequency Fc (Hz) at sample rate Fs (Hz).",
        "url": "https://www.mathworks.com/help/comms/ref/ammod.html"
    },
    "fmmod": {
        "syntax": "y = fmmod(x, Fc, Fs, freqdev)",
        "summary": "Frequency modulation",
        "description": "fmmod(x, Fc, Fs, freqdev) uses the message signal x to frequency modulate a carrier with frequency Fc at sample rate Fs.",
        "url": "https://www.mathworks.com/help/comms/ref/fmmod.html"
    },
    "awgn": {
        "syntax": "y = awgn(x, snr)",
        "summary": "Add additive white Gaussian noise to signal",
        "description": "awgn(x, snr) adds additive white Gaussian noise to vector x with signal-to-noise ratio snr in dB.",
        "url": "https://www.mathworks.com/help/comms/ref/awgn.html"
    },
    "tf": {
        "syntax": "sys = tf(num, den)",
        "summary": "Transfer function model",
        "description": "sys = tf(num, den) creates a continuous-time transfer function model with numerator num and denominator den.",
        "url": "https://www.mathworks.com/help/control/ref/tf.html"
    },
    "bode": {
        "syntax": "bode(sys)",
        "summary": "Bode plot of frequency response",
        "description": "bode(sys) creates a Bode plot of the frequency response of dynamic system model sys.",
        "url": "https://www.mathworks.com/help/control/ref/bode.html"
    },
    "syms": {
        "syntax": "syms x y z",
        "summary": "Shortcut for creating symbolic variables",
        "description": "syms creates symbolic variables in the workspace for symbolic calculus.",
        "url": "https://www.mathworks.com/help/symbolic/syms.html"
    },
    "linewidth": {
        "syntax": "plot(X, Y, 'LineWidth', width)",
        "summary": "Line width property for 2D/3D plot lines",
        "description": "LineWidth specifies the width of plot lines in points (default: 1.0). Example: plot(x, y, 'LineWidth', 2.5).",
        "url": "https://www.mathworks.com/help/matlab/creating_plots/line-properties.html"
    },
    "color": {
        "syntax": "plot(X, Y, 'Color', color_spec)",
        "summary": "Line/Marker color property",
        "description": "Color specifies the color of lines or markers. Supported colors: 'r' (red), 'g' (green), 'b' (blue), 'c' (cyan), 'm' (magenta), 'y' (yellow), 'k' (black), 'w' (white).",
        "url": "https://www.mathworks.com/help/matlab/creating_plots/specify-line-colors.html"
    },
    "linestyle": {
        "syntax": "plot(X, Y, 'LineStyle', style_spec)",
        "summary": "Line style property",
        "description": "LineStyle specifies line appearance: '-' (solid), '--' (dashed), ':' (dotted), '-.' (dash-dot), 'none' (no line).",
        "url": "https://www.mathworks.com/help/matlab/ref/plot.html"
    },
    "marker": {
        "syntax": "plot(X, Y, 'Marker', marker_spec)",
        "summary": "Marker symbol property",
        "description": "Marker specifies symbols at data points: 'o' (circle), '+' (plus), '*' (star), '.' (point), 'x' (cross), 's' (square), 'd' (diamond), '^' (up triangle), 'v' (down triangle).",
        "url": "https://www.mathworks.com/help/matlab/creating_plots/specify-line-colors.html"
    },
    "logspace": {
        "syntax": "y = logspace(a, b, n)",
        "summary": "Logarithmically spaced vector",
        "description": "logspace(a, b, n) generates n logarithmically spaced points between 10^a and 10^b.",
        "url": "https://www.mathworks.com/help/matlab/ref/logspace.html"
    },
    "diag": {
        "syntax": "D = diag(v, k)",
        "summary": "Diagonal matrices and diagonals of a matrix",
        "description": "diag(v) creates a diagonal matrix with vector v on the main diagonal.",
        "url": "https://www.mathworks.com/help/matlab/ref/diag.html"
    },
    "cross": {
        "syntax": "C = cross(A, B)",
        "summary": "Vector cross product",
        "description": "cross(A, B) returns the cross product of 3D vectors A and B.",
        "url": "https://www.mathworks.com/help/matlab/ref/cross.html"
    },
    "dot": {
        "syntax": "C = dot(A, B)",
        "summary": "Vector dot product",
        "description": "dot(A, B) returns the scalar dot product of vectors A and B.",
        "url": "https://www.mathworks.com/help/matlab/ref/dot.html"
    },
    "reshape": {
        "syntax": "B = reshape(A, m, n)",
        "summary": "Reshape array",
        "description": "reshape(A, m, n) returns an m-by-n matrix whose elements are taken column-wise from A.",
        "url": "https://www.mathworks.com/help/matlab/ref/reshape.html"
    },
    "repmat": {
        "syntax": "B = repmat(A, m, n)",
        "summary": "Replicate and tile an array",
        "description": "repmat(A, m, n) creates a large matrix consisting of an m-by-n tiling of copies of A.",
        "url": "https://www.mathworks.com/help/matlab/ref/repmat.html"
    },
    "sort": {
        "syntax": "B = sort(A)",
        "summary": "Sort array elements",
        "description": "sort(A) sorts the elements of array A in ascending order along columns.",
        "url": "https://www.mathworks.com/help/matlab/ref/sort.html"
    },
    "sub2ind": {
        "syntax": "ind = sub2ind(siz, row, col)",
        "summary": "Convert subscripts to linear index",
        "description": "sub2ind(siz, row, col) determines equivalent linear index from row and column subscripts for a matrix of size siz.",
        "url": "https://www.mathworks.com/help/matlab/ref/sub2ind.html"
    },
    "ind2sub": {
        "syntax": "[row, col] = ind2sub(siz, ind)",
        "summary": "Convert linear index to subscripts",
        "description": "ind2sub(siz, ind) determines equivalent row and column subscripts corresponding to linear index ind for matrix of size siz.",
        "url": "https://www.mathworks.com/help/matlab/ref/ind2sub.html"
    },
    "find": {
        "syntax": "ind = find(X)",
        "summary": "Find indices of non-zero elements",
        "description": "find(X) returns a vector containing the linear indices of each non-zero element in array X.",
        "url": "https://www.mathworks.com/help/matlab/ref/find.html"
    },
    "gtext": {
        "syntax": "gtext('string')",
        "summary": "Place text in figure using mouse click",
        "description": "gtext('string') waits for a mouse click on the current figure and places the text string at clicked coordinates.",
        "url": "https://www.mathworks.com/help/matlab/ref/gtext.html"
    }
}

def get_help_text(topic: str) -> str:
    t = topic.strip().lower()
    if t in HELP_DATABASE:
        info = HELP_DATABASE[t]
        res = (
            f"\n--- MATLAB / Vectra Help: {t.upper()} ---\n"
            f"Syntax:      {info['syntax']}\n"
            f"Summary:     {info['summary']}\n"
            f"Description: {info['description']}\n"
            f"Online Docs: {info['url']}\n"
        )
        return res
    else:
        return f"\nNo documentation found for topic '{topic}'. Search online docs at: https://www.mathworks.com/help/search.html?qdoc={topic}\n"

def open_doc_url(topic: str) -> str:
    t = topic.strip().lower()
    if t in HELP_DATABASE:
        url = HELP_DATABASE[t]['url']
    else:
        url = f"https://www.mathworks.com/help/search.html?qdoc={topic}"
    webbrowser.open(url)
    return f"\nOpening documentation for '{topic}' in your web browser: {url}\n"

