#
# Imports
#
import numpy as np
import signals as sig

#
# Global variables
#
_mean =0.0
_variance =0.0
_std = 0.0

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

def calc_variance(sig_src_arr):
    """
    Takes an array and returns its variance.-
    """
    global _mean
    global _variance
    
    for x in range(len(sig_src_arr)):
        _mean += sig_src_arr[x]
    _mean = _mean / len(sig_src_arr)

    for x in range(len(sig_src_arr)):
        _variance = _variance + (sig_src_arr[x]-_mean)**2
    _variance = _variance /(len(sig_src_arr))
    return _variance

def calc_standard_deviation(sig_src_arr):
    """
    Takes an array and returns its STD.-
    """
    global _mean
    global _variance
    global _std
    
    for x in range(len(sig_src_arr)):
        _mean += sig_src_arr[x]
    _mean = _mean / len(sig_src_arr)

    for x in range(len(sig_src_arr)):
        _variance = _variance + (sig_src_arr[x]-_mean)**2
    _variance = _variance /(len(sig_src_arr))
    _std = _variance**(.5)
    return _std


#
# main
#
if __name__ == "__main__":
    print(calc_standard_deviation(sig.InputSignal_1kHz_15kHz))
    # [Done] exited with code=0 in 1.763 seconds