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
t = np.linspace(0, 1.0, 2001)   # f_Nyq = 1000 -> fc = 0.25 * f_Nyq
sig_5Hz = np.sin(2 * np.pi * 5 * t)
sig_250Hz = np.sin(2 * np.pi * 250 * t)
sig_5Hz_250Hz = sig_5Hz + sig_250Hz
# Butterworth LP
b, a = signal.butter(8, 0.125)  # 8 = 1 / 0.125


#
# Private functions
#



#
# main
#
if __name__ == "__main__":
    # FIlter signal
    outputSignal = signal.filtfilt(b, a, sig_5Hz_250Hz, padlen=150)

    #
    style.use("dark_background")
    fig, pltArr = plt.subplots(4, sharex=True) 
    fig.suptitle("Forward-Backward Filter")
    pltArr[0].plot(sig_5Hz, color='red')
    pltArr[0].set_title("5Hz Signal", color='red')
    pltArr[1].plot(sig_250Hz, color='cyan')
    pltArr[1].set_title("250Hz Signal", color='cyan')
    pltArr[2].plot(sig_5Hz_250Hz, color='yellow')
    pltArr[2].set_title("5Hz+250Hz Signal", color='yellow')
    pltArr[3].plot(outputSignal, color='blue')
    pltArr[3].set_title("Filtered Signal", color='blue')

    #
    plt.show()
