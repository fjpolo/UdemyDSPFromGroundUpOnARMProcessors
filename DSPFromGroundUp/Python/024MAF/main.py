#
# Imports
#
from matplotlib import pyplot as plt
import mysignals as sigs
from scipy import signal
from matplotlib import style


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
    # MAF
    median_filter_output = signal.medfilt(sigs.InputSignal_1kHz_15kHz,11)


    # Plot
    style.use('dark_background')

    f, plt_arr =plt.subplots(2,sharex=True)
    f.suptitle('Median Filter')

    plt_arr[0].plot(sigs.InputSignal_1kHz_15kHz,color='red')
    plt_arr[0].set_title("Input Signal", color ='red')

    plt_arr[1].plot(median_filter_output,color='cyan')
    plt_arr[1].set_title("Output Signal", color ='cyan')

    plt.show()



