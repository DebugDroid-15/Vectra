clc;
clear;

% 1. Variables and Range Vectors
fs = 2000;
T = 1;
t = 0:1/fs:T;

% 2. Complex Signal Processing
x = sin(2*pi*50*t) + 0.5*sin(2*pi*150*t);
noise = 0.1*randn(size(t));
x_noisy = x + noise;

% 3. FFT Analysis
X = fft(x_noisy);

% 4. Matrix Arithmetic & Column-Major Indexing
A = [1 2; 3 4];
linear_val = A(2); % Must equal 3

% 5. Linear Algebra Operations
[U, S, V] = svd(A);

% 6. Digital Filtering
[b, a] = butter(4, 200/(fs/2));
filtered = filter(b, a, x_noisy);

% 7. Modulation Pipeline
m = sin(2*pi*10*t);
s_am = ammod(m, 100, fs);

% 8. Plotting Operations
figure;
subplot(2, 1, 1);
plot(t(1:200), x_noisy(1:200));
title('Noisy Signal');
grid on;

subplot(2, 1, 2);
plot(t(1:200), filtered(1:200));
title('Filtered Signal');
grid on;

