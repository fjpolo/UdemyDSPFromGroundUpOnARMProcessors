#
# Imports
#
from scipy import signal
from matplotlib import pyplot as plt
from matplotlib import style
from scipy import signal
import numpy as np



#
# Global variables
#
t = np.linspace(-10, 10, 10)  
y = 1 + t + 0.01 * t**2

#
# Private functions
#



#
# main
#
if __name__ == "__main__":
    # Detrend
    yconst = signal.detrend(y, type='constant')
    ylin = signal.detrend(y, type='linear')
    #
    # style.use("dark_background")
    plt.plot(t, y, '-rx')
    plt.plot(t, yconst, '-bo')
    plt.plot(t, ylin, '-k+')
    plt.grid()
    plt.legend(['Input', 'Constant detrend', 'Linear detrend'])
    #
    plt.show()
