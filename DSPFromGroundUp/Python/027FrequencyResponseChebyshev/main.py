#
# Imports
#
from scipy.signal import freqs, iirfilter
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
    b,a = iirfilter(4,[1,10],1,60, analog =True,ftype='cheby1')
    # w: freq, h: amplitude
    w,h= freqs(b,a, worN=np.logspace(-1,2,1000))
    
    
    # Plot
    plt.semilogx(w,abs(h))
    plt.xlabel('Frequency')
    plt.ylabel('Amplitude Response')
    plt.grid()
    plt.show()



