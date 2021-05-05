#
# Imports
#
from matplotlib import pyplot as plt
from matplotlib import style
import mysignals as sigs


#
# Global variables
#


#
# Private functions
#

#
def calc_running_sum(sig_src_arr,sig_dest_arr):
    for x in range(len(sig_dest_arr)):
        sig_dest_arr[x] = 0

    for x in range(len(sig_src_arr)):
        sig_dest_arr[x] =  sig_dest_arr[x-1]+sig_src_arr[x]    

    
    

#
# main
#
if __name__ == "__main__":
    output_signal =[None]*320
    calc_running_sum(sigs.InputSignal_1kHz_15kHz,output_signal)
    #
    style.use('ggplot')
    #style.use('dark_background')

    f,plt_arr = plt.subplots(2,sharex=True)
    f.suptitle("Running Sum")

    plt_arr[0].plot(sigs.InputSignal_1kHz_15kHz,color='red')
    plt_arr[0].set_title("Input Signal")

    plt_arr[1].plot(output_signal,color ='magenta')
    plt_arr[1].set_title("Output Signal")

    plt.show()
