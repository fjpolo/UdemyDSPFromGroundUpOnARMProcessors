#
# Imports
#
from scipy import signal
from matplotlib import pyplot as plt
from matplotlib import style
import numpy as np

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
    original_signal = np.repeat([0.,1.,1.,0.,1.,0.,0.,1.],128)
    noise  =np.random.randn(len(original_signal))
    noisy_signal = original_signal + noise
    rectangular_pulse  =  np.ones(128)
    correlated_output = signal.correlate(noisy_signal,rectangular_pulse, mode='same')
    clock = np.arange(64, len(original_signal), 128)

    #plot
    fig,(ax_orig,ax_noise,ax_corr) = plt.subplots(3,1,sharex=True)
    ax_orig.plot(original_signal)
    ax_orig.plot(clock,original_signal[clock],'ro')
    ax_noise.plot(noisy_signal)
    ax_corr.plot(correlated_output)
    ax_corr.plot(clock, correlated_output[clock],'ro')
    ax_orig.margins(0,0.1)
    fig.tight_layout()
    fig.show()
    plt.show()
