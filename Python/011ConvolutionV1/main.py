#
# Imports
#
import mysignals as sigs
from matplotlib import pyplot as plt
from matplotlib import style
from scipy import signal

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
    # Convolve
    output_signal = signal.convolve(sigs.InputSignal_1kHz_15kHz,sigs.Impulse_response, mode='same')
    # style
    style.use('ggplot')
    style.use('dark_background')
     # figures
    fig,plt_arr = plt.subplots(3,sharex=True)
    fig.suptitle("Convolution")
    plt_arr[0].plot(sigs.InputSignal_1kHz_15kHz, color ='cyan')
    plt_arr[0].set_title("Input Signal")
    plt_arr[1].plot(sigs.Impulse_response, color ='pink')
    plt_arr[1].set_title("Impulse Response")
    plt_arr[2].plot(output_signal, color ='magenta')
    plt_arr[2].set_title("Output Signal")
    # show plot
    plt.show()