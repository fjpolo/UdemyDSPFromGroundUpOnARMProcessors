#
# Imports
#
import numpy as np
import signals as sigs

#
# Global variables
#
_mean =0.0

#
# Private functions
#
def calc_mean(sig_src_arr):
    """
    Takes an array and returns its mean.-
    """
    global _mean
    for x in range(len(sig_src_arr)):
        _mean += sig_src_arr[x]
    _mean = _mean/len(sig_src_arr)
    return _mean

#
# main
#
if __name__ == "__main__":
    print("The signal's mean is: ", calc_mean(sigs.InputSignal_1kHz_15kHz))
    # [Done] exited with code=0 in 5.216 seconds

