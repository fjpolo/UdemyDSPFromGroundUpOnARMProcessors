#
# Imports
#
from matplotlib import pyplot as plt
from matplotlib import style
from signals import InputSignal_1kHz_15kHz
import numpy as np

#
# Global variables
#
x =np.array([1,2,3,4,5,6])
y =np.array([7,5,6,7,8,9])
npInputSignal_1kHz_15kHz = np.array(InputSignal_1kHz_15kHz)

#
# Private functions
#

#
# main
#
if __name__ == "__main__":
    # prepare figure
    style.use("ggplot")
    style.use('dark_background')
    # sublots
    fig, plt_arr = plt.subplots(3, sharex=True)
    fig.suptitle("Multiplot")
    # draw using subplots
    plt_arr[0].plot(npInputSignal_1kHz_15kHz, color='magenta')
    # plt_arr[0].set_title("Subplot 1")
    plt_arr[0].set_title("Subplot 1", color='magenta')
    plt_arr[1].plot(np.divide(npInputSignal_1kHz_15kHz, 2), color='red')
    plt_arr[1].set_title("Subplot 2")
    plt_arr[2].plot(np.divide(npInputSignal_1kHz_15kHz, 0.5), color="yellow")
    plt_arr[2].set_title("Subplot 3")
    # labels
    plt.xlabel('X axis')
    plt.ylabel('Y axis')
    plt.legend()
    # show plot
    plt.show()
