function [] = Animate(t, x,theta,r_1,r_2,range)
%UNTITLED2 Summary of this function goes here
%   Detailed explanation goes here
      %Distance between wheel center and cg

x1 = x;
y1 = r_1;
x2 = x - r_2*sin(theta);
y2 = y1 + r_2*cos(theta);



for i = 1:length(t)
    figure(2)
    plot([x1(i), x2(i)], [y1, y2(i)])
    axis(range)
    pause(.05)
    
end

