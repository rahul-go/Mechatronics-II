clc
clear vars
%% Variables
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
p = [-1,-2,-3,-4]
K = place(A,B,p)