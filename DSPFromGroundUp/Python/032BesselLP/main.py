#
# Imports
#
from scipy import signal
from matplotlib import pyplot as plt
from matplotlib import style
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
    plt.plot(w,20*np.log10(abs(h)), color='silver', ls='dashed')

    b,a= signal.bessel(4,100,'low',analog=True)
    w,h = signal.freqs(b,a)
    plt.plot(w,20*np.log10(abs(h)))
    plt.xscale('log')
    plt.title("Bessel filter frequency response (with Butterworth)")
    plt.xlabel("Frequency (rads/second)")
    plt.ylabel("Amplitude (dB)")
    plt.margins(0,0.1)
    plt.grid(which='both', axis='both')
    plt.axvline(100,color='green')
    plt.show()



