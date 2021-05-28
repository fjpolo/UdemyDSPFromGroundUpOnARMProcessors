"""
Task 1
    a)Design a bandpassfilterusingmodulation, foran 8 band uniform filterbank.
        i.Start witha lowpass filter, whichyoucandesign usingthewindowmethod.
        ii.Design thislowpass filtersuch thatitspass band goesupto1/16thoftheNyquistfrequency.
    b)Then usemodulationsuch thatweobtainall the8 subbands(thesubbandnumbersshouldstartat 0 andgoupto7).
    The band pass filtersshouldbesuch thatall subbandshavethesame bandwidth, meaningthefirstshouldgofrom0 to1/8, thenextfrom1/8thto2/8th, andso on.
    Note: The modulationcanalso beconductedbymultiplicationwitha cosinefunctioninsteadofa complexvaluedexponentialfunction. Use
    Ψ𝑛=cos𝜋8𝑘+0.5𝑛
    asthemodulatingfunction, forsubbandk=0,...,7, withn asthetime index.
    c)Plot thefrequencyresponsesoftheresultingfilters(magnituderangeabout0 to-80 dB, normalizeitsuch that0 dB isthemaximumvalue).
    d)Usea signaltotestthisfilterbank. Filter thesignalandplottheresultingsubbandsignalsin thefrequencydomain.

Task 2
    a)Implementan FFT filterbank.
        i.Usethesame time signal( like an audiosignalwitha lenght> 1000 samples).
        ii.Divideitintoblocks(size8), andthenapplytheFFT toeachblock. This wayyougeta time/frequencyrepresentation, withsubbands, like withthefilterbankview.
    b)Plot theresultingsubbandsignals. Also plotthefrequencyresponseofeachequivalentFFT filter.
    c)Then applytheinverse FFT toobtainthereconstructedsignal. Compareitwiththeoriginal signal.

Task 3
    Comparethetwofilterbanks.
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
def Task1():
    """
    Lab4 Task 1.-
    """
    print("Lab 4 Task 1:")
    
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
    # Filter LP Windowed
    #
    LP_L = 16
    LP_delay = (LP_L - 1) / 2.0
    LP_fc = (1/16.0)
    LP_fstop = LP_fc - 0.1 
    n = np.arange(16)
    h = np.sin(LP_fstop * np.pi * (n - LP_delay) ) / (np.pi * (n - LP_delay))
    hk = np.kaiser(LP_L, 8)
    hfilt = hk * h
    PlotFreqResponse(hfilt, "Frequency Response from hfilt")

    # Modulate
    N = 8
    FilterList = []
    for it in range(0,N):
        omega = it * (np.pi / float(N))
        # hfilter_temp = hfilt * np.cos( omega * np.arange(LP_L) )
        hfilter_temp = hfilt * np.cos( (np.pi/8.0) * (it + 0.5) * np.arange(LP_L) )
        FilterList.append(hfilter_temp)
    
    # Plot frequency response of all filters
    plt.figure()
    for it in range(0,8):
        # Plot fequency response
        [freq, response] = scipy.signal.freqz(FilterList[it])
        fig.suptitle("Filter Bank Frequency Response - Magnitude")
        #Magnitude
        plt.plot((freq/math.pi), 20 * np.log10(np.abs(response)))
        plt.title("Magnitude of Frequency Response")
        plt.xlabel('Normalized Frequency (xPi [rad/sample])')
        plt.ylabel("Magnitude [dB]")


    

    # Filter the same signal with every filter and plot the frequency response
    SpeechSignalFullRange_Filtered_List = []
    MusicSignalFullRange_Filtered_List = []
    fig, pltArr = plt.subplots(N, sharex=True) 
    for it in range(0, N):
        Speech_temp = scipy.signal.lfilter(FilterList[it], [1], SpeechSignalFullRange)
        Music_temp = scipy.signal.lfilter(FilterList[it], [1], MusicSignalFullRange)
        SpeechSignalFullRange_Filtered_List.append(Speech_temp)
        MusicSignalFullRange_Filtered_List.append(Music_temp)
        # Plot fequency response
        [freq, response] = scipy.signal.freqz(Speech_temp)
        fig.suptitle("Filter Bank Frequency Response - Magnitude")
        #Magnitude
        pltArr[it].plot((freq/math.pi), 20 * np.log10(np.abs(response)))
        # pltArr[it].title("Magnitude of Frequency Response")
        pltArr[it].set_xlabel('Normalized Frequency (xPi [rad/sample])')
        pltArr[it].set_ylabel("Magnitude [dB]")



    # Filter - Synthesis

    # Mix

    # Upsample    

    # Plot   
  




    #
    # Filter -> Downsample -> Upsample -> Filter -> Reconstruct
    #

    # # Downsample N = 8
    # N = 8
    # SpeechSignalFullRange_Dn8_List = []
    # MusicSignalFullRange_Dn8_List = []
    # for it in range(0,N):
    #     Speech_Dn_Temp = SpeechSignalFullRange[it::N]
    #     Music_Dn_Temp = MusicSignalFullRange[it::N]
    #     SpeechSignalFullRange_Dn8_List.append(Speech_Dn_Temp)
    #     MusicSignalFullRange_Dn8_List.append(Music_Dn_Temp)

    # # Filter - Analysis
    # SpeechSignalFullRange_Dn8_Filtered_List = []
    # MusicSignalFullRange_Dn8_Filtered_List = []
    # for it in range(0,N):
    #     SpeechSignalFullRange_Dn2_Up2_Filt_temp = scipy.signal.lfilter(FilterList[it], [1], SpeechSignalFullRange_Dn8_List[it])
    #     MusicSignalFullRange_Dn2_Up2_Filt_temp = scipy.signal.lfilter(FilterList[it], [1], MusicSignalFullRange_Dn8_List[it])
    #     #
    #     # print(it, ":", SpeechSignalFullRange_Dn2_Up2_Filt_temp[:16], "\n")
    #     # PlotFreqResponse(SpeechSignalFullRange_Dn2_Up2_Filt_temp, "")
    #     # print(SpeechSignalFullRange_Dn2_Up2_Filt_temp.shape)
    #     #
    #     SpeechSignalFullRange_Dn8_Filtered_List.append(SpeechSignalFullRange_Dn2_Up2_Filt_temp)
    #     MusicSignalFullRange_Dn8_Filtered_List.append(MusicSignalFullRange_Dn2_Up2_Filt_temp)

    # # Mix
    # SpeechSignalFullRange_Dn8_Filtered_Up8 = np.concatenate(list(zip(
    #                                                                     SpeechSignalFullRange_Dn8_Filtered_List[0],
    #                                                                     SpeechSignalFullRange_Dn8_Filtered_List[1],
    #                                                                     SpeechSignalFullRange_Dn8_Filtered_List[2],
    #                                                                     SpeechSignalFullRange_Dn8_Filtered_List[3],
    #                                                                     SpeechSignalFullRange_Dn8_Filtered_List[4],
    #                                                                     SpeechSignalFullRange_Dn8_Filtered_List[5],
    #                                                                     SpeechSignalFullRange_Dn8_Filtered_List[6], 
    #                                                                     SpeechSignalFullRange_Dn8_Filtered_List[7]
    #                                                                 )))
    # MusicSignalFullRange_Dn8_Filtered_Up8 = np.concatenate(list(zip(
    #                                                                     MusicSignalFullRange_Dn8_Filtered_List[0],
    #                                                                     MusicSignalFullRange_Dn8_Filtered_List[1],
    #                                                                     MusicSignalFullRange_Dn8_Filtered_List[2],
    #                                                                     MusicSignalFullRange_Dn8_Filtered_List[3],
    #                                                                     MusicSignalFullRange_Dn8_Filtered_List[4],
    #                                                                     MusicSignalFullRange_Dn8_Filtered_List[5],
    #                                                                     MusicSignalFullRange_Dn8_Filtered_List[6],
    #                                                                     MusicSignalFullRange_Dn8_Filtered_List[7]
    #                                                                 )))

    # #
    # # Plot signals
    # #
    # style.use("dark_background")
    # fig, pltArr = plt.subplots(2, sharex=True) 
    # fig.suptitle("Signals")
    # pltArr[0].plot(SpeechSignalFullRange_Dn8_Filtered_Up8, color='red')
    # pltArr[0].set_title("Speech Signal")
    # pltArr[1].plot(MusicSignalFullRange_Dn8_Filtered_Up8, color='red')
    # pltArr[1].set_title("Music Signal")


    # # Plot fequency response - Speech
    # PlotFreqResponse(SpeechSignalFullRange_Dn8_Filtered_Up8, "Frequency Response - LPfiltered Reconstructed Speech")
    # # Plot fequency response - Music
    # PlotFreqResponse(MusicSignalFullRange_Dn8_Filtered_Up8, "Frequency Response - LPfiltered Reconstructed Music")

    # #
    # # Filter LP Windowed
    # #
    # LP_L = 16
    # LP_delay = (LP_L - 1) / 2.0
    # LP_fc = 0.3
    # LP_fstop = LP_fc - 0.1 
    # n = np.arange(16)
    # h = np.sin(LP_fstop * np.pi * (n - LP_delay) ) / (np.pi * (n - LP_delay))
    # hk = np.kaiser(LP_L, 8)
    # hfilt = hk * h
    # SpeechSignalFullRange_Dn8_Filtered_Up8_LPfiltered = scipy.signal.lfilter(hfilt, [1], SpeechSignalFullRange_Dn8_Filtered_Up8)
    # MusicSignalFullRange_Dn8_Filtered_Up8_LPfiltered = scipy.signal.lfilter(hfilt, [1], MusicSignalFullRange_Dn8_Filtered_Up8)

    # #
    # # Plot signals
    # #
    # style.use("dark_background")
    # fig, pltArr = plt.subplots(2, sharex=True) 
    # fig.suptitle("Signals")
    # pltArr[0].plot(SpeechSignalFullRange_Dn8_Filtered_Up8_LPfiltered, color='red')
    # pltArr[0].set_title("Speech Signal")
    # pltArr[1].plot(MusicSignalFullRange_Dn8_Filtered_Up8_LPfiltered, color='red')
    # pltArr[1].set_title("Music Signal")


    # # Plot fequency response - Speech
    # PlotFreqResponse(SpeechSignalFullRange_Dn8_Filtered_Up8_LPfiltered, "Frequency Response - LPfiltered Reconstructed Speech")
    # # Plot fequency response - Music
    # PlotFreqResponse(MusicSignalFullRange_Dn8_Filtered_Up8_LPfiltered, "Frequency Response - LPfiltered Reconstructed Music")

    #Show plot
    plt.show()




#
# main
#
if __name__ == "__main__":
    Task1()
