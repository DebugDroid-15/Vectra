% VECTRA COMPLETE ULTIMATE REGRESSION & ACCEPTANCE WORKLOAD
clc;
clear;

% 1. Formatted I/O Printing & String Generation
fprintf('=== VECTRA ULTIMATE ACCEPTANCE TEST SUITE ===\n');
fprintf('Testing Formatted Output: int=%d, float=%.4f\n', 42, 3.14159);
s_str = sprintf('Value = %.2f', 99.99);

% 2. Variables and Range Vectors
fs = 2000;
T = 1;
t = 0:1/fs:T;

% 3. Complex Signal Processing & FFT
x = sin(2*pi*50*t) + 0.5*sin(2*pi*150*t);
noise = 0.1*randn(size(t));
x_noisy = x + noise;
X = fft(x_noisy);

% 4. Matrix Arithmetic & 1-Based Column-Major Indexing
A = [1 2; 3 4];
linear_val = A(2); % Must equal 3

% 5. Linear Algebra & Decompositions
[U, S, V] = svd(A);
det_val = det(A);
inv_A = inv(A);

% 6. Digital Filtering (Butterworth)
[b, a] = butter(4, 200/(fs/2));
filtered = filter(b, a, x_noisy);

% 7. Modulation & Demodulation Pipeline
message = sin(2*pi*10*t);
s_am = ammod(message, 100, fs);
rec_am = amdemod(s_am, 100, fs);

% 8. Control Systems Modeling
num = [1];
den = [1 3 2];
sys = tf(num, den);
[step_y, step_t] = step(sys);

% 9. Symbolic Mathematics with Safe Type Conversion
syms z;
sym_expr = z^2 + 3*z + 2;
d_expr = diff(sym_expr, z);
i_expr = int(sym_expr, z);

% 10. Visualization Pipeline
figure;
subplot(3, 1, 1);
plot(t(1:200), x_noisy(1:200));
title('Noisy Signal');
grid on;

subplot(3, 1, 2);
plot(t(1:200), filtered(1:200));
title('Filtered Signal');
grid on;

subplot(3, 1, 3);
plot(step_t, step_y);
title('Control Step Response');
grid on;

fprintf('Vectra Ultimate Workload completed cleanly with 0 errors.\n');
