"""
1.Hilbert transform
    We would like to determine the instantaneous amplitude of a speech signal.
    •read in a speech signal (use the one from Homework 3 or 4)
    •attenuate its negative frequencies using a Hilbert transformer with an impulse response length of 40 samples
    •plot the resulting spectrum on the whole axis (from 0 to 2pi). How much are the negative frequencies attenuated?
    •using this analytic signal, compute its instantaneous magnitude
    •plot the original speech signal and its instantaneous amplitude in one time plot.

2. Wiener Filter
    We would like to reduce the noise in a speech signal.
    •read in a speech signal
    •add uniform white noise with amplitude of 5% of the max. amplitude of the speech signal
    •compute the resulting Signal to Noise Ratio (SNR) in dB
    •compute a Wiener filter with 14 coefficients
    •plot the resulting magnitude response
    •filter the noisy signal with the Wiener Filter
    •compute the resulting SNR in dB
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


#
# Private Tasks
#

#Task1
def Task1():
    """
    Lab5 Task 1.-
    """
    print("Lab 5 Task 1:")

    # Audio
    speech_8kHz = a.extract()

    # Hilbert
    HilbertTransform = signal.remez(41, [0.03, 0.47],[1], type='hilbert')

    # Frequency response
    fig, pltArr = plt.subplots(2, sharex=True) 
    fig.suptitle("Frequency Response HilbertTransform")
    [freq, response] = scipy.signal.freqz(HilbertTransform)
    pltArr[0].plot(freq, np.log10(np.abs(response)))
    pltArr[0].set_title("Magnitude of Frequency Reponse")
    angles = np.unwrap(np.angle(response))
    pltArr[1].plot(freq, angles)
    pltArr[1].set_title("Angle of Frequency Reponse")


    # Filter using Hilbert transform
    speech_8kHz_filtered = signal.lfilter(HilbertTransform, [1], speech_8kHz)

    # Frequency response INput
    fig, pltArr = plt.subplots(2, sharex=True) 
    fig.suptitle("Frequency Response speech_8kHz")
    [freq, response] = scipy.signal.freqz(speech_8kHz)
    pltArr[0].plot(freq, np.log10(np.abs(response)))
    pltArr[0].set_title("Magnitude of Frequency Reponse")
    angles = np.unwrap(np.angle(response))
    pltArr[1].plot(freq, angles)
    pltArr[1].set_title("Angle of Frequency Reponse")
    # Frequency response t
    fig, pltArr = plt.subplots(2, sharex=True) 
    fig.suptitle("Frequency Response speech_8kHz_filtered")
    [freq, response] = scipy.signal.freqz(speech_8kHz_filtered)
    pltArr[0].plot(freq, np.log10(np.abs(response)))
    pltArr[0].set_title("Magnitude of Frequency Reponse")
    angles = np.unwrap(np.angle(response))
    pltArr[1].plot(freq, angles)
    pltArr[1].set_title("Angle of Frequency Reponse")


    #
    plt.show()

#Task2
def Task2():
    """
    Lab5 Task 2.-
    """
    print("Lab 5 Task 2:")


#
# main
#
if __name__ == "__main__":
    # Task1()
    Task2()