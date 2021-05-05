#
# Imports
#
from scipy import signal
import numpy as np


#
# Global variables
#
csvfile = "conv_output_signal.txt"


#
# Private functions
#
    
    

#
# main
#
if __name__ == "__main__":
    sig = np.array([0,0,0,0,1,1,1,1])
    filter = np.array([1,1,0])

    conv_result = signal.convolve(sig,filter)
    deconv_result = signal.deconvolve(conv_result,filter)

    print("Convolution result :")
    print(conv_result)
    print("Deconvolution result : ")
    print(deconv_result)
    """
        Convolution result :
        [0 0 0 0 1 2 2 2 1 0]
        Deconvolution result : 
        (array([0., 0., 0., 0., 1., 1., 1., 1.]), 
        array([0., 0., 0., 0., 0., 0., 0., 0., 0., 0.]))

        [Done] exited with code=0 in 3.447 seconds
    """