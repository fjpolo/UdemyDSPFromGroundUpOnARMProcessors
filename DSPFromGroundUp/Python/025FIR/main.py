#
# Imports
#
from matplotlib import pyplot as plt
import mysignals as sigs
from scipy import signal
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
    # time
    t = np.linspace(0,1.0,2001)
    # signals
    sig_5hz = np.sin(2*np.pi*5*t)
    sig_250hz = np.sin(2*np.pi*250*t)
    sig_5hz_250hz = sig_5hz + sig_250hz

    # Filter
    b,a = signal.butter(8,0.125)
    filtered_signal = signal.filtfilt(b,a,sig_5hz_250hz, padlen=150)

    # Plot
    style.use('dark_background')

    f, plt_arr =plt.subplots(4,sharex=True)
    f.suptitle('Filtfilt Filter')

    plt_arr[0].plot(sig_5hz,color='red')
    plt_arr[0].set_title("5Hz Signal", color ='red')

    plt_arr[1].plot(sig_250hz,color='red')
    plt_arr[1].set_title(" 250Hz Signal", color ='red')

    plt_arr[2].plot(sig_5hz_250hz,color='yellow')
    plt_arr[2].set_title("Combined  5hz and 250hz signal", color ='yellow')

    plt_arr[3].plot(filtered_signal,color='magenta')
    plt_arr[3].set_title("Filtered Signal", color ='magenta')
    plt.show()



