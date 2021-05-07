#
# Imports
#
from scipy.signal import butter, lfilter, freqz
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import style


#
# Global variables
#


#
# Private functions
#

# ButterworthBP_createKernel(fc_low, fc_high, fs, order =5)
def ButterworthBP_createKernel(fc_low, fc_high, fs, order =5):
    """
    ButterworthBP_createKernel(fc_low, fc_high, fs, order =5):

    """
    nyq = 0.5 * fs
    low = fc_low / nyq
    high = fc_high / nyq
    b,a = butter( order, [low, high], btype='band')
    return b, a

# ButterworthBP_filterRun(data, fc_low, fc_high, fs ,order=5)
def ButterworthBP_filterRun(data, fc_low, fc_high, fs ,order=5):
    """
    ButterworthBP_filterRun(data, fc_low,fc_high, fs ,order=5):
    
    """
    b, a = ButterworthBP_createKernel(fc_low, fc_high, fs, order=order)
    y = lfilter(b, a, data)
    return y




#
# main
#
if __name__ == "__main__":
    # Smaple frequency
    fs = 5000
    # Lowcut frequency
    fc_low = 500
    # Highcut frequency
    fc_high = 1250

    # Prepare figure
    plt.figure(1)
    
    # Create different order filters
    for order in [3,5,6,9]:
        b,a = ButterworthBP_createKernel(fc_low,fc_high,fs, order =order)
        w,h = freqz(b,a,worN=2000)
        plt.plot((fs*0.5/np.pi)*w, abs(h),label ='order=%d'%order )

    # Plot filters
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Gain')
    plt.grid()
    plt.legend(loc='best')

    #
    #Test Filter
    #

    # Period
    T = 0.05
    # Number of samples
    nsamples = T*fs
    # Time
    t = np.linspace(0,T,int(nsamples))
    # Random amplitude constant
    a = 0.02
    # f0
    f0 = 600
    
    # input signals
    x1 = 0.1 * np.sin(2 * np.pi * 1.2 * np.sqrt(t))
    x2 = 0.01 * np.cos(2 * np.pi * 312 * (t+0.1) )
    x3 = a * np.cos(2 * np.pi * f0 * (t+.11) )
    x4 = 0.03 * np.cos(2 * np.pi * 2000 * t)
    
    # Final input signal
    x = x1 + x2 + x3 + x4
    
    # Plot x in new figure
    plt.figure(2)
    plt.plot(t,x, label='Noisy signal')
    
    # Filter using BP filter order 6
    y = ButterworthBP_filterRun(x,fc_low,fc_high,fs,order=6)
    
    # Plot
    plt.plot(t,y,label ='Filtered signal(%g Hz)'% f0)
    plt.xlabel('time (seconds)')
    plt.hlines([-a,a],0,T,linestyles='--')
    plt.grid()
    plt.axis('tight')
    plt.legend(loc='upper left')
    plt.show()



