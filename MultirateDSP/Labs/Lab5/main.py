"""
Task 1
    Setting 1:
        a)Take a DCT type 4, anddeterminetheequivalentimpulseresponsesfortheanalysisandthesynthesis. The DCT4 transformmatrixisdefinedas:
        b)Usea 8 band DCT (8x8 transformmatrix).
        c)Plot thefrequencyresponsesoftheresultinganalysisandsynthesisfilters.
        d)Test thisfilterbankwiththeaudiosignal. Do youhaveperfectreconstruction?

Task 1
    Setting 2:
        a)On theanalysisside, after subbanddecompositionkeeponlythefirsttwoorthreesubbands, settheotherstozero.
        b)The processon thesynthesissidedoesnot change.
        c)UsetheaudiosignaltotestyourDCT filterbank
        d)Howdoesthereconstructedsignalsoundin comparisontotheoriginal?

Task 2
    a)EfficientlyimplementanMDCTanalysisandasynthesisfilterbank,usingthepolyphaseimplementationwiththepolyphasematricesH(z)andG(z),asdescribedinthelecture,withN=8subbandsandasinewindowoflength16.(SeeFig.1inthenextslide)
    b)ImplementSetting1and2fromTask1
    c)Testyourfilterbankwiththeaudiosignal
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
    Lab5 Task 1.-
    """
    print("Lab 5 Task 1:")
    
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

    # # Plot fequency response - Speech
    # PlotFreqResponse(SpeechSignalFullRange, "Frequency Response Speech")
    # # Plot fequency response - Music
    # PlotFreqResponse(MusicSignalFullRange, "Frequency Response Music")



    # DCT Analysis
    N = 8
    T = []
    n = np.arange(N)
    for k in range(N):
        dct4_temp = math.sqrt(2.0/N)*(np.cos((math.pi/N)*(n+0.5)*(k+0.5)))
        T.append(dct4_temp)
    
    # Plot frequency response of all filters
    plt.figure()
    for it in range(N):
        # Plot fequency response
        [freq, response] = scipy.signal.freqz(np.flipud(T[it]))
        # fig.suptitle("Filter Bank Frequency Response - Magnitude")
        #Magnitude
        plt.plot((freq/math.pi), 20 * np.log10(np.abs(response)))
        plt.title("Magnitude of Frequency Response")
        plt.xlabel('Normalized Frequency (xPi [rad/sample])')
        plt.ylabel("Magnitude [dB]")

    # DCT Synthesis - G = T^-1 = T^T = T
    G = []
    n = np.arange(N)
    for k in range(N):
        dct4_temp = math.sqrt(2.0/N)*(np.cos((math.pi/N)*(n+0.5)*(k+0.5)))
        G.append(dct4_temp)

    # Downsample N = 8
    SpeechSignalFullRange_Dn8_List = []
    MusicSignalFullRange_Dn8_List = []
    for it in range(0,N):
        Speech_Dn_Temp = SpeechSignalFullRange[it::N]
        Music_Dn_Temp = MusicSignalFullRange[it::N]
        SpeechSignalFullRange_Dn8_List.append(Speech_Dn_Temp)
        MusicSignalFullRange_Dn8_List.append(Music_Dn_Temp)

    # Filter - Analysis
    SpeechSignalFullRange_Dn8_Analysis_List = []
    MusicSignalFullRange_Dn8_Analysis_List = []
    for it in range(0,N):
        SpeechSignalFullRange_Dn2_Up2_Filt_temp = scipy.signal.lfilter(T[it], [1], SpeechSignalFullRange_Dn8_List[it])
        MusicSignalFullRange_Dn2_Up2_Filt_temp = scipy.signal.lfilter(T[it], [1], MusicSignalFullRange_Dn8_List[it])
        SpeechSignalFullRange_Dn8_Analysis_List.append(SpeechSignalFullRange_Dn2_Up2_Filt_temp)
        MusicSignalFullRange_Dn8_Analysis_List.append(MusicSignalFullRange_Dn2_Up2_Filt_temp)

    # Upsample
    SpeechSignalFullRange_Dn8_Analysis_Up_List = []
    MusicSignalFullRange_Dn8_Analysis_Up_List = []
    for it in range(0,N):
        SpeechSignalFullRange_temp = np.zeros(N * len(SpeechSignalFullRange_Dn8_Analysis_List[it]))
        SpeechSignalFullRange_temp[it::N] = SpeechSignalFullRange_Dn8_Analysis_List[it]
        MusicSignalFullRange_temp = np.zeros(N * len(MusicSignalFullRange_Dn8_Analysis_List[it]))
        MusicSignalFullRange_temp[it::N] = MusicSignalFullRange_Dn8_Analysis_List[it]
        SpeechSignalFullRange_Dn8_Analysis_Up_List.append(SpeechSignalFullRange_temp)
        MusicSignalFullRange_Dn8_Analysis_Up_List.append(MusicSignalFullRange_temp)

    # Filter - Synthesis
    SpeechSignalFullRange_Dn8_Analysis_Up_Synthesis_List = []
    MusicSignalFullRange_Dn8_Analysis_Up_Synthesis_List = []
    for it in range(0,N):
        SpeechSignalFullRange_temp = scipy.signal.lfilter(G[it], [1], SpeechSignalFullRange_Dn8_Analysis_Up_List[it])
        MusicSignalFullRange_temp = scipy.signal.lfilter(G[it], [1], MusicSignalFullRange_Dn8_Analysis_Up_List[it])
        SpeechSignalFullRange_Dn8_Analysis_Up_Synthesis_List.append(SpeechSignalFullRange_temp)
        MusicSignalFullRange_Dn8_Analysis_Up_Synthesis_List.append(MusicSignalFullRange_temp)

    # Mix
    SpeechSignalFullRange_Reconstructed = np.concatenate(list(zip(
                                                                        SpeechSignalFullRange_Dn8_Analysis_Up_Synthesis_List[0],
                                                                        SpeechSignalFullRange_Dn8_Analysis_Up_Synthesis_List[1],
                                                                        SpeechSignalFullRange_Dn8_Analysis_Up_Synthesis_List[2],
                                                                        SpeechSignalFullRange_Dn8_Analysis_Up_Synthesis_List[3],
                                                                        SpeechSignalFullRange_Dn8_Analysis_Up_Synthesis_List[4],
                                                                        SpeechSignalFullRange_Dn8_Analysis_Up_Synthesis_List[5],
                                                                        SpeechSignalFullRange_Dn8_Analysis_Up_Synthesis_List[6], 
                                                                        SpeechSignalFullRange_Dn8_Analysis_Up_Synthesis_List[7]
                                                                    )))
    MusicSignalFullRange_Reconstructed = np.concatenate(list(zip(
                                                                        MusicSignalFullRange_Dn8_Analysis_Up_Synthesis_List[0],
                                                                        MusicSignalFullRange_Dn8_Analysis_Up_Synthesis_List[1],
                                                                        MusicSignalFullRange_Dn8_Analysis_Up_Synthesis_List[2],
                                                                        MusicSignalFullRange_Dn8_Analysis_Up_Synthesis_List[3],
                                                                        MusicSignalFullRange_Dn8_Analysis_Up_Synthesis_List[4],
                                                                        MusicSignalFullRange_Dn8_Analysis_Up_Synthesis_List[5],
                                                                        MusicSignalFullRange_Dn8_Analysis_Up_Synthesis_List[6],
                                                                        MusicSignalFullRange_Dn8_Analysis_Up_Synthesis_List[7]
                                                                    )))

    #
    # Play
    #
    # sd.play(SpeechSignalFullRange_Reconstructed, 8*fs_Speech)
    # sd.wait()
    sd.play(MusicSignalFullRange_Reconstructed, 8*fs_Music)
    sd.wait()

    #
    style.use("dark_background")
    fig, pltArr = plt.subplots(2, sharex=True) 
    fig.suptitle("Signals")
    pltArr[0].plot(SpeechSignalFullRange_Reconstructed, color='red')
    pltArr[0].set_title("Speech reconstructed Signal")
    pltArr[1].plot(MusicSignalFullRange_Reconstructed, color='red')
    pltArr[1].set_title("Music reconstructed Signal")


    #Show plot
    plt.show()


# Task2
def Task2():
    """
    Lab5 Task 2.-
    """
    print("Lab 5 Task 2:")

    #
    from x2polyphase import *
    from polmatmult import *
    from Fafoldingmatrix import *
    from DCT4 import *
    
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

    # # Plot fequency response - Speech
    # PlotFreqResponse(SpeechSignalFullRange, "Frequency Response Speech")
    # # Plot fequency response - Music
    # PlotFreqResponse(MusicSignalFullRange, "Frequency Response Music")


    # MDCT




    #Show plot
    plt.show()


#
# main
#
if __name__ == "__main__":
    Task1()
    # Task2()
