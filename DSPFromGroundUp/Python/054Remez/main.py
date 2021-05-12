#
# Imports
#
from scipy.signal import freqz, remez
import numpy as np
from matplotlib import pyplot as plt


#
# Global variables
#

# Filter with passband 0.2-0.4Hz, stopband 0-0.1Hz and 0.45-0.5Hz
BPfilter = remez(72, [0, 0.1, 0.2, 0.4, 0.45, 0.5], [0, 1, 0])


#
# Private functions
#



#
# main
#
if __name__ == "__main__":
    # Plot
    freq, response = freqz(BPfilter)
    amp = abs(response)
    plt.semilogy(freq / (2*np.pi), amp, 'b')
    plt.grid()
    #
    plt.show()
