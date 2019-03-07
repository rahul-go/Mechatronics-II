OS = 10;        %Percent overshoot [%]
T_s = 1;        %Settling time [sec]
zeta = -log(OS/100)/sqrt(pi()^2 + log(OS/100)^2);
theta = acos(zeta);
w_n = 4/(T_s*zeta);

x = -4/T_s
y = w_n*sin(theta)

