#
# Imports
#
from scipy import signal
from matplotlib import pyplot as plt
import numpy as np


#
# Global variables
#


#
# Private functions
#


#
# main
#
if __name__ == "__main__":
    # Filter
    b = signal.firwin(80,0.5, window=('kaiser',8))
    # w: freq, h: amplitude
    w,h = signal.freqz(b)

    # Plot
    plt.semilogy(w,np.abs(h),'g')
    plt.ylabel('Amplitude (db)',color='b')
    plt.xlabel('Freuency (rad/sample)')
    plt.show()



