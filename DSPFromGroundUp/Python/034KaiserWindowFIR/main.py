#
# Imports
#
from scipy import signal
from matplotlib import pyplot as plt
from matplotlib import style
from numpy import cos, sin,pi,arange,absolute



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
    #sampling rate and number of samples
    sampling_rate = 100
    nsamples = 400
    # time signal
    t = arange(nsamples)/sampling_rate
    # signals
    x1 = cos(2*pi*0.5*t)+0.2*sin(2*pi*2.5*t*0.1)
    x2 = 0.2*sin(2*pi*15.3*t)+0.1*sin(2*pi*16.7*t+0.1)
    x3 = 0.1*sin(2*pi*23.45*t+0.8)
    # final signal
    x= x1+x2+x3

    #
    #Create FIR filter
    #
    # nyquist sampling rate
    nyq_rate = sampling_rate / 2.0  
    # width of transitioin band   
    width = 5.0 / nyq_rate
    # ripple in dB
    ripple_db = 60.0
    # order and kaiser parameter
    N, beta =signal.kaiserord(ripple_db, width)
    # cut frequency in Hz
    fc_hz =10.0
    # Number of taps of the filter
    taps = signal.firwin( 
                        N,                      # Kaiser order
                        (fc_hz / nyq_rate),     # Normalized frequency
                        window=('kaiser', beta) # Kaiser window
                        )
    # FIlter input and save in output
    filtered_x = signal.lfilter(taps, 1.0, x)

    # Plot sinc()
    plt.figure(1)
    plt.plot(taps, 'bo-', linewidth=2)
    plt.title('Filter Coefficients (%d taps)'%N)
    plt.grid()

    # Plot filter freq response
    plt.figure(2)
    w,h = signal.freqz(taps, worN=8000)
    plt.plot((w/pi)*nyq_rate, absolute(h), linewidth=2, color='blue')
    plt.xlabel('Frequency(Hz)')
    plt.ylabel('Gain')
    plt.ylim(-0.05,1.05)
    plt.grid()
    #upper inset plot
    ax1 = plt.axes([0.42,0.6,0.45,0.25])
    plt.plot((w/pi)*nyq_rate,absolute(h), linewidth=2, color='magenta')
    plt.xlim(0,8.0)
    plt.ylim(0.9985,1.001)
    plt.grid()
    #lower inset plot
    ax2 = plt.axes([0.42,0.25,0.45,0.25])
    plt.plot((w/pi)*nyq_rate, absolute(h), linewidth=2, color='magenta')
    plt.xlim(12.0,20.0)
    plt.ylim(0.0,0.0025)
    plt.grid()

    # Plot input signal and filtered signal
    delay = 0.5*(N-1) / sampling_rate
    plt.figure(3)
    plt.plot(t, x)
    plt.plot(t-delay, filtered_x,'r-')
    plt.plot(t[N-1:]-delay, filtered_x[N-1:], 'g', linewidth=4)
    plt.xlabel('t')
    plt.grid()

    # Show figures and plot everything
    plt.show()



