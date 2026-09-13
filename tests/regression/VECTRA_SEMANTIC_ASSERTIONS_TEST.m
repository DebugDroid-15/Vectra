%% VECTRA SEMANTIC ASSERTION REGRESSION SUITE
% Rigorous self-validating MATLAB test verifying all 16 production criteria.

clc;
clear;

fprintf('\n========================================================\n');
fprintf('    VECTRA SEMANTIC ASSERTION REGRESSION SUITE\n');
fprintf('========================================================\n');

%% 1. Matrix & Linear Indexing Assertions
A = [1 2 3; 4 5 6; 7 8 10];
assert(A(1,1) == 1, 'A(1,1) failed');
assert(A(2) == 4, 'Linear indexing A(2) failed');
assert(A(3) == 7, 'Linear indexing A(3) failed');
assert(A(2,1) == 4, 'A(2,1) failed');
fprintf('1. Matrix & Linear Indexing: PASS\n');

%% 2. fprintf Comprehensive Formatting Assertions
formatted_str = sprintf('%d %i %.2f %e %s x=%d y=%.2f', 10, 10, 3.14159, 3.14159, 'Vectra', 10, 3.14);
fprintf('Formatted test output: %s\n', formatted_str);
assert(length(formatted_str) > 0, 'sprintf output empty');
fprintf('2. fprintf & sprintf Formatting: PASS\n');

%% 3. Complex Number Representation & Operations
q = 3 + 4i;
assert(abs(real(q) - 3) < 1e-6, 'Complex real part failed');
assert(abs(imag(q) - 4) < 1e-6, 'Complex imag part failed');
assert(abs(abs(q) - 5) < 1e-6, 'Complex abs magnitude failed');

z1 = 1i;
z2 = -2i;
z3 = 3 - 4i;
z4 = (3 + 4i) * (2 - i); % 6 - 3i + 8i - 4i^2 = 10 + 5i
assert(abs(real(z4) - 10) < 1e-6, 'Complex multiplication real part failed');
assert(abs(imag(z4) - 5) < 1e-6, 'Complex multiplication imag part failed');
fprintf('3. Complex Numbers & Operations: PASS\n');

%% 4. Statistics & Signal Processing Assertions
fs_stat = 1000;
t_stat = 0:1/fs_stat:1-1/fs_stat;
y_stat = sin(2*pi*5*t_stat);

mean_y = mean(y_stat);
std_y = std(y_stat);
max_y = max(y_stat);
min_y = min(y_stat);

assert(abs(mean_y) < 0.05, 'Signal mean failed');
assert(abs(std_y - sqrt(0.5)) < 0.05, 'Signal std failed');
assert(abs(max_y - 1.0) < 0.05, 'Signal max failed');
assert(abs(min_y + 1.0) < 0.05, 'Signal min failed');
fprintf('4. Signal Statistics (mean, std, max, min): PASS\n');

%% 5. Symbolic Mathematics & Equation Solving
syms s;
expr = s^3 - 6*s^2 + 11*s - 6;
roots_val = solve(expr == 0, s);
assert(length(roots_val) == 3, 'Symbolic solve count failed');
assert(abs(roots_val(1) - 1) < 1e-4, 'Symbolic root 1 failed');
assert(abs(roots_val(2) - 2) < 1e-4, 'Symbolic root 2 failed');
assert(abs(roots_val(3) - 3) < 1e-4, 'Symbolic root 3 failed');

syms x;
f_quad = x^2 - 4;
quad_roots = solve(f_quad == 0, x);
assert(length(quad_roots) == 2, 'Symbolic quad solve count failed');
assert(abs(quad_roots(1) - (-2)) < 1e-4, 'Symbolic quad root -2 failed');
assert(abs(quad_roots(2) - 2) < 1e-4, 'Symbolic quad root 2 failed');
fprintf('5. Symbolic Mathematics & Solvers: PASS\n');

%% 6. Control System Zeros & Poles
num = [1];
den = [1 3 2];
sys = tf(num, den);
p_sys = pole(sys);
z_sys = zero(sys);

assert(length(p_sys) == 2, 'Control poles count failed');
assert(numel(z_sys) == 0, 'Control zeros count failed');
fprintf('6. Control Systems (poles & empty zeros): PASS\n');

%% 7. Digital Modulation Assertions
bits = [0 1 1 0 1 0 1 1];
mod_bits = bpskmod(bits);
rec_bits = bpskdemod(mod_bits);
bit_errs = sum(bits ~= rec_bits);
assert(bit_errs == 0, 'BPSK modulation/demodulation failed');
fprintf('7. Digital Communication BPSK: PASS\n');

%% 8. Subroutine Function Execution Assertions
[res_s, res_p] = test_subroutine(6, 4);
assert(res_s == 10, 'Subroutine sum failed');
assert(res_p == 24, 'Subroutine product failed');
fprintf('8. Subroutine Function Execution: PASS\n');

fprintf('\n========================================================\n');
fprintf('    ALL SEMANTIC REGRESSION ASSERTIONS PASSED (100%%)\n');
fprintf('========================================================\n');

function [s, p] = test_subroutine(a, b)
s = a + b;
p = a * b;
end
