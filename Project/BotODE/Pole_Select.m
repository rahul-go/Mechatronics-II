function [pole_1,pole_2] = Pole_Select(OS,T_s)
%UNTITLED2 Summary of this function goes here
%   OS = % overshoot [%]
%   T_s = settling time [s]

zeta = -log(OS/100)/sqrt(pi()^2 + log(OS/100)^2);
theta = acos(zeta);
w_n = 4/(T_s*zeta);

x = -4/T_s;
y = w_n*sin(theta); 

pole_1 = x+y*i;
pole_2 = x-y*i;
end

