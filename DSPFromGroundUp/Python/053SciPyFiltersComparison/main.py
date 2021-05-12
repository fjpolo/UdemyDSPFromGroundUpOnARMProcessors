#
# Imports
#
from scipy import signal
from scipy.signal import lfilter, lfilter_zi, filtfilt, butter
from numpy import sin, cos, pi, linspace
from numpy.random import randn
from matplotlib.pyplot import plot, legend, grid, figure, show

#
# Global variables
#
t = linspace(-1, 1, 201)    # fs = 200Hz  
x1 = sin(2*pi*0.75*t*(1-t))
x2 = 2.1 + 0.1*sin(2*pi*1.25*t+1)
x3 = 0.18*cos(2*pi*3.85*t)
x = x1 + x2 + x3
xn = x + randn(len(t))*0.08


#
# Private functions
#



#
# main
#
if __name__ == "__main__":

    #
    # Butterworth filter
    #
    b,a = butter(3, 0.05)
    zi = lfilter_zi(b, a)
    z1, _ = lfilter(b, a, xn, zi=zi*xn[0])
    z2, _ = lfilter(b, a, z1, zi=zi*z1[0])
    y = filtfilt(b, a, xn)
    

    # Plot
    figure()
    plot(t,xn, 'b', linewidth=2)
    plot(t,z1, 'r--', linewidth=2)
    plot(t,z2, 'r', linewidth=2)
    plot(t,y, 'g', linewidth=2)
    legend(['Input', 'lfilter_once', 'lfilter_twice', 'filtfilt'])
    grid()
    #
    show()
