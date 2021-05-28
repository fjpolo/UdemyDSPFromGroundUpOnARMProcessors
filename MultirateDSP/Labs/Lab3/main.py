"""
1. Read in two different audio signals
    • Speech signal
    • Music signal
        -> Downsample and upsample both signals with the factor N=2

2. For that purpose design a low pass filter using the window method
    • Use window length of L=16
    • Determine where the stopband should start

3.Plot the frequency response:
    •Music/Speech signals
    •Filter
    •Downsampled and filtered music/speech signal (Show here the entire spectrum from 0 to 2pi; Matlab: usefreqz(low_dwn,1,128, 'whole') )
    •Reconstructed music/speech signal

4. Design a highpass filter out of the lowpass filter
    •Repeat the downsampling/upsampling process with this filter
    •Repeat Task 3 (plots)
5. Analyzeandcompare
    •Howdoesthespectrumofthesignalchangeafter filteringanddownsampling?
    •Howdoesthereconstructedspeech/musicsoundsin thecaseofthelowpassandhighpassfilter? Whatarethedifferences?
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
import time
import sounddevice as sd
import soundfile as sf
# import sound
import scipy
# from Freqz import freqz

#
# Global variables
#
CHUNK = 1024
# Frequencies
f_sine = 440
f_triangle = 440
Fs = f_sine / 0.1

# Time
t = np.linspace(0, 1, int(Fs))

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
# Private functions
#

# SNR
def SNR(signal, error):
    return 10 * np.log10(abs(np.var(signal) / np.var(error)))

# Plot PlotFreqResponse
def PlotFreqResponse(x, title):
    #
    # Plot fequency response
    #
    # fig = plt.figure()
    [freq, response] = signal.freqz(x)
    fig, pltArr = plt.subplots(2, sharex=True) 
    fig.suptitle(title)
    #Magnitude
    pltArr[0].plot((freq/math.pi), 20 * np.log10(np.abs(response)))
    pltArr[0].set_title("Magnitude of Frequency Response")
    pltArr[0].set_xlabel('Normalized Frequency (xPi [rad/sample])')
    pltArr[0].set_ylabel("Magnitude [dB]")
    # Phase
    angles = np.unwrap(np.angle(response))
    pltArr[1].plot((freq/math.pi), angles)
    pltArr[1].set_title("Phase of Frequency Response")
    pltArr[1].set_xlabel('Normalized Frequency (xPi [rad/sample])')
    pltArr[1].set_ylabel("Angle [xPi [rad/sample]]")

    


#
# Private Tasks
#

# Task1
def Task123():
    """
    Lab2 Task 1, 2 and 3.-
    """
    print("Lab 2 Task 1, 2 and 3:")
    
    # 
    # Signals
    #
    
    # Speech
    SpeechPath = "MultirateDSP\Labs\Lab3\speech8kHz.wav"
    SpeechSignalFullRange, fs_Speech = sf.read(SpeechPath, dtype='float32')
    # sd.play(SpeechSignalFullRange, fs_Speech)
    # sd.wait()
    print("     Speech fs: ", fs_Speech)

    # Music
    MusicPath = "MultirateDSP\Labs\Lab3\ImperialMarch_12.wav"
    MusicSignalFullRange_Stereo, fs_Music = sf.read(MusicPath, dtype='float32')  # Stereo
    MusicSignalFullRange = [s[0] for s in MusicSignalFullRange_Stereo]            # Mono
    print("     Music fs: ", fs_Music)

    # sd.play(MusicSignalFullRange, fs_Music)
    # sd.wait()

    #
    # Plot Full range signals
    #
    style.use("dark_background")
    fig, pltArr = plt.subplots(2, sharex=True) 
    fig.suptitle("Signals")
    pltArr[0].plot(SpeechSignalFullRange, color='red')
    pltArr[0].set_title("Speech Signal")
    pltArr[1].plot(MusicSignalFullRange, color='red')
    pltArr[1].set_title("Music Signal")

    # Plot fequency response - Speech
    PlotFreqResponse(SpeechSignalFullRange, "Frequency Response Speech")
    # Plot fequency response - Music
    PlotFreqResponse(MusicSignalFullRange, "Frequency Response Music")



    #
    # Downsample
    #
    SpeechSignalFullRange_Dn2 = SpeechSignalFullRange[::2]
    MusicSignalFullRange_Dn2 = MusicSignalFullRange[::2]

    # Plot fequency response - Speech
    PlotFreqResponse(SpeechSignalFullRange_Dn2, "Frequency Response Downsampled N=2 Speech")
    # Plot fequency response - Music
    PlotFreqResponse(MusicSignalFullRange_Dn2, "Frequency Response Downsampled N=2 Music")


    #
    # Filter LP Windowed
    #
    # n = np.arange(16)
    # h = np.sin(0.14*np.pi*(n-7.5))/(np.pi*(n-7.5))
    # h = np.ones(16)   
    # hk = np.sin(0.5*np.pi*(n-7.5))/(np.pi*(n-7.5))                 # Sinc
    # hk = 0.5-0.5*np.cos(2*np.pi/16*(np.arange(16)+0.5))            # Hanning
    # hk = np.sin(np.pi/16*(np.arange(16)+0.5))                      # Sine window     
    # hk = np.kaiser(16,8)                                           # Kaiser                      
    # hk = np.sin(np.pi/2*np.sin(np.pi/16*(np.arange(16)+0.5))**2)   # Vorbis
    # hfilt = hk * h
    LP_L = 16
    LP_delay = (LP_L -1)/2.0
    LP_fc = 0.5
    LP_fstop = LP_fc - 0.1 
    n = np.arange(16)
    h = np.sin(LP_fstop*np.pi*(n-LP_delay))/(np.pi*(n-LP_delay))
    hk = np.kaiser(16,8)
    hfilt = hk * h
    PlotFreqResponse(hfilt, "Frequency Response from hfilt")

    #
    # Upsample
    #
    SpeechSignalFullRange_Dn2_Up2 = np.zeros(2 * len(SpeechSignalFullRange_Dn2))
    SpeechSignalFullRange_Dn2_Up2[::2] = SpeechSignalFullRange_Dn2
    MusicSignalFullRange_Dn2_Up2 = np.zeros(2 * len(MusicSignalFullRange_Dn2))
    MusicSignalFullRange_Dn2_Up2[::2] = MusicSignalFullRange_Dn2

    # Plot fequency response - Speech
    PlotFreqResponse(SpeechSignalFullRange_Dn2_Up2, "Frequency Response - Speech Downsampled Upsampled")
    # Plot fequency response - Music
    PlotFreqResponse(MusicSignalFullRange_Dn2_Up2, "Frequency Response - Music Downsampled Upsampled")


    #
    # Filter
    #
    
    #Speech
    SpeechSignalFullRange_Dn2_Up2_Filt = signal.lfilter(hfilt, [1], SpeechSignalFullRange_Dn2_Up2)
    #Music
    MusicSignalFullRange_Dn2_Up2_Filt = signal.lfilter(hfilt, [1], MusicSignalFullRange_Dn2_Up2)

    #
    PlotFreqResponse(SpeechSignalFullRange_Dn2_Up2_Filt, "Frequency Response - Speech Downsampled Upsampled Filtered")
    PlotFreqResponse(MusicSignalFullRange_Dn2_Up2_Filt, "Frequency Response - Music Downsampled Upsampled Filtered")



    #Show plot
    plt.show()

    # #
    # # Play
    # #
    # sd.play(SpeechSignalFullRange_Dn2_Up2_Filt, fs_Speech)
    # sd.wait()
    # sd.play(MusicSignalFullRange_Dn2_Up2_Filt, fs_Music)
    # sd.wait()


# Task4
def Task4():
    """
    Lab2 Task 4.-
    """
    print("Lab 2 Task 4:")
    
    # 
    # Signals
    #
    
    # Speech
    SpeechPath = "MultirateDSP\Labs\Lab3\speech8kHz.wav"
    SpeechSignalFullRange, fs_Speech = sf.read(SpeechPath, dtype='float32')
    # sd.play(SpeechSignalFullRange, fs_Speech)
    # sd.wait()
    print("     Speech fs: ", fs_Speech)

    # Music
    MusicPath = "MultirateDSP\Labs\Lab3\ImperialMarch_12.wav"
    MusicSignalFullRange_Stereo, fs_Music = sf.read(MusicPath, dtype='float32')  # Stereo
    MusicSignalFullRange = [s[0] for s in MusicSignalFullRange_Stereo]            # Mono
    print("     Music fs: ", fs_Music)

    # sd.play(MusicSignalFullRange, fs_Music)
    # sd.wait()

    #
    # Plot Full range signals
    #
    style.use("dark_background")
    fig, pltArr = plt.subplots(2, sharex=True) 
    fig.suptitle("Signals")
    pltArr[0].plot(SpeechSignalFullRange, color='red')
    pltArr[0].set_title("Speech Signal")
    pltArr[1].plot(MusicSignalFullRange, color='red')
    pltArr[1].set_title("Music Signal")

    # Plot fequency response - Speech
    PlotFreqResponse(SpeechSignalFullRange, "Frequency Response Speech")
    # Plot fequency response - Music
    PlotFreqResponse(MusicSignalFullRange, "Frequency Response Music")



    #
    # Downsample
    #
    SpeechSignalFullRange_Dn2 = SpeechSignalFullRange[::2]
    MusicSignalFullRange_Dn2 = MusicSignalFullRange[::2]

    # Plot fequency response - Speech
    PlotFreqResponse(SpeechSignalFullRange_Dn2, "Frequency Response Downsampled N=2 Speech")
    # Plot fequency response - Music
    PlotFreqResponse(MusicSignalFullRange_Dn2, "Frequency Response Downsampled N=2 Music")


    #
    # Filter LP Windowed
    #
    # n = np.arange(16)
    # h = np.sin(0.14*np.pi*(n-7.5))/(np.pi*(n-7.5))
    # h = np.ones(16)   
    # hk = np.sin(0.5*np.pi*(n-7.5))/(np.pi*(n-7.5))                 # Sinc
    # hk = 0.5-0.5*np.cos(2*np.pi/16*(np.arange(16)+0.5))            # Hanning
    # hk = np.sin(np.pi/16*(np.arange(16)+0.5))                      # Sine window     
    # hk = np.kaiser(16,8)                                           # Kaiser                      
    # hk = np.sin(np.pi/2*np.sin(np.pi/16*(np.arange(16)+0.5))**2)   # Vorbis
    # hfilt = hk * h
    LP_L = 16
    LP_delay = (LP_L -1)/2.0
    LP_fc = 0.5
    LP_fstop = LP_fc - 0.1 
    n = np.arange(16)
    h = np.sin(LP_fstop*np.pi*(n-LP_delay))/(np.pi*(n-LP_delay))
    hk = np.kaiser(16,8)
    hfilt = hk * h

    #
    # Convert to highpass
    #
    hfilt_HP = hfilt * np.cos( (np.pi) * np.arange(LP_L) )
    PlotFreqResponse(hfilt_HP, "Frequency Response from hfilt")


    #
    # Upsample
    #
    SpeechSignalFullRange_Dn2_Up2 = np.zeros(2 * len(SpeechSignalFullRange_Dn2))
    SpeechSignalFullRange_Dn2_Up2[::2] = SpeechSignalFullRange_Dn2
    MusicSignalFullRange_Dn2_Up2 = np.zeros(2 * len(MusicSignalFullRange_Dn2))
    MusicSignalFullRange_Dn2_Up2[::2] = MusicSignalFullRange_Dn2

    # Plot fequency response - Speech
    PlotFreqResponse(SpeechSignalFullRange_Dn2_Up2, "Frequency Response - Speech Downsampled Upsampled")
    # Plot fequency response - Music
    PlotFreqResponse(MusicSignalFullRange_Dn2_Up2, "Frequency Response - Music Downsampled Upsampled")


    #
    # Filter
    #
    
    #Speech
    SpeechSignalFullRange_Dn2_Up2_Filt = signal.lfilter(hfilt_HP, [1], SpeechSignalFullRange_Dn2_Up2)
    #Music
    MusicSignalFullRange_Dn2_Up2_Filt = signal.lfilter(hfilt_HP, [1], MusicSignalFullRange_Dn2_Up2)

    #
    PlotFreqResponse(SpeechSignalFullRange_Dn2_Up2_Filt, "Frequency Response - Speech Downsampled Upsampled Filtered")
    PlotFreqResponse(MusicSignalFullRange_Dn2_Up2_Filt, "Frequency Response - Music Downsampled Upsampled Filtered")



    #Show plot
    plt.show()

    # #
    # # Play
    # #
    # sd.play(SpeechSignalFullRange_Dn2_Up2_Filt, fs_Speech)
    # sd.wait()
    # sd.play(MusicSignalFullRange_Dn2_Up2_Filt, fs_Music)
    # sd.wait()


#
# main
#
if __name__ == "__main__":
    # Task123()
    Task4()
