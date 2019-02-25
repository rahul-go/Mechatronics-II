function [x_dot] = botEOM(t, x, A, B, T_m)

%% Variables
g = -32.174;   %gravity
weight_1=1.1/16;
weight_2=1.63-2*weight_1
m_1 = -1*weight_1/g; %mass of wheel, slug
m_2 = -1*weight_2/g; %mass of body
r_1 = 2.55/2; %radius of wheel
r_2 = 1.028; %distance from center of wheel to c.g. of body
I_1 = m_1*r_1^2; %moment of inertia of wheel slug*in^2
I_2 = 1; %moment of inertia of body

m_eff = m_1 + m_2 +(I_1/r_1^2); %effective mass
I_eff = m_2*r_2^2 + I_2; %effective moment of inertia
b_1 = 0; %damping coefficient from rolling resistance due to translation of x
b_2 = 0; %damping coefficient relative from rolling between wheels to body (theta 2-theta1)
T_m = 0; %torque to wheels .75lbin for both wheels max speed 3.6rot/s
%% matrices
A1 = [m_eff -m_2*r_2*cos(y(4)) 0 0
     -m_2*r_2*cos(y(4)) I_eff 0 0
      0 0 1 0
      0 0 0 1];
A2 = [-T_m/r_1 - b_2/r_1

x_dot = A*x + B*T_m;



