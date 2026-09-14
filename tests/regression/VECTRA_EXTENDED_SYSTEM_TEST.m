%% ================================================================
%                    VECTRA EXTENDED SYSTEM TEST
%              Compute. Simulate. Innovate.
%
%  Single-file MATLAB compatibility / numerical / runtime test
%% ================================================================

clc;
clear;

fprintf('\n');
fprintf('============================================================\n');
fprintf('              VECTRA EXTENDED SYSTEM TEST\n');
fprintf('============================================================\n');

tol = 1e-8;

%% ================================================================
% 1. BASIC LANGUAGE & ASSIGNMENT
%% ================================================================
fprintf('\n[1] BASIC LANGUAGE & ASSIGNMENT\n');
a = 10;
b = 25;
c = a + b;
assert(c == 35, 'Basic arithmetic failed');

x = 5; x = x + 10; x = x * 2; x = x / 5;
assert(abs(x - 6) < tol, 'Sequential assignment failed');

%% ================================================================
% 2. ARRAYS & INDEXING
%% ================================================================
fprintf('[2] ARRAYS & INDEXING\n');
row = [1 2 3 4 5];
col = [1; 2; 3; 4; 5];
A = [1 2 3; 4 5 6; 7 8 9];
assert(A(1,1) == 1, 'Matrix indexing A(1,1) failed');
assert(A(2,3) == 6, 'Matrix indexing A(2,3) failed');
assert(A(3,3) == 9, 'Matrix indexing A(3,3) failed');

% Linear indexing
assert(A(2) == 4, 'Linear indexing A(2) failed');
assert(A(4) == 2, 'Linear indexing A(4) failed');

% Matrix slicing
assert(sum(A(2, :)) == 15, 'Row slicing failed');
assert(sum(A(:, 3)) == 18, 'Col slicing failed');
sub = A(1:2, 2:3);
assert(sub(2,2) == 6, 'Submatrix failed');

%% ================================================================
% 3. COLON OPERATOR & EDGE CASES
%% ================================================================
fprintf('[3] COLON OPERATOR & EDGE CASES\n');
v1 = 1:10;
assert(length(v1) == 10 && v1(10) == 10, 'Basic colon failed');
v2 = 1:2:10;
assert(length(v2) == 5 && v2(5) == 9, 'Step colon failed');
v3 = 10:-1:1;
assert(v3(2) == 9, 'Negative step colon failed');
v4 = 1:-1:10;
assert(length(v4) == 0, 'Empty colon failed');

%% ================================================================
% 4. ELEMENT-WISE OPERATIONS
%% ================================================================
fprintf('[4] ELEMENT-WISE OPERATIONS\n');
x = [1 2 3 4];
y = [5 6 7 8];
assert(sum(abs((x + y) - [6 8 10 12])) < tol, 'Element add failed');
assert(sum(abs((x .* y) - [5 12 21 32])) < tol, 'Element mul failed');
assert(sum(abs((x .^ 2) - [1 4 9 16])) < tol, 'Element pow failed');

%% ================================================================
% 5. MATRIX OPERATIONS & DECOMPOSITIONS
%% ================================================================
fprintf('[5] MATRIX OPERATIONS & DECOMPOSITIONS\n');
A = [1 2; 3 4];
B = [5 6; 7 8];
C = A * B;
assert(C(1,1) == 19 && C(2,2) == 50, 'Matrix mul failed');

A = [1 2 3; 0 1 4; 5 6 0];
Ai = inv(A);
assert(sum(sum(abs(A * Ai - eye(3)))) < tol, 'Matrix inverse failed');

d = det(A);
assert(abs(d - 1) < tol, 'Determinant failed');
assert(rank(A) == 3, 'Rank failed');
assert(trace(A) == 2, 'Trace failed');

[U, S, V] = svd(A);
assert(sum(sum(abs(U * S * V' - A))) < tol, 'SVD reconstruction failed');

[L, U_lu, P] = lu(A);
assert(sum(sum(abs(P * A - L * U_lu))) < tol, 'LU reconstruction failed');

[Q, R] = qr(A);
assert(sum(sum(abs(Q * R - A))) < tol, 'QR reconstruction failed');

[V_eig, D_eig] = eig(A);
assert(sum(sum(abs(A * V_eig - V_eig * D_eig))) < tol, 'Eig reconstruction failed');
e_vals = eig(A);
assert(abs(sum(e_vals) - trace(A)) < tol, 'Eig sum vs trace failed');

%% ================================================================
% 6. STATISTICS & SCALAR REDUCTIONS
%% ================================================================
fprintf('[6] STATISTICS & REDUCTIONS\n');
data = [1 2 3 4 5 6 7 8 9 10];
[m_val, m_idx] = max(data);
assert(m_val == 10 && m_idx == 10, 'Max with multiple outputs failed');
assert(min(data) == 1, 'Min single output failed');
assert(sum(data) == 55, 'Sum failed');
assert(mean(data) == 5.5, 'Mean failed');
assert(median(data) == 5.5, 'Median failed');
assert(abs(std(data) - 3.027650) < 1e-5, 'Std failed');
assert(abs(var(data) - 9.166666) < 1e-5, 'Var failed');

% Matrix reduction tests
M = [1 2 3; 4 5 6];
assert(sum(sum(abs(max(M) - [4 5 6]))) < tol, 'Matrix max failed');
assert(sum(sum(abs(sum(M) - [5 7 9]))) < tol, 'Matrix sum failed');

%% ================================================================
% 7. MATHEMATICAL FUNCTIONS & COMPLEX ARITHMETIC
%% ================================================================
fprintf('[7] MATH & COMPLEX ARITHMETIC\n');
assert(abs(sin(pi/2) - 1) < tol, 'Sin failed');
assert(abs(log(exp(3)) - 3) < tol, 'Log/exp failed');
assert(floor(3.8) == 3 && ceil(3.2) == 4, 'Floor/ceil failed');

z = 3 + 4i;
assert(real(z) == 3 && imag(z) == 4, 'Complex real/imag failed');
assert(abs(z) == 5, 'Complex abs failed');
assert(conj(z) == 3 - 4i, 'Complex conj failed');

%% ================================================================
% 8. LOGICAL OPERATORS & INDEXING
%% ================================================================
fprintf('[8] LOGICALS\n');
a = 5; b = 10;
assert(a < b, 'Logical < failed');
assert(~(a == b), 'Logical == failed');
assert(a ~= b, 'Logical ~= failed');

mask = data > 5;
sel = data(mask);
assert(sum(sel) == 40, 'Logical indexing sum failed');
assert(length(sel) == 5, 'Logical indexing length failed');

%% ================================================================
% 9. POLYNOMIALS & CALCULUS
%% ================================================================
fprintf('[9] POLYNOMIALS & CALCULUS\n');
p = [1 -6 11 -6];
r = roots(p);
assert(sum(abs(sort(r) - [1; 2; 3])) < tol, 'Roots failed');

v = polyval(p, 4);
assert(abs(v - 6) < tol, 'Polyval failed');

x_int = 0:0.01:pi;
y_int = sin(x_int);
assert(abs(trapz(x_int, y_int) - 2) < 1e-3, 'Trapz failed');

y_diff = x_int.^2;
dy = diff(y_diff);
assert(abs(dy(1) - 1e-4) < tol, 'Diff failed');

%% ================================================================
% 10. DSP & FFT
%% ================================================================
fprintf('[10] DSP & FFT\n');
fs = 1000;
t = 0:1/fs:1-1/fs;
sig = sin(2*pi*50*t);
S = fft(sig);
sig_rec = ifft(S);
fft_err = max(abs(sig - sig_rec));
assert(fft_err < tol, 'FFT/IFFT round trip failed');

[max_val, max_idx] = max(abs(S(1:length(S)/2)));
f_detected = (max_idx - 1) * fs / length(S);
assert(abs(f_detected - 50) < tol, 'FFT peak frequency failed');

cv = conv([1 1], [1 2 1]);
assert(sum(abs(cv - [1 3 3 1])) < tol, 'Convolution failed');

[b, a] = butter(2, 0.5);
[H, w] = freqz(b, a, 1024, fs);
assert(abs(abs(H(1)) - 1) < 1e-2, 'Butterworth passband DC failed');
assert(abs(abs(H(length(H))) - 0) < 1e-2, 'Butterworth stopband Nyquist failed');

%% ================================================================
% 11. COMMUNICATIONS
%% ================================================================
fprintf('[11] COMMUNICATIONS\n');
fc = 100; fm = 10;
msg = sin(2*pi*fm*t);
am_sig = ammod(msg, fc, fs);
am_rec = amdemod(am_sig, fc, fs);
am_err = sqrt(mean((msg - am_rec).^2));
assert(am_err < 0.05, 'AM demodulation failed');

bits = [1 0 1 1 0 0 1 0];
b_mod = bpskmod(bits);
b_rec = bpskdemod(b_mod);
assert(sum(abs(b_rec - bits)) == 0, 'BPSK bit error failed');

q_mod = qpskmod(bits);
q_rec = qpskdemod(q_mod);
assert(sum(abs(q_rec - bits)) == 0, 'QPSK bit error failed');

qam_data = [0 1 2 3 3 2 1 0];
qam_m = qammod(qam_data, 4);
qam_r = qamdemod(qam_m, 4);
assert(sum(abs(qam_r - qam_data)) == 0, 'QAM symbol error failed');

%% ================================================================
% 12. CONTROL SYSTEMS
%% ================================================================
fprintf('[12] CONTROL SYSTEMS\n');
sys = tf([1], [1 3 2]);
p_sys = pole(sys);
assert(sum(abs(sort(p_sys) - [-2; -1])) < tol, 'Poles failed');

[y_s, t_s] = step(sys);
assert(abs(y_s(length(y_s)) - 0.5) < 0.05, 'Step response steady state failed');

[mag, phase, w_bode] = bode(sys);
assert(abs(mag(1) - (-6.0206)) < 1e-2, 'Bode magnitude at DC failed');

%% ================================================================
% 13. CROSS-SUBSYSTEM VALIDATION
%% ================================================================
fprintf('[13] CROSS-SUBSYSTEM\n');
% Signal -> Filter -> FFT -> Spectrum
sig_noisy = sin(2*pi*10*t) + sin(2*pi*200*t);
[b_low, a_low] = butter(4, 50/(fs/2));
sig_filt = filter(b_low, a_low, sig_noisy);
F_filt = abs(fft(sig_filt));
[~, max_f_idx] = max(F_filt(1:length(F_filt)/2));
f_peak = (max_f_idx - 1) * fs / length(F_filt);
assert(abs(f_peak - 10) < tol, 'Cross-subsystem Filter->FFT failed');

%% ================================================================
% 14. SYMBOLIC MATHEMATICS
%% ================================================================
fprintf('[14] SYMBOLIC\n');
syms x;
expr = (x^2 - 1)/(x - 1);
expr_simp = simplify(expr);
assert(strcmp(char(expr_simp), 'x + 1'), 'Symbolic simplify failed');

df = diff(x^3, x);
assert(strcmp(char(df), '3*x^2'), 'Symbolic diff failed');

sol = solve(x^2 - 9 == 0, x);
assert(abs(sol(1) - (-3)) < tol, 'Symbolic solve failed');
assert(abs(sol(2) - 3) < tol, 'Symbolic solve failed');

%% ================================================================
% 15. USER FUNCTIONS
%% ================================================================
fprintf('[15] USER FUNCTIONS\n');
[s_res, p_res] = my_sub(5, 6);
assert(s_res == 11, 'Subroutine add failed');
assert(p_res == 30, 'Subroutine mul failed');

fprintf('\n============================================================\n');
fprintf('VECTRA EXTENDED TEST: ALL CHECKS PASSED\n');
fprintf('============================================================\n');

function [s, p] = my_sub(a, b)
    s = a + b;
    p = a * b;
end
