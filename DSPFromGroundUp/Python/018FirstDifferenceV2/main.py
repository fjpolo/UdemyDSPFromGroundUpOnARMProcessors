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
def calc_first_difference(sig_src_arr,sig_dest_arr):
    for x in range(len(sig_dest_arr)):
        sig_dest_arr[x] =0

    for x in range(len(sig_src_arr)):
        sig_dest_arr[x] = sig_src_arr[x] - sig_src_arr[x-1]
        

    


#
# main
#
if __name__ == "__main__":
    output_signal =[None]*320
    calc_first_difference(sigs.InputSignal_1kHz_15kHz,output_signal)
    
    # Plot
    style.use('ggplot')
    #style.use('dark_background')

    f,plt_arr = plt.subplots(2,sharex=True)
    f.suptitle("First Difference")

    plt_arr[0].plot(sigs.InputSignal_1kHz_15kHz,color='red')
    plt_arr[0].set_title("Input Signal")

    plt_arr[1].plot(output_signal,color ='magenta')
    plt_arr[1].set_title("Output Signal")

    plt.show()



