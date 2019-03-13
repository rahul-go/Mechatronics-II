

clc
clear all
close all
clear vars
format shortG

%% Variables
t_f=20;

g = 9.8;   %gravity [m/s^2]
m_1 = .023; %mass of wheel [kg]
m_2 = .538-2*m_1; %mass of body [kg]
r_1 = .0825; %radius of wheel [m]
r_2 = .0384; %distance from center of wheel to c.g. of body [m]
I_1 = .00003569; %moment of inertia of wheel [kg*m^2]
I_2 = .00190245; %moment of inertia of body [kg*m^2]

m_eff = m_1 + m_2 +(I_1/r_1^2); %effective mass [kg]
I_eff = m_2*r_2^2 + I_2; %effective moment of inertia [kg*m^2]
b_1 = 0; %damping coefficient from rolling resistance due to translation of x
b_2 = 0; %damping coefficient relative from rolling between wheels to body (theta 2-theta1)

%% Matrix breakup
A_1_1 = -(b_1*r_1^2*I_eff + b_2*(I_eff + m_2*r_1*r_2))/(r_1^2*(I_eff*m_eff - m_2^2*r_2^2));
A_1_2 = -(b_2*(I_eff + m_2*r_1*r_2))/(r_1*(I_eff*m_eff - m_2^2*r_2^2));
A_1_4 = (m_2^2*r_2^2*g)/(I_eff*m_eff - m_2^2*r_2^2);
A_2_1 = -(b_1*m_2*r_1^2*r_2 + b_2*(m_eff*r_1 + m_2*r_2))/(r_1^2*(I_eff*m_eff - m_2^2*r_2^2));
A_2_2 = -(b_2*(m_eff*r_1 + m_2*r_2))/(r_1*(I_eff*m_eff - m_2^2*r_2^2));
A_2_4 = (m_eff*m_2*r_2*g)/(I_eff*m_eff - m_2^2*r_2^2);
B_1 = (I_eff + m_2*r_1*r_2)/(r_1*(I_eff*m_eff - m_2^2*r_2^2));
B_2 = (m_eff*r_1 + m_2*r_2)/(r_1*(I_eff*m_eff - m_2^2*r_2^2));
A = [ A_1_1 A_1_2 0 A_1_4
      A_2_1 A_2_2 0 A_2_4
        1     0   0   0 
        0     1   0   0  ];

B = [B_1
     B_2
      0
      0 ];

%% poles  
%p = [-4+5.5i, -4-5.5i, -40, -50];

OS = 10;
T_s = 15;
[pole_1,pole_2] = Pole_Select(OS,T_s);

p = [pole_1, pole_2, pole_1*10, pole_2*10];
K = place(A,B,p);

sim('Closed_Loop');


%% Simulation
figure(1)
plot(tout, x_out_lin(:,3),'k',tout, x_out_lin(:,4),'b');
title('Position and Angle');
legend('Position ', 'Angle');
xlabel('time [s]');
range = [-1 1 -1 1 ];
figure(2)
plot(tout, torque);
title('Torque');
xlabel('time [s]');
disp("the max torque output is " + round(max(abs(torque)), 2) + " N-m");
disp("The poles are " + round(p(1),3, 'significant') + ", " + ...
    round(p(2),3, 'significant') + ", " + round(p(3),3,'significant') + ", " ...
    + round(p(4),3, 'significant'));
disp("The gain matrix is " + round(K(1), 3, 'significant') + ", " + ...
    round(K(2),3,'significant') + ", " + round(K(3),3,'significant') + ", " + ...
    round(K(4),3,'significant'));
Animate(tout, x_out_lin(:,3), x_out_lin(:,4),r_1,r_2, range);
