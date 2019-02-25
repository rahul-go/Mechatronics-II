function [x_dot] = botEOM(t, x, T_m)

%% Variables
g = 32.174;   %gravity
weight_1=1.1/16;
weight_2=1.63-2*weight_1
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

%% matrices
A1 = [m_eff -m_2*r_2*cos(x(4)) 0 0
     -m_2*r_2*cos(x(4)) I_eff 0 0
      0 0 1 0
      0 0 0 1];
A2 = [-T_m/r_1 - (b_2/r_1^2)*x(1) - (b_2/r_1)*x(2) - b_1*x(1) - m_2*r_2*x(2)^2*sin(x(4))
    T_m - (b_2/r_1)*x(1) - b_2*x(2) + m_2*r_2*g*sin(x(4))
    x(1)
    x(2)]

x_dot = inv(A1)*A2;



