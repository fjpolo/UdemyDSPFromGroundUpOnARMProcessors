#
# Imports
#
import mysignals as sigs
from matplotlib import pyplot as plt
from matplotlib import style
import csv

#
# Global variables
#
csvfile = "conv_output_signal.txt"


#
# Private functions
#

# convolution(inputArr, impRespArr, outputArr)
def convolution(inputArr, impRespArr, outputArr):
    """
    convolution(inputArr, impRespArr, outputArr):

     Convolve two signals. Takes input array, impulse response array and
    output array and modified the output array with the convolution.-
    """
    # Loop through total len of convolved signal. Init output arr
    for x in range(len(inputArr)+len(impRespArr)):
        outputArr[x] = 0
    # Loop through input signal len
    for x in range(len(inputArr)):
        # Loop throug impulse response len
        for y in range(len(impRespArr)):
            outputArr[x+y] += inputArr[x] * impRespArr[y]
    # Save in txt file
    with open(csvfile,"w") as output:
        writer = csv.writer(output, lineterminator =',')
        for x in outputArr:
            writer.writerow([x])
    
    

#
# main
#
if __name__ == "__main__":
    # Convolve
    output_signal = [None]*(len(sigs.InputSignal_1kHz_15kHz)+len(sigs.Impulse_response))
    convolution(sigs.InputSignal_1kHz_15kHz,sigs.Impulse_response, output_signal)
    # Plot
    style.use('ggplot')
    style.use('dark_background')
    fig,plt_arr =plt.subplots(3,sharex=True)
    fig.suptitle("Convolution")
    plt_arr[0].plot(sigs.InputSignal_1kHz_15kHz)
    plt_arr[0].set_title("Input Signal")
    plt_arr[1].plot(sigs.Impulse_response, color = 'brown')
    plt_arr[1].set_title("Impulse Response", color ='brown')
    plt_arr[2].plot(output_signal, color ='green')
    plt_arr[2].set_title("Output Signal", color='green')
    plt.show()