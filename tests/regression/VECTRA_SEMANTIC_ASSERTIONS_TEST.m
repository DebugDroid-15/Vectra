%% VECTRA SEMANTIC ASSERTION REGRESSION SUITE
clc; clear;

fprintf('\n========================================================\n');
fprintf('    VECTRA COMPREHENSIVE SEMANTIC ASSERTION SUITE\n');
fprintf('========================================================\n');

%% Linear Algebra
A = [1 2 3; 4 5 6; 7 8 10];
B = [1 0 0; 0 1 0; 0 0 1];
AB = A * B;
assert(sum(sum(abs(AB - A))) < 1e-10, 'Matrix Multiplication failed');

Ai = inv(A);
assert(sum(sum(abs(A*Ai - eye(3)))) < 1e-10, 'Matrix Inverse failed');
assert(abs(det(A) - (-3)) < 1e-10, 'Determinant failed');
assert(rank(A) == 3, 'Rank failed');
assert(trace(A) == 16, 'Trace failed');

[V, D] = eig(A); e = diag(D);
assert(abs(sum(e) - trace(A)) < 1e-10, 'Eigenvalues trace sum failed');
assert(abs(prod(e) - det(A)) < 1e-10, 'Eigenvalues determinant prod failed');

[U, S, V] = svd(A);
assert(sum(sum(abs(U*S*V' - A))) < 1e-10, 'SVD reconstruction failed');

%% Polynomials & Calculus
p = [1 -6 11 -6];
r = roots(p);
assert(sum(abs(sort(r) - [1; 2; 3])) < 1e-6, 'Polynomial roots failed');

v = polyval(p, 1:5);
assert(sum(abs(v - [0 0 0 6 24])) < 1e-6, 'Polynomial evaluation failed');

x = 0:0.01:1;
y = x.^3;
dy = diff(y);
assert(abs(dy(1) - 1e-6) < 1e-10, 'Numerical diff failed on dy(1)');
assert(abs(dy(2) - 7e-6) < 1e-10, 'Numerical diff failed on dy(2)');

integral_val = trapz(x, y);
assert(abs(integral_val - 0.25) < 1e-3, 'Numerical integration failed');

%% DSP
sig = [1 2 3 4 5 6 7 8];
F = fft(sig);
sig_rec = ifft(F);
assert(sum(abs(sig - sig_rec)) < 1e-10, 'FFT/IFFT round trip failed');

fs = 1000;
t = 0:1/fs:1-1/fs;
f_target = 50;
sig_f = sin(2*pi*f_target*t);
F_sig = abs(fft(sig_f));
[~, idx] = max(F_sig(1:length(F_sig)/2));
f_detected = (idx-1)*fs/length(F_sig);
assert(abs(f_detected - f_target) < 1e-6, 'FFT frequency detection failed');

c = conv([1 1], [1 2 1]);
assert(sum(abs(c - [1 3 3 1])) < 1e-10, 'Convolution failed');

[b_filt, a_filt] = butter(2, 0.5);
assert(length(b_filt) == 3, 'Filter coefficients numerator failed');
assert(length(a_filt) == 3, 'Filter coefficients denominator failed');
[h, w] = freqz(b_filt, a_filt);
assert(abs(abs(h(1)) - 1) < 1e-4, 'Filter DC response failed');

%% Communications
fc = 500; fm = 20; fs = 2000;
t_am = 0:1/fs:1-1/fs;
msg_am = sin(2*pi*fm*t_am);
am_mod = ammod(msg_am, fc, fs);
am_dem = amdemod(am_mod, fc, fs);
err_am = sqrt(mean((msg_am - am_dem).^2));
assert(err_am < 0.05, 'AM Modulation/Demodulation failed');

bits = [0 1 1 0 1 0 1 1];
bpsk_m = bpskmod(bits);
assert(sum(abs(bpskdemod(bpsk_m) - bits)) == 0, 'BPSK failed');

qpsk_m = qpskmod(bits);
assert(sum(abs(qpskdemod(qpsk_m) - bits)) == 0, 'QPSK failed');

qam_data = [0 1 2 3 0 2 1 3];
qam_m = qammod(qam_data, 4);
assert(sum(abs(qamdemod(qam_m, 4) - qam_data)) == 0, 'QAM failed');

%% Control Systems
sys = tf([1], [1 3 2]);
p_sys = pole(sys);
assert(sum(abs(sort(p_sys) - [-2; -1])) < 1e-6, 'Control poles failed');

[y_step, t_step] = step(sys);
assert(abs(y_step(length(y_step)) - 0.5) < 0.05, 'Control step response steady state failed');

%% Symbolic
syms x y_sym z;
f_sym = x^2 - 1;
df = diff(f_sym, x);
assert(strcmp(char(df), '2*x'), 'Symbolic diff failed');

int_f = int(df, x);
% Integration constant means it could just be x^2
assert(strcmp(char(int_f), 'x^2'), 'Symbolic int failed');

sol = solve(x^2 - 4 == 0, x);
assert(abs(sol(1) - (-2)) < 1e-6, 'Symbolic solve 1 failed');
assert(abs(sol(2) - 2) < 1e-6, 'Symbolic solve 2 failed');

expr_simp = (x^2 - 1)/(x - 1);
assert(strcmp(char(simplify(expr_simp)), 'x + 1'), 'Symbolic simplify failed');

fprintf('\nALL SEMANTIC REGRESSION ASSERTIONS PASSED (100%%)\n');
