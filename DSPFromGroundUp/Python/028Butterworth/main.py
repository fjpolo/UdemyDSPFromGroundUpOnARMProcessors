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
    b,a = signal.butter(4,100,'low',analog=True)
    print("b: ", b)
    print("a: ", a)    
    # w: freq, h: amplitude
    w,h = signal.freqs(b,a)
    
    
    # Plot
    plt.plot(w,20*np.log10(abs(h)))
    plt.xscale('log')

    plt.title('Butterworth filter frequencry response')
    plt.xlabel('Frequency (rads/second)')
    plt.ylabel('Amplitude (db)')
    plt.margins(0,0.2)
    plt.grid()
    plt.axvline(100,color='green')
    plt.show()



