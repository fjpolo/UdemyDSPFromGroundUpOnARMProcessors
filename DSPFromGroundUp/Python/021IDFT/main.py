#
# Imports
#
import mysignals as sigs
from matplotlib import pyplot as plt
from matplotlib import style
import math


#
# Global variables
#


#
# Private functions
#

#
def calc_dft(sig_src_arr, ReXArr, ImXArr, MagArr):
    for j in range(int(len(sig_src_arr)/2)):
        ReXArr[j] =0
        ImXArr[j] =0
        

    for k in range(int(len(sig_src_arr)/2)):
        for i in range(len(sig_src_arr)):
            ReXArr[k] += sig_src_arr[i]*math.cos(2*math.pi*k*i/len(sig_src_arr))
            ImXArr[k] -= sig_src_arr[i]*math.sin(2*math.pi*k*i/len(sig_src_arr))

    for x in range(int(len(sig_src_arr)/2)):
        MagArr[x] = math.sqrt(math.pow(ReXArr[x],2)+math.pow(ImXArr[x],2))
        
    
#       
def calc_idft(sig_src_rex_arr, sig_src_imx_arr, outputArr):

     for j in range(len(sig_src_rex_arr)*2):
         outputArr[j] =0


     for x in range(len(sig_src_rex_arr)):
        sig_src_rex_arr[x] =  sig_src_rex_arr[x]/len(sig_src_rex_arr)
        sig_src_imx_arr[x] =  sig_src_imx_arr[x]/len(sig_src_rex_arr)


     for k in range(len(sig_src_rex_arr)):
        for i in range(len(sig_src_rex_arr)*2):
            outputArr[i] = outputArr[i] + sig_src_rex_arr[k] *math.cos(2*math.pi*k*i/(len(sig_src_rex_arr)*2))
            outputArr[i] = outputArr[i] + sig_src_imx_arr[k] *math.sin(2*math.pi*k*i/(len(sig_src_rex_arr)*2))
   
    


#
# main
#
if __name__ == "__main__":
    input = sigs.InputSignal_1kHz_15kHz
    ReX = [None]*int((len(input)/2))
    ImX = [None]*int((len(input)/2))
    MagInput = [None]*int((len(input)/2))
    newSignal = [None] * int((len(input)))

    #DFT
    calc_dft(input, ReX, ImX, MagInput)

    # IDFT
    calc_idft(ReX, ImX, newSignal)

    # Plot
    style.use('ggplot')
    fig,plt_arr = plt.subplots(5, sharex=True)
    fig.suptitle("Discrete Fourier Transform (DFT)")

    plt_arr[0].plot(input, color='red')
    plt_arr[0].set_title("Input Signal",color='red')
    
    plt_arr[1].plot(ReX, color='green')
    plt_arr[1].set_title("Frequency Domain(Real part)",color='green')

    plt_arr[2].plot(ImX, color='green')
    plt_arr[2].set_title("Frequency Domain(Imaginary part)",color='green')

    plt_arr[3].plot(MagInput, color='magenta')
    plt_arr[3].set_title("Frequency Domain (Magnitude))",color='magenta')

    plt_arr[4].plot(newSignal, color='magenta')
    plt_arr[4].set_title("Time Domain (Outout from Inverse DFT))",color='yellow')

    plt.show()



