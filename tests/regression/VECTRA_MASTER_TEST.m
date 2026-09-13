%% VECTRA MASTER TEST
% One-file MATLAB compatibility and engineering test

clc;
clear;

fprintf('\n========== VECTRA MASTER TEST ==========\n');

%% 1. Variables, ranges, arrays, indexing
a = 10;
b = 20;
x = 0:0.01:1;

A = [1 2 3;
     4 5 6;
     7 8 10];

fprintf('A(1,1) = %d\n', A(1,1));
fprintf('A(2)   = %d\n', A(2));

if A(2) == 4
    fprintf('Indexing: PASS\n');
else
    fprintf('Indexing: FAIL\n');
end

%% 2. Matrix operations
B = eye(3);
C = A + B;
D = A * B;
E = A .* A;

fprintf('det(A)   = %.4f\n', det(A));
fprintf('rank(A)  = %d\n', rank(A));
fprintf('trace(A) = %.4f\n', trace(A));

Ai = inv(A);
fprintf('Inverse error = %.2e\n', max(abs(A*Ai-eye(3))));

%% 3. Mathematics and statistics
y = sin(2*pi*50*x);
z = cos(2*pi*50*x);

fprintf('Mean = %.6f\n', mean(y));
fprintf('Std  = %.6f\n', std(y));
fprintf('Max  = %.6f\n', max(y));
fprintf('Min  = %.6f\n', min(y));

%% 4. Complex numbers
q = 3 + 4i;

fprintf('|q| = %.2f\n', abs(q));
fprintf('Real = %.2f\n', real(q));
fprintf('Imag = %.2f\n', imag(q));

%% 5. Control flow
total = 0;

for k = 1:10
    if mod(k,2) == 0
        total = total + k;
    end
end

fprintf('Even number sum = %d\n', total);

%% 6. Signal generation + noise
fs = 2000;
t = 0:1/fs:1;

signal = sin(2*pi*50*t) + 0.5*sin(2*pi*150*t) + 0.25*sin(2*pi*300*t);

noise = 0.1*randn(size(t));
noisy = signal + noise;

fprintf('Signal RMS = %.4f\n', sqrt(mean(noisy.^2)));

%% 7. FFT
N = length(noisy);

X = fft(noisy);
X = fftshift(X);

f = (-N/2:N/2-1)*(fs/N);

mag = abs(X);

figure;
plot(f,mag);
title('VECTRA FFT');
xlabel('Frequency (Hz)');
ylabel('Magnitude');
grid on;

%% 8. DSP filter
[b,a] = butter(4,200/(fs/2));

filtered = filter(b,a,noisy);

[H,w] = freqz(b,a,1024,fs);

figure;

subplot(2,1,1);
plot(t,noisy);
title('Noisy Signal');
xlabel('Time (s)');
ylabel('Amplitude');
grid on;

subplot(2,1,2);
plot(t,filtered);
title('Filtered Signal');
xlabel('Time (s)');
ylabel('Amplitude');
grid on;

%% 9. Convolution and correlation
h = [1 0.5 0.25];

conv_result = conv(signal,h);
corr_result = xcorr(signal(1:100),signal(1:100));

fprintf('Convolution length = %d\n', length(conv_result));
fprintf('Correlation length = %d\n', length(corr_result));

%% 10. Communication system
message = sin(2*pi*20*t);

am = ammod(message,500,fs);
received = awgn(am,20);
demodulated = amdemod(received,500,fs);

fprintf('AM communication completed.\n');

figure;

subplot(3,1,1);
plot(t,message);
title('Message');
grid on;

subplot(3,1,2);
plot(t,am);
title('AM Signal');
grid on;

subplot(3,1,3);
plot(t,demodulated);
title('Demodulated Signal');
grid on;

%% 11. Digital communication
bits = [0 1 1 0 1 0 1 1];

modulated_bits = bpskmod(bits);
recovered_bits = bpskdemod(modulated_bits);

errors = sum(bits ~= recovered_bits);

fprintf('BPSK bit errors = %d\n',errors);

%% 12. Control system
num = [1];
den = [1 3 2];

sys = tf(num,den);

p = pole(sys);
[z0] = zero(sys);

fprintf('Control-system poles:\n');
disp(p);

fprintf('Control-system zeros:\n');
disp(z0);

[y_step,t_step] = step(sys);

figure;
plot(t_step,y_step);
title('Control System Step Response');
xlabel('Time (s)');
ylabel('Amplitude');
grid on;

%% 13. Symbolic mathematics
syms s;

expr = s^3 - 6*s^2 + 11*s - 6;

derivative = diff(expr,s);
integral_value = int(expr,s);
solutions = solve(expr == 0,s);

fprintf('Symbolic expression:\n');
disp(expr);

fprintf('Derivative:\n');
disp(derivative);

fprintf('Integral:\n');
disp(integral_value);

fprintf('Roots:\n');
disp(solutions);

%% 14. 3D graphics
[X,Y] = meshgrid(-5:0.25:5);

R = sqrt(X.^2 + Y.^2);
Z = sinc(R);

figure;
surf(X,Y,Z);
title('VECTRA 3D Surface');
xlabel('X');
ylabel('Y');
zlabel('Z');

%% 15. Function test
[result_sum,result_product] = test_function(6,4);

fprintf('Function sum = %d\n',result_sum);
fprintf('Function product = %d\n',result_product);

%% Final
fprintf('\n========================================\n');
fprintf('         VECTRA MASTER TEST DONE\n');
fprintf('========================================\n');
fprintf('Workspace variables, matrices, signals,\n');
fprintf('FFT, DSP, communications, control,\n');
fprintf('symbolic math and graphics were executed.\n');
fprintf('========================================\n');


function [s,p] = test_function(a,b)

s = a + b;
p = a * b;

end

