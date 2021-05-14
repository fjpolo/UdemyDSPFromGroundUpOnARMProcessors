"""
1. Upsample the speech signal by the factor of N = 4, using Noble identities (polyphase decomposition)

2. Design filter for the anti-alias-filtering
    –FIR with 32 filter coefficients
    –Use: Parks-McClellan-Algorithm (remez filter design function)
    –Plot impulse and frequency response
        • Reasonable filter design, i.e. consider:
        • passband, stopband, transition band
        • stopband attenuation
        • weights
        • normalization of frequency
        • stopband should start where aliasing components appear

3.Listen to and compare signals before and after upsampling and filtering

4.Design a frequency warped filter with the following parameters:
    –Sampling frequency: 44.1 kHz
    –Cutoff frequency: 0.15*pi
    –No. of filter coefficients: 6

5. Plot the filter‘s:
    a)impulse response
    b)frequency response
    c)z-plane (poles,zeroes)

6. Implement the minimum phase version of a linear phase filter
    –Create a FIR filter with the help of remez() function with the passband of 0,25
    –Make the minimum phase version out of it

7. Plot the minimum phase filter‘s:
    a) impulse response
    b) frequency response
    c) z-plane
"""


#
# Imports
#
from scipy import signal
from matplotlib import pyplot as plt
from matplotlib import style
from scipy import signal
import numpy as np
import wave
import sys
import pyaudio
import math
import scipy
# from sound import sound
import sounddevice as sd
import time
from warpingphase import *
from zplane import *


CHUNK = 75 * 1024



#
# Classes
#
class AudioFile:
    chunk = CHUNK
    def __init__(self, file):
        """ Init audio stream """ 
        self.wf = wave.open(file, 'rb')
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(
            format = self.p.get_format_from_width(self.wf.getsampwidth()),
            channels = self.wf.getnchannels(),
            rate = self.wf.getframerate(),
            output = True
        )

    def play(self):
        """ Play entire file """
        data = self.wf.readframes(self.chunk)
        while data != '':
            self.stream.write(data)
            data = self.wf.readframes(self.chunk)

    def close(self):
        """ Graceful shutdown """ 
        self.stream.close()
        self.p.terminate()

    def extract(self):
        signal = self.wf.readframes(self.chunk)
        signal = np.fromstring(signal, "Int16")
        return signal

#
# Global variables
#

# Audio
# open the file for reading.
audioPath = "AdvancedDSP\Labs\Lab3\speech8kHz.wav"
a = AudioFile(audioPath)


#
# Private functions
#

# SNR
def SNR(signal, error):
    return 10 * np.log10(abs(np.var(signal) / np.var(error)))


#
# Private Tasks
#

#Task123
def Task123():
    """
    Lab4 Tasks 1, 2 and 3.-
    """
    print("Lab 4 Tasks 1, 2 and 3:")

    #
    # Task 1 - Upsample and analyze Frequency Response
    #


    # Audio
    speech_8kHz = a.extract()
    # Upsample
    upN = int(32/8)
    speech_32kHz = np.zeros(int(32/8) * len(speech_8kHz))
    speech_32kHz[::upN] = speech_8kHz

    # Plot 
    style.use("dark_background")
    fig, pltArr = plt.subplots(2, sharex=True) 
    fig.suptitle("FIR Filter")
    pltArr[0].plot(speech_8kHz, color='red')
    pltArr[0].set_title("Original Signal")
    pltArr[1].plot(speech_32kHz, color='red')
    pltArr[1].set_title("Upsampled Signal")
    # Plot frequency response input
    fig = plt.figure()
    [freq, response] = scipy.signal.freqz(speech_8kHz)
    plt.plot(freq, np.abs(response))
    plt.xlabel('Normalized Frequency (pi is Nyquist Frequency)')
    plt.ylabel("Magnitude of Frequency Response")
    plt.title("Magnitude of Frequency Response for our Bandbass Filter")
    # Plot frequency response Output
    fig = plt.figure()
    [freq, response] = scipy.signal.freqz(speech_32kHz)
    plt.plot(freq, np.abs(response))
    plt.xlabel('Normalized Frequency (pi is Nyquist Frequency)')
    plt.ylabel("Magnitude of Frequency Response")
    plt.title("Magnitude of Frequency Response for our Bandbass Filter") 
    #
    plt.show()



    #
    # Task 2 - Filter
    #

    # @0.78fs starts aliasing, 

    # fs
    fs = 32000
    # fc = 0.78 * fs
    fc = 12800
    # Transition band width in Hz
    trans_width = 500
    # Design Filter - LowPass fc @ 0.4
    FIR_N = 32
    # Band edges for passs, transition and stop
    FIR_Fbands = [0, fc, fc + trans_width, 0.5*fs]
    # Amplitude at given edges
    FIR_Abands = [1, 0]
    # Taps
    LowPass_Filter = signal.remez(FIR_N, bands=FIR_Fbands, desired=[1, 0], Hz=fs)

    # Impulse
    impulse = np.zeros(50)
    impulse[0] = 1

    # Filter
    impulseResponse = signal.lfilter(LowPass_Filter, [1], impulse)

    # Plot impulse and Impulse response
    style.use("dark_background")
    fig, pltArr = plt.subplots(2, sharex=True) 
    fig.suptitle("FIR Filter")
    pltArr[0].plot(impulse, color='red')
    pltArr[0].set_title("Impulse Signal")
    pltArr[1].plot(impulseResponse, color='red')
    pltArr[1].set_title("impulse Response Signal")

    # Plot frequency response      
    fig = plt.figure()
    [freq, response] = scipy.signal.freqz(LowPass_Filter)
    plt.plot(freq, np.abs(response))
    plt.xlabel('Normalized Frequency (pi is Nyquist Frequency)')
    plt.ylabel("Magnitude of Frequency Response")
    plt.title("Magnitude of Frequency Response for our Bandbass Filter") 
    #
    plt.show()

    # Filter upsampled signal
    speech_32kHz_filtered = signal.lfilter(LowPass_Filter, [1], speech_32kHz)

    # Downsample
    speech_32kHz_reconstructed = speech_32kHz_filtered[::4]
    # sd.play(speech_32kHz_reconstructed, 8000)  
    # time.sleep(10)

    # Plot 
    style.use("dark_background")
    fig, pltArr = plt.subplots(2, sharex=True) 
    fig.suptitle("FIR Filter")
    pltArr[0].plot(speech_8kHz, color='red')
    pltArr[0].set_title("Original Signal")
    pltArr[1].plot(speech_32kHz_reconstructed, color='red')
    pltArr[1].set_title("Up-Filtered-Dn Signal")
    # Plot frequency response input
    fig = plt.figure()
    [freq, response] = scipy.signal.freqz(speech_8kHz)
    plt.plot(freq, np.abs(response))
    plt.xlabel('Normalized Frequency (pi is Nyquist Frequency)')
    plt.ylabel("Magnitude of Frequency Response")
    plt.title("Magnitude of Frequency Response for our Bandbass Filter")
    # Plot frequency response Output
    fig = plt.figure()
    [freq, response] = scipy.signal.freqz(speech_32kHz_reconstructed)
    plt.plot(freq, np.abs(response))
    plt.xlabel('Normalized Frequency (pi is Nyquist Frequency)')
    plt.ylabel("Magnitude of Frequency Response")
    plt.title("Magnitude of Frequency Response for our Bandbass Filter") 
    #
    plt.show()

#Task4
def Task45():
    """
    Lab4 Task 4.-
    """
    print("Lab 4 Tasks 4 and 5:") 

    # fs
    fs_kHz = 44.1
    # fc
    fc = 0.15
    # Number of coefficients
    Ntaps = 6

    # Warping allpass coefficient:
    a = 1.0674 * (2 / np.pi * np.arctan(0.6583 * fs_kHz)) ** 0.5 - 0.1916

    # with fs_kHz=44.1kHz:
    # The warped cutoff frequency then is:
    fcw = -warpingphase(0.05 * np.pi, a)
    # print(fcw)  # 1.6467445101361733

    # fcw = 1.6467445101361733 in radiants

    # filter design:
    # cutoff frequency normalized to nyquist:
    fcny=fcw/np.pi
    c = signal.remez(4, [0, (fcny/2.0), (fcny/2.0 + 0.1), 0.5], [1, 0],[1, 100])

    #The resulting Impulse Response:
    plt.plot(c)
    plt.xlabel('Sample')
    plt.ylabel('value')
    plt.title('Filter Coefficients in Warped Domain')
    # Frequency response
    fig = plt.figure()
    [freq, response] = signal.freqz(c,1)
    plt.plot(freq, np.log10(np.abs(response)))
    plt.xlabel('Normalized Frequency (pi is Nyquist Frequency)')
    plt.ylabel("Magnitude of Frequency Response")
    plt.title("Magnitude of Frequency Response - Ouput") 
    #
    plt.show()


    # Warping Allpass filters:
    #Numerrator:
    B = [-a.conjugate(), 1]
    #Denominator:
    A = [1, -a]
    # Impulse with 80 zeros:
    Imp = np.zeros(80)
    Imp[0] = 1
    x = Imp

    # Y1(z)=A(z), Y2(z)=A^2(z),...
    # Warped delays:
    y1 = signal.lfilter(B,A,x)
    y2 = signal.lfilter(B,A,y1)
    y3 = signal.lfilter(B,A,y2)

    # Output of warped filter with impulse as input:
    yout = c[0]*x+c[1]*y1+c[2]*y2+c[3]*y3

    #
    signal.freqz(yout, 1)

    #Impulse response:
    plt.plot(yout)
    plt.xlabel('Sample')
    plt.ylabel('value')
    plt.title('Impulse Response of Warped Lowpass Filter')
    # Frequency response
    fig = plt.figure()
    [freq, response] = signal.freqz(yout, 1)
    plt.plot(freq, np.log10(np.abs(response)))
    plt.xlabel('Normalized Frequency (pi is Nyquist Frequency)')
    plt.ylabel("Magnitude of Frequency Response")
    plt.title("Magnitude of Frequency Response - Ouput") 
    #
    plt.show()



    # Z
    zplane(np.roots(yout), 0, [-1.1, 2.1, -1.1, 1.1])
    np.abs(np.roots(yout))
    rt = np.roots(yout)
    [b, r] = signal.deconvolve(yout, [1,-rt[1]])	
    hsincmp = signal.convolve(b,[1,-1/rt[1].conjugate()])

#Task67
def Task67():
    """
    Lab4 Tasks 6 and 7.-
    """
    print("Lab 4 Tasks 6 and 7:") 


    # Low-pass filter design parameters
    Ntaps=16
    Fbands=[0, 0.15, 0.2, 0.25, 0.3, 0.5]
    Abands=[0, 1, 0]
    Weights= [100, 1, 100]
    #
    BPtaps = signal.remez(Ntaps, Fbands, Abands, Weights)
    #
    fig = plt.figure()
    plt.plot(BPtaps)
    plt.xlabel('Sample')
    plt.ylabel('Value')
    plt.title('Impulse Response of the FIR Filter')
    # Frequency response
    fig, pltArr = plt.subplots(2, sharex=True) 
    fig.suptitle("Frequency Response")
    [freq, response] = signal.freqz(BPtaps, [1], worN=2000)
    pltArr[0].plot(freq, np.log10(np.abs(response)))
    pltArr[0].set_title("Magnitude of Frequency Reponse")
    angles = np.unwrap(np.angle(response))
    pltArr[1].plot(freq, angles)
    pltArr[1].set_title("Angle of Frequency Reponse")
    # plt.xlabel('Normalized Frequency (pi is Nyquist Frequency)')
    # plt.ylabel("Magnitude of Frequency Response")
    # plt.title("Magnitude of Frequency Response")


    # Minimum phase version
    rt = np.roots(BPtaps)
    [b, r] = signal.deconvolve(BPtaps, [1,-rt[1]])
    MinPhTaps = signal.convolve(b,[1,-1/rt[1].conjugate()])

    #impulse response
    fig = plt.figure()
    plt.plot(MinPhTaps)
    plt.xlabel('Sample')
    plt.ylabel('Value')
    plt.title('Impulse Response of the Minimum Phase Filter')
    # Frequency response
    fig, pltArr = plt.subplots(2, sharex=True) 
    fig.suptitle("Frequency Response")
    [freq, response] = signal.freqz(MinPhTaps, [1], worN=2000)
    pltArr[0].plot(freq, np.log10(np.abs(response)))
    pltArr[0].set_title("Magnitude of Frequency Reponse")
    angles = np.unwrap(np.angle(response))
    pltArr[1].plot(freq, angles)
    pltArr[1].set_title("Angle of Frequency Reponse")
    # plt.xlabel('Normalized Frequency (pi is Nyquist Frequency)')
    # plt.ylabel("Magnitude of Frequency Response")
    # plt.title("Magnitude of Frequency Response")
    #
    plt.show()




#
# main
#
if __name__ == "__main__":
    Task123()
    Task45()
    Task67()