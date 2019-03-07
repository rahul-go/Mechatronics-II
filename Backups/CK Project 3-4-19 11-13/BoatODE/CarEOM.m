%% CarEOM Usage and Description
% This function represents the equations of motion for the simulation. It
% returns xdot with inputs of time, x, the A and B state-space matrices,
% the slope data, and the horizontal velocity of the car. See the attached
% sheet for hand calculations.
%
% To find u (in this case, the vertical component of the velocity of
% the car) corresponding to the time and x value, this function solves for
% the corresponding distance value, from which it interpolates the
% corresponding slope value, from which it solves for the corresponding u
% value, the vertical component of the velocity of the car. Then, knowing
% the x and u values, the script solves y = A*x + B*u using matrix
% multiplication.

function [xdot] = CarEOM(t, x, A, B, slope, v_x)

x_r = v_x*t;                    % Distance of car (ft)

% Interpolate slope (m) from distance (in/ft)
m_r = interp1(slope(:, 1), slope(:, 2), x_r);

u = v_x*m_r;                    % Vertical velocity (yr_dot) of car (ft/s)

xdot = A*x + B*u;

end