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
    b,a = signal.ellip(4,5,40,100,'low', analog=True)
    print("b: ", b)
    print("a: ", a)    
    # w: freq, h: amplitude
    w,h = signal.freqs(b,a)   
    
    
    # Plot
    plt.xscale('log')
    plt.plot(w,20*np.log10(abs(h)))
    plt.title("Elliptic filter frequency response(rp=5, rs=40)")
    plt.xlabel("Frequency (rads/second)")
    plt.ylabel("Amplitude (dB)")
    plt.margins(0,0.1)
    plt.grid(which='both', axis='both')

    plt.axvline(100,color='magenta')
    plt.axhline(-40,color='red')
    plt.axhline(-5,color='green')

    plt.show()



