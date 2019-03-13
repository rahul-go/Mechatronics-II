

clc
clear all
close all
clear vars
format shortG

%% Variables
t_f=20;

g = 32.174;   %gravity
weight_1=1.1/16;    %weight of wheel, lbf
weight_2=1.63-2*weight_1;       %weight of body, lbf
m_1 = weight_1/g; %mass of wheel, slug
m_2 = weight_2/g; %mass of body
r_1 = 2.55/2; %radius of wheel
r_2 = 1.028; %distance from center of wheel to c.g. of body
I_1 = m_1*r_1^2; %moment of inertia of wheel slug*in^2
I_2 = 1; %moment of inertia of body

m_eff = m_1 + m_2 +(I_1/r_1^2); %effective mass
I_eff = m_2*r_2^2 + I_2; %effective moment of inertia
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
range = [-20 20 -20 20];
figure(2)
plot(tout, torque);
title('Torque');
xlabel('time [s]');
disp("the max torque output is " + round(max(abs(torque)), 2) + " in-lbs");
disp("The poles are " + round(p(1),3, 'significant') + ", " + ...
    round(p(2),3, 'significant') + ", " + round(p(3),3,'significant') + ", " ...
    + round(p(4),3, 'significant'));
disp("The gain matrix is " + round(K(1), 3, 'significant') + ", " + ...
    round(K(2),3,'significant') + ", " + round(K(3),3,'significant') + ", " + ...
    round(K(4),3,'significant'));
Animate(tout, x_out_lin(:,3), x_out_lin(:,4),r_1,r_2, range);
