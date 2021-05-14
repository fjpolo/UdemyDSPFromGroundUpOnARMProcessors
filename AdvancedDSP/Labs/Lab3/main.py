"""
1. Upsample the given speech signal (8kHz) to 32 kHz
    Use the .wav-file which is uploaded at moodle in unit „Seminar 4“
    
    a)Upsampling by the factor 4
        Hint: insert 3 zeros after each sample
    b)Plot the spectra of the original and upsampled signal and compare
        Hint: use freqz(…) for creating the spectrum
    c)Listen to both signals
        Hint: use wavwrite(...)

2. FIR lowpass filtering
    a)Implement the FIR lowpass filter with the following difference equation:
    b)Plot the impulse response (first 50 samples)
    c)Plot the frequency response
    d)Filter the upsampled speech signal with the given FIR filter
        Hint: use filter(...)

3. IIR lowpass filtering
    a)Implement the IIR lowpass filter with the following difference equation:
    b)Plot the impulse response (first 50 samples)
    c)Plot the frequency response
    d)Filter the upsampled speech signal with the given IIR filter
        Hint: use filter(...)

4. Downsampling
    a)Filter the given speech signal (8kHz) with the given IIR filter
    b)Downsample the signal by the factor 2
        Hint: means taking every second speech sample
    c)Plot the spectra of the original and downsampled signal and compare
        Hint: use freqz(…) for creating the spectrum
    d)Listen to both signals
        Hint: use wavwrite(...)

5. Noble Identities
    a)Reverse the order of upsampling and filtering according to the Noble Identities (only for FIR case)
    b)Compare the resulting signals (plot and listen)

6. Compare FIR and IIR lowpass filters:
    - Transfer functions
    - Signals after upsampling and filtering
    - Listen to signals before and after lowpass filtering (aliasing)
    - Make your own conclusions about comparison
    - Which filter is better? Why?
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

# Task1
def Task1():
    """
    Lab3 Task 1.-
    """
    print("Lab 3 Task 1:")

    # a.play()
    # a.close()
    speech_8kHz = a.extract()

    # Upsample
    N = int(32/8)
    speech_32kHz = np.zeros(int(32/8) * len(speech_8kHz))
    speech_32kHz[::N] = speech_8kHz
    # print(len(speech_8kHz))
    # print(len(speech_32kHz))

    # Play
    sd.play(speech_8kHz, 8000)
    time.sleep(10)
    sd.play(speech_32kHz, 32000)
    time.sleep(10)

    # Plot time
    style.use("dark_background")
    fig, pltArr = plt.subplots(2, sharex=True) 
    fig.suptitle("Speech signals")
    pltArr[0].plot(speech_8kHz, color='red')
    pltArr[0].set_title("8kHz Signal")
    pltArr[1].plot(speech_32kHz, color='red')
    pltArr[1].set_title("32kHz Signal")

    # Frequency Response
    fig, pltArr = plt.subplots(2, sharex=True) 
    fig.suptitle("Speech signals - Frequency Response")
    [freq, response] = scipy.signal.freqz(speech_8kHz)
    pltArr[0].plot(freq, np.log10(np.abs(response)), color='red')
    pltArr[0].set_title("8kHz Signal")
    [freq, response] = scipy.signal.freqz(speech_32kHz)
    pltArr[1].plot(freq, np.log10(np.abs(response)), color='red')
    pltArr[1].set_title("32kHz Signal")

    #
    plt.show()

# Task2
def Task2():
    """
    Lab3 Task 2.-
    """
    print("Lab 3 Task 2:")  

    

    # LP FIR
    B = [0.3235, 0.2665, 0.2940, 0.2655, 0.3235]
    A = [1]

    # Impulse
    impulse = np.zeros(50)
    impulse[0] = 1

    # Filter
    impulseResponse = signal.lfilter(B, A, impulse)

    # Plot impulse and Impulse response
    style.use("dark_background")
    fig, pltArr = plt.subplots(2, sharex=True) 
    fig.suptitle("FIR Filter")
    pltArr[0].plot(impulse, color='red')
    pltArr[0].set_title("Impulse Signal")
    pltArr[1].plot(impulseResponse, color='red')
    pltArr[1].set_title("impulse Response Signal")
    # Frequency response
    fig = plt.figure()
    [freq, response] = scipy.signal.freqz(impulseResponse)
    plt.plot(freq, np.log10(np.abs(response)))
    plt.xlabel('Normalized Frequency (pi is Nyquist Frequency)')
    plt.ylabel("Magnitude of Frequency Response")
    plt.title("Magnitude of Frequency Response for impulse response") 
    #
    # plt.show()

    #
    # Filter speech
    #

    # Audio
    speech_8kHz = a.extract()
    # Upsample
    N = int(32/8)
    speech_32kHz = np.zeros(int(32/8) * len(speech_8kHz))
    speech_32kHz[::N] = speech_8kHz

    # Filter
    output = signal.lfilter(B, A, speech_32kHz)
    # sd.play(output, 32000)  
    # time.sleep(10)

    # Plot input and output
    style.use("dark_background")
    fig, pltArr = plt.subplots(2, sharex=True) 
    fig.suptitle("FIR Filter")
    pltArr[0].plot(speech_8kHz, color='red')
    pltArr[0].set_title("Original 8kHz Signal")
    pltArr[1].plot(output, color='red')
    pltArr[1].set_title("Output Response Signal")
    # Frequency response input
    fig = plt.figure()
    [freq, response] = scipy.signal.freqz(speech_8kHz)
    plt.plot(freq, np.log10(np.abs(response)))
    plt.xlabel('Normalized Frequency (pi is Nyquist Frequency)')
    plt.ylabel("Magnitude of Frequency Response")
    plt.title("Magnitude of Frequency Response - Input")
    # Frequency response output
    fig = plt.figure()
    [freq, response] = scipy.signal.freqz(output)
    plt.plot(freq, np.log10(np.abs(response)))
    plt.xlabel('Normalized Frequency (pi is Nyquist Frequency)')
    plt.ylabel("Magnitude of Frequency Response")
    plt.title("Magnitude of Frequency Response - Ouput") 
    #
    plt.show()

# Task3
def Task3():
    """
    Lab3 Task 3.-
    """
    print("Lab 3 Task 3:")  


    # IIR LP FIlter
    A = [1, -1.3547, 0.6125]
    B = [0.256, 0.0512, 0.256]

    # Impulse
    impulse = np.zeros(50)
    impulse[0] = 1

    # Filter
    impulseResponse = signal.lfilter(B, A, impulse)

    # Plot impulse and Impulse response
    style.use("dark_background")
    fig, pltArr = plt.subplots(2, sharex=True) 
    fig.suptitle("IIR Filter")
    pltArr[0].plot(impulse, color='red')
    pltArr[0].set_title("Impulse Signal")
    pltArr[1].plot(impulseResponse, color='red')
    pltArr[1].set_title("impulse Response Signal")
    # Frequency response
    fig = plt.figure()
    [freq, response] = scipy.signal.freqz(impulseResponse)
    plt.plot(freq, np.log10(np.abs(response)))
    plt.xlabel('Normalized Frequency (pi is Nyquist Frequency)')
    plt.ylabel("Magnitude of Frequency Response")
    plt.title("Magnitude of Frequency Response for impulse response") 
    #
    # plt.show()

    #
    # Filter speech
    #

    # Audio
    speech_8kHz = a.extract()
    
    # Upsample
    N = int(32/8)
    speech_32kHz = np.zeros(int(32/8) * len(speech_8kHz))
    speech_32kHz[::N] = speech_8kHz

    # Filter
    output = signal.lfilter(B, A, speech_32kHz)
    # sd.play(output, 32000)  
    # time.sleep(10)

    # Plot input and output
    style.use("dark_background")
    fig, pltArr = plt.subplots(2, sharex=True) 
    fig.suptitle("FIR Filter")
    pltArr[0].plot(speech_32kHz, color='red')
    pltArr[0].set_title("Input Signal")
    pltArr[1].plot(output, color='red')
    pltArr[1].set_title("Output Response Signal")
    # Frequency response input
    fig = plt.figure()
    [freq, response] = scipy.signal.freqz(speech_32kHz)
    plt.plot(freq, np.log10(np.abs(response)))
    plt.xlabel('Normalized Frequency (pi is Nyquist Frequency)')
    plt.ylabel("Magnitude of Frequency Response")
    plt.title("Magnitude of Frequency Response - Input")
    # Frequency response output
    fig = plt.figure()
    [freq, response] = scipy.signal.freqz(output)
    plt.plot(freq, np.log10(np.abs(response)))
    plt.xlabel('Normalized Frequency (pi is Nyquist Frequency)')
    plt.ylabel("Magnitude of Frequency Response")
    plt.title("Magnitude of Frequency Response - Ouput") 
    #
    plt.show()

# Task4
def Task4():
    """
    Lab3 Task 4.-
    """
    print("Lab 3 Task 4:") 


    # IIR LP FIlter
    A = [1, -1.3547, 0.6125]
    B = [0.256, 0.0512, 0.256]

    # Impulse
    impulse = np.zeros(50)
    impulse[0] = 1

    # IMpulse response
    impulseResponse = signal.lfilter(B, A, impulse)

    # Audio
    speech_8kHz = a.extract()
    
    # Upsample
    N = int(32/8)
    speech_32kHz = np.zeros(int(32/8) * len(speech_8kHz))
    speech_32kHz[::N] = speech_8kHz

    # Filter
    output = signal.lfilter(B, A, speech_32kHz)

    # Downsample
    speech_32kHz_reconstructed = output[::2]
    # sd.play(speech_32kHz_reconstructed, 16000)  
    # time.sleep(10)



    # Plot input and output
    style.use("dark_background")
    fig, pltArr = plt.subplots(2, sharex=True) 
    fig.suptitle("IIR Filter")
    pltArr[0].plot(speech_8kHz, color='red')
    pltArr[0].set_title("Original 8kHz Signal")
    pltArr[1].plot(speech_32kHz_reconstructed, color='red')
    pltArr[1].set_title("Reconstructed 8kHz Signal")
    # Frequency response input
    fig = plt.figure()
    [freq, response] = scipy.signal.freqz(speech_8kHz)
    plt.plot(freq, np.log10(np.abs(response)))
    plt.xlabel('Normalized Frequency (pi is Nyquist Frequency)')
    plt.ylabel("Magnitude of Frequency Response")
    plt.title("Magnitude of Frequency Response - Input")
    # Frequency response output
    fig = plt.figure()
    [freq, response] = scipy.signal.freqz(speech_32kHz_reconstructed)
    plt.plot(freq, np.log10(np.abs(response)))
    plt.xlabel('Normalized Frequency (pi is Nyquist Frequency)')
    plt.ylabel("Magnitude of Frequency Response")
    plt.title("Magnitude of Frequency Response - Ouput") 
    #
    plt.show()

# Task5
def Task5():
    """
    Lab3 Task 5.-
    """
    print("Lab 3 Task 5:") 


    # FIR LP FIlter
    B = [0.3235, 0.2665, 0.2940, 0.2655, 0.3235]
    A = [1]

    # Impulse
    impulse = np.zeros(50)
    impulse[0] = 1

    # IMpulse response
    impulseResponse = signal.lfilter(B, A, impulse)

    # Audio
    speech_8kHz = a.extract()
    
    # Filter
    output = signal.lfilter(B, A, speech_8kHz)
    
    # Upsample
    N = int(32/8)
    speech_32kHz = np.zeros(int(32/8) * len(output))
    speech_32kHz[::N] = output

    
    # Downsample
    speech_32kHz_reconstructed = output[::2]
    # sd.play(speech_32kHz_reconstructed, 16000)  
    # time.sleep(10)


    # Plot input and output
    style.use("dark_background")
    fig, pltArr = plt.subplots(2, sharex=True) 
    fig.suptitle("FIR Filter")
    pltArr[0].plot(speech_8kHz, color='red')
    pltArr[0].set_title("Original 8kHz Signal")
    pltArr[1].plot(speech_32kHz_reconstructed, color='red')
    pltArr[1].set_title("Reconstructed 8kHz Signal")
    # Frequency response input
    fig = plt.figure()
    [freq, response] = scipy.signal.freqz(speech_8kHz)
    plt.plot(freq, np.log10(np.abs(response)))
    plt.xlabel('Normalized Frequency (pi is Nyquist Frequency)')
    plt.ylabel("Magnitude of Frequency Response")
    plt.title("Magnitude of Frequency Response - Input")
    # Frequency response output
    fig = plt.figure()
    [freq, response] = scipy.signal.freqz(speech_32kHz_reconstructed)
    plt.plot(freq, np.log10(np.abs(response)))
    plt.xlabel('Normalized Frequency (pi is Nyquist Frequency)')
    plt.ylabel("Magnitude of Frequency Response")
    plt.title("Magnitude of Frequency Response - Ouput") 
    #
    plt.show()

#
# main
#
if __name__ == "__main__":
        Task1()
        Task2()
        Task3()
        Task4()
        Task5()