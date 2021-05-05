#
# Imports
#
from matplotlib import pyplot as plt
from matplotlib import style
import mysignals as sigs
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
    output_signal = np.cumsum(sigs.InputSignal_1kHz_15kHz)

    #style.use('ggplot')
    style.use('dark_background')

    f,plt_arr = plt.subplots(2,sharex=True)
    f.suptitle("Running Sum")

    plt_arr[0].plot(sigs.InputSignal_1kHz_15kHz,color='yellow')
    plt_arr[0].set_title("Input Signal")

    plt_arr[1].plot(output_signal,color ='magenta')
    plt_arr[1].set_title("Output Signal")

    plt.show()