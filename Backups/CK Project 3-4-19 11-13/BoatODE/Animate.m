function [] = Animate(t, x,theta)
%UNTITLED2 Summary of this function goes here
%   Detailed explanation goes here
r = 1;      %Distance between wheel center and cg

x1 = x;
y1 = x*0;
x2 = x - r*sin(theta);
y2 = y1 + r*cos(theta);



for i = 1:length(t)
    figure(2)
    plot([x1(i), x2(i)], [y1(i), y2(i)])
    axis([-5 5 -5 5])
    pause(.1)
    
end

