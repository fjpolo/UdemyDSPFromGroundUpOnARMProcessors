"""
Task 1:
     Take an audio signal Track48.wav (download from moodle)
     Open/read a *.wav audio into integer array; find out sampling frequency, number of bits and print them
     Hint – to read wav-file use scipy.io.wavfile
         Be careful: the name of the audio file is an string, you must write „name.wav“
     Reproduce the audio at the desired sampling frequency
         Hint – to play audio use pyaudio
         Be careful: pyaudio stream.write() needs string values!!
     Extract 8 seconds from the middle of the audio data.
         Be careful: you need to translate first the seconds into samples!
     Normalize the fragment dividing each channel by its maximum (take into account data type and its range)
     Plot and play both channels separately to check you have not chosen a silence fragment:
         Hint - „matplotlib.pyplot“
Task 2: Fast Fourier Transformation (FFT)
     Use previous audio signal (only one channel)
     Process it block wise, by taking 4 consecutive blocks of 1024 samples
     Apply the FFT to it
     Plot the magnitude of it (The 4 different FFT blocks in different colors on top of each other)

Task 3: Quantization
     Write a python function „encframewk.py“ that reads "Track48.wav" audio file with 16 bit per sample and stores the samples with 16 bit per sample in a binary file "encoded.bin"
         Hint: for saving file you can use library pickle with command pickle.dump(array, file, 1) or such
     Write a python function „decframewk.py“ that reads "encoded.bin", and stores clean data into 16 bit samples back into the "decoded.wav"
         Hint: you can use for loading "*.bin" file pickle.load(file)
     Observe if the size of the *.wav and the *.bin files are different?

Task 4: Quantization
     Extend the framework into "encfamewk8bit.py" and "decframewk8bit.py"
     Store its encoded binary data into a binary file "encoded8bit.bin“
     To increase compression, and hence to obtain a smaller binary file „encoded8bit.bin“ (half the size), in the "encframewk8bit.py" quantize the audio samples from the sound file to 8 bit per sample
     Use uniform quantizer
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
# from polmatmult import *
# from polyphase import *
# from FAfoldingmatrix import *
# from DCT4 import *
from scipy.io import wavfile
from scipy.fft import fft, fftfreq
from encframewk import *
from decframewk import *
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

# PyAudioPlay
def PyAudioPlay(input_array, rate, channels):
    # instantiate PyAudio (1)
    p = pyaudio.PyAudio()

    # open stream (2), 2 is size in bytes of int16
    stream = p.open(format=p.get_format_from_width(2),
                    channels=channels,
                    rate=rate,
                    output=True)

    # play stream (3), blocking call
    stream.write(input_array)

    # stop stream (4)
    stream.stop_stream()
    stream.close()

    # close PyAudio (5)
    p.terminate()
    


#
# Private Tasks
#

# Task1
def Task1():
    """
    Lab1 Task 1.-
    """
    print("Lab 1 Task 1:")
    
    # 
    # Signals
    #
    
    # Speech
    # SpeechPath = "AudioCoding\Labs\speech8kHz.wav"
    # fs_Speech, SpeechSignalFullRange = wavfile.read(SpeechPath)
    # SpeechSignal_length = SpeechSignalFullRange.shape[0] / fs_Speech
    # print(f"    Speech fs: {fs_Speech}")
    # print(f"    Samples: {SpeechSignalFullRange.shape[0]}")
    # print(f"    Length = {SpeechSignal_length}[s]")

    # Music
    MusicPath = "AudioCoding\Labs\ImperialMarch_12.wav"
    fs_Music, MusicSignalFullRange = wavfile.read(MusicPath)
    MusicSignal_length = MusicSignalFullRange.shape[0] / fs_Music
    print(f"    Music fs: {fs_Music}")
    print(f"    Samples: {MusicSignalFullRange.shape[0]}")
    print(f"    Length = {MusicSignal_length}[s]")
    MusicSignalFullRange_L = MusicSignalFullRange[:, 0]
    MusicSignalFullRange_R = MusicSignalFullRange[:, 1]

    # sd.play(MusicSignalFullRange, fs_Music)
    # sd.wait()

    # # Plot fequency response - Speech
    # PlotFreqResponse(SpeechSignalFullRange, "Frequency Response Speech")
    # # Plot fequency response - Music
    # PlotFreqResponse(MusicSignalFullRange, "Frequency Response Music")

    #
    # PyAudioPlay(SpeechSignalFullRange, fs_Speech, 1)
    # PyAudioPlay(MusicSignalFullRange, fs_Music, 2)

    #
    # Extract 8 seconds from the middle of the audio data - Music
    #
    Sample_time = 8
    MusicMiddleSample = np.floor(MusicSignalFullRange_L.shape[0] / 2)
    MusicDurationOfOneSampleinS = 1 / fs_Music
    MusicNumberOfSamplesFor2S = Sample_time * fs_Music
    print(f"    Music Middle Sample: {MusicMiddleSample}")
    print(f"    Duration of one sample: {MusicDurationOfOneSampleinS}[S]")    
    print(f"    Number of samples for {Sample_time}[S]: {MusicNumberOfSamplesFor2S}")
    MusicSignalFullRange_L_Middle8S = MusicSignalFullRange_L[int(MusicMiddleSample - MusicNumberOfSamplesFor2S/2):int(MusicMiddleSample + MusicNumberOfSamplesFor2S/2)]
    MusicSignalFullRange_R_Middle8S = MusicSignalFullRange_R[int(MusicMiddleSample - MusicNumberOfSamplesFor2S/2):int(MusicMiddleSample + MusicNumberOfSamplesFor2S/2)]

    # Normalize 
    MusicSignalFullRange_L_Middle8S = MusicSignalFullRange_L_Middle8S / np.max(MusicSignalFullRange_L_Middle8S)
    MusicSignalFullRange_R_Middle8S = MusicSignalFullRange_R_Middle8S / np.max(MusicSignalFullRange_R_Middle8S)

    #
    # Plot Full range signals
    #
    style.use("dark_background")
    fig, pltArr = plt.subplots(3, sharex=True) 
    fig.suptitle("Signals")
    pltArr[0].plot(MusicSignalFullRange, color='red')
    pltArr[0].set_title("Music Signal - Stereo")
    pltArr[1].plot(MusicSignalFullRange_L_Middle8S, color='red')
    pltArr[1].set_title(f"Music Signal - Middle {Sample_time}[S] - L Channel")    
    pltArr[2].plot(MusicSignalFullRange_R_Middle8S, color='red')
    pltArr[2].set_title(f"Music Signal - Middle {Sample_time}[S] - R Channel")

    #
    # FFT
    #
    NumBLocks = 4
    NumSamples = 1024
    MusicSignalFullRange_L_Middle8S_Blocks = []
    MusicSignalFullRange_R_Middle8S_Blocks = []
    plt.figure()
    for block in range(NumBLocks):
        Signalblock = MusicSignalFullRange_L_Middle8S[int(NumSamples*block):int((NumSamples*block)+NumSamples)]
        MusicSignalFullRange_L_Middle8S_Blocks.append(Signalblock)
        plt.plot(Signalblock)
        Signalblock = MusicSignalFullRange_R_Middle8S[int(NumSamples*block):int((NumSamples*block)+NumSamples)]
        MusicSignalFullRange_R_Middle8S_Blocks.append(Signalblock)


    # Apply FFT
    MusicSignalFullRange_L_Middle8S_Blocks_FFT = []
    MusicSignalFullRange_R_Middle8S_Blocks_FFT = []
    # style.use("dark_background")
    # fig, pltArr = plt.subplots(NumBLocks, sharex=True) 
    # fig.suptitle("FFT")
    # for block in range(NumBLocks):
    #     blockFFT = fft(MusicSignalFullRange_L_Middle8S_Blocks[block])
    #     MusicSignalFullRange_L_Middle8S_Blocks_FFT.append(blockFFT)
    #     blockFFT = fft(MusicSignalFullRange_R_Middle8S_Blocks[block])
    #     MusicSignalFullRange_R_Middle8S_Blocks_FFT.append(blockFFT)
    #     #
    #     [freq, response] = signal.freqz(blockFFT)
    #     pltArr[block].plot((freq/math.pi), 20 * np.log10(np.abs(response)))
    #     pltArr[block].set_title(f"Block N°{block} Frequency Response")
    #     pltArr[block].set_xlabel('Normalized Frequency (xPi [rad/sample])')
    #     pltArr[block].set_ylabel("Magnitude [dB]")
    plt.figure()
    # fig.title("FFT")
    plt.xlabel('Normalized Frequency (xPi [rad/sample])')
    plt.ylabel("Magnitude [dB]")
    for block in range(NumBLocks):
        # L channel
        blockFFT = fft(MusicSignalFullRange_L_Middle8S_Blocks[block])
        MusicSignalFullRange_L_Middle8S_Blocks_FFT.append(blockFFT)
        [freq, response] = signal.freqz(blockFFT)
        plt.plot((freq/math.pi), 20 * np.log10(np.abs(response)))
        # R channel
        blockFFT = fft(MusicSignalFullRange_R_Middle8S_Blocks[block])
        MusicSignalFullRange_R_Middle8S_Blocks_FFT.append(blockFFT)
        



    #Show plot
    plt.show()

# Task3
def Task3():
    """
    Lab5 Task 3.-
    """
    print("Lab 1 Task 3:")

    # Encode
    MusicPath = "AudioCoding\Labs\ImperialMarch_12.wav"
    SavePath = "AudioCoding\Labs\Lab1\ImperialMarch_12.bin"
    # samplerate = encframewk_Read32PCM(MusicPath, SavePath)
    samplerate = encframewk_Read16PCM(MusicPath, SavePath)
    # samplerate = encframewk_Read8PCM(MusicPath, SavePath)
    # Decode
    LoadPath = "AudioCoding\Labs\Lab1\ImperialMarch_12.bin"
    wavPath = "AudioCoding\Labs\Lab1\ImperialMarch_12.wav"
    # decframewk_Read32PCM(LoadPath, wavPath, samplerate)
    decframewk_Read16PCM(LoadPath, wavPath, samplerate)
    # decframewk_Read8PCM(LoadPath, wavPath, samplerate)
    # Load decoded signal

    #
    MusicPath = "AudioCoding\Labs\ImperialMarch_12.wav"
    fs_Music, MusicSignal = wavfile.read(MusicPath)
    MusicSignal_L = MusicSignal[:, 0]
    MusicSignal_R = MusicSignal[:, 1]
    MusicPathQuantized = "AudioCoding\Labs\Lab1\ImperialMarch_12.wav"
    fs_Music, MusicSignal8BitQuantized = wavfile.read(MusicPathQuantized)
    # MusicSignal8BitQuantized = np.int8(MusicSignal8BitQuantized/np.max(np.abs(MusicSignal8BitQuantized)) * (2**8))
    MusicSignal8BitQuantized_L = MusicSignal8BitQuantized[:, 0]
    MusicSignal8BitQuantized_R = MusicSignal8BitQuantized[:, 1]
    #Play
    # PyAudioPlay(MusicSignalFullRange, fs_Music, 2)

    #
    # Plot
    #
    style.use("dark_background")
    fig, pltArr = plt.subplots(2, sharex=True) 
    fig.suptitle("Signals")
    pltArr[0].plot(MusicSignal)
    pltArr[0].set_title("Music Signal - Original")  
    pltArr[1].plot(MusicSignal8BitQuantized)
    pltArr[1].set_title(f"Music Signal - 8bit quantized")


    # Show plot
    plt.show()

#
# main
#
if __name__ == "__main__":
    # Task1()
    Task3()