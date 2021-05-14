"""
1.Generate 3 different signals

– Use full and 20 dB under full range signals

a)Triangular wave
b)Sinusoidal wave
    - normalized Frequency of 0.1
    - 𝑓𝑟𝑒𝑞𝑛𝑜𝑟𝑚=𝑓𝑓𝑠, where f- frequency of the signal and 𝑓𝑠-sampling frequency
    - Range = -1 to 1
c)Any audio signal (16 bit)
    - You can download a file from our moodle page
    - Duration of the file ≤ 10 s
    - For reading a file into Matlab use wavread(„name.wav“)

Plot and listen to the signals
What is the difference between full and under full range signals?


2.Quantize and reconstruct signals
– Uniform quantization with 16 bit accuracy
    -Implement Mid-tread and Mid-rise quantizers
    - Calculate the quantization error for both of them
    - Which one is better and why?
– μ-law quantization with 8 bit accuracy
    - 𝑦=𝑠𝑖𝑔𝑛(𝑥)∙ln⁡(1+255∙|𝑥𝐴|) / ln⁡(1+255)
    - 𝑥= 𝑠𝑖𝑔𝑛(𝑦)∙( (256𝑦−1) / 255 )∙𝐴

Plot and listen to the signals
Compare results of uniform and μ-law quantization


3.Determine SNR for all the signals. SNR should be calculated in dB.
    𝑆𝑁𝑅=10∗𝑙𝑜𝑔10(𝑆𝑖𝑔𝑛𝑎𝑙⁡𝐸𝑛𝑒𝑟𝑔𝑦 / 𝑄𝑢𝑎𝑛𝑡𝑖𝑧𝑎𝑡𝑖𝑜𝑛⁡𝐸𝑟𝑟𝑜𝑟⁡𝐸𝑛𝑒𝑟𝑔𝑦)

What stands out when comparing the SNRs of the sinusoidal and the triangular wave?
Please, use subplot() for making the plots
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
    # Generate 3 signals: Full Range
    #
    
    # Sine
    SineFullRangeSignal = np.sin(2*np.pi*f_sine*t)
    
    # Triangular
    TriangularSignalFullRange = signal.sawtooth(2*np.pi*f_triangle*t)
    
    # Audio
    # open the file for reading.
    audioPath = "AdvancedDSP\Labs\Lab1\ImperialMarch_12.wav"
    a = AudioFile(audioPath)
    # a.play()
    # a.close()
    AudioSignalFulRange = a.extract()

    #
    # Plot Full range signals
    #
    style.use("dark_background")
    fig, pltArr = plt.subplots(3, sharex=True) 
    fig.suptitle("Full Range signals")
    pltArr[0].plot(SineFullRangeSignal, color='red')
    pltArr[0].set_title("Sine Signal", color='red')
    pltArr[1].plot(TriangularSignalFullRange, color='red')
    pltArr[1].set_title("Triangular Signal", color='red')
    pltArr[2].plot(AudioSignalFulRange, color='red')
    pltArr[2].set_title("Audio Signal", color='red')

    # 
    # Generate 3 signals: 20dB under full range (1/10th)
    #

    # Sine
    SineSignalU20dB = 0.1 *  np.sin(2*np.pi*f_sine*t)
    
    # Triangular
    TriangularSignalU20dB = 0.1 * signal.sawtooth(2*np.pi*f_triangle*t)

    # Audio
    # open the file for reading.
    audioPath = "AdvancedDSP\Labs\Lab1\ImperialMarch_12.wav"
    a = AudioFile(audioPath)
    # a.play()
    # a.close()
    AudioSignalU20dB = a.extract() / 10

    #
    # Plot U20dB signals
    #
    style.use("dark_background")
    fig, pltArr = plt.subplots(3, sharex=True) 
    fig.suptitle("U20dB signals")
    pltArr[0].plot(SineSignalU20dB, color='red')
    pltArr[0].set_title("Sine Signal", color='red')
    pltArr[1].plot(TriangularSignalU20dB, color='red')
    pltArr[1].set_title("Triangular Signal", color='red')
    pltArr[2].plot(AudioSignalU20dB, color='red')
    pltArr[2].set_title("Audio Signal", color='red')
    #
    plt.show()

    """
    What is the difference between full and under full range signals?

    SNR is going to change. If we got 90dB of SNR for full range, then
    SNR for under range signal is going to be 70dB (90-20)	
    """

# Task2
def Task2():
    """
    Lab1 Task 2.-
    """
    print("Lab 1 Task 2:")
    
    #
    # Full-Range
    #

    # Signals

    # Sine
    SineFullRangeSignal = np.sin(2*np.pi*f_sine*t)
    # Triangular
    TriangularSignalFullRange = signal.sawtooth(2*np.pi*f_triangle*t)

    # Audio
    # open the file for reading.
    audioPath = "AdvancedDSP\Labs\Lab1\ImperialMarch_12.wav"
    a = AudioFile(audioPath)
    AudioSignalFullRange = a.extract()
    
    #
    # Uniform Quantization with 16-bit - MidRise quantizer
    #

    #Step
    # step = (1-(-1))/(2**16)
    step = (max(t)-(min(t)))/(2**16)

    # Sine
    SineFullRangeSignal_MidRise = np.floor(SineFullRangeSignal/step)
    SineFullRangeSignal_MidRise_reconstructed = SineFullRangeSignal_MidRise * step

    # Triangular
    TriangularSignalFullRange_MidRise = np.floor(TriangularSignalFullRange/step)
    TriangularSignalFullRange_MidRise_reconstructed = TriangularSignalFullRange_MidRise * step

    # Audio
    AudioSignalFullRange_MidRise = np.floor(AudioSignalFullRange/step)
    AudioSignalFullRange_MidRise_reconstructed = AudioSignalFullRange_MidRise * step

    #
    # Plot Sine
    #
    style.use("dark_background")
    fig, pltArr = plt.subplots(4, sharex=True) 
    fig.suptitle("Full-Range Mid-Rise Quantization")
    pltArr[0].plot(SineFullRangeSignal, color='red')
    pltArr[0].set_title("Sine Signal")
    pltArr[1].plot(SineFullRangeSignal_MidRise, color='red')
    pltArr[1].set_title("Sine Quantized Signal")
    pltArr[2].plot(SineFullRangeSignal_MidRise_reconstructed, color='red')
    pltArr[2].set_title("Sine reconstructed Signal")
    pltArr[3].plot(abs(SineFullRangeSignal - SineFullRangeSignal_MidRise_reconstructed), color='red')
    pltArr[3].set_title("Error Signal")

    #
    # Plot Triangular
    #
    style.use("dark_background")
    fig, pltArr = plt.subplots(4, sharex=True) 
    fig.suptitle("Full-Range Mid-Rise Quantization")
    pltArr[0].plot(TriangularSignalFullRange, color='red')
    pltArr[0].set_title("Triangular Signal")
    pltArr[1].plot(TriangularSignalFullRange_MidRise, color='red')
    pltArr[1].set_title("Triangular Quantized Signal")
    pltArr[2].plot(TriangularSignalFullRange_MidRise_reconstructed, color='red')
    pltArr[2].set_title("Triangular reconstructed Signal")
    pltArr[3].plot(abs(TriangularSignalFullRange - TriangularSignalFullRange_MidRise_reconstructed), color='red')
    pltArr[3].set_title("Error Signal")


    #
    # Plot Audio
    #
    style.use("dark_background")
    fig, pltArr = plt.subplots(4, sharex=True) 
    fig.suptitle("Full-Range Mid-Rise Quantization")
    pltArr[0].plot(AudioSignalFullRange, color='red')
    pltArr[0].set_title("Audio Signal")
    pltArr[1].plot(AudioSignalFullRange_MidRise, color='red')
    pltArr[1].set_title("Audio Quantized Signal")
    pltArr[2].plot(AudioSignalFullRange_MidRise_reconstructed, color='red')
    pltArr[2].set_title("Audio reconstructed Signal")
    pltArr[3].plot(abs(AudioSignalFullRange - AudioSignalFullRange_MidRise_reconstructed), color='red')
    pltArr[3].set_title("Error Signal")
    #
    plt.show()


    #
    # Uniform Quantization with 16-bit - MidTread quantizer
    #

    #Step
    step = (max(t)-(min(t)))/(2**16)

    # Sine
    SineFullRangeSignal_MidTread = np.round(SineFullRangeSignal/step)
    SineFullRangeSignal_MidTread_reconstructed = SineFullRangeSignal_MidTread * step

    # Triangular
    TriangularSignalFullRange_MidTread = np.round(TriangularSignalFullRange/step)
    TriangularSignalFullRange_MidTread_reconstructed = TriangularSignalFullRange_MidTread * step

    # Audio
    AudioSignalFullRange_MidTread = np.round(AudioSignalFullRange/step)
    AudioSignalFullRange_MidTread_reconstructed = AudioSignalFullRange_MidTread * step

    #
    # Plot Sine
    #
    style.use("dark_background")
    fig, pltArr = plt.subplots(4, sharex=True) 
    fig.suptitle("Full-Range Mid-Rise Quantization")
    pltArr[0].plot(SineFullRangeSignal, color='red')
    pltArr[0].set_title("Sine Signal")
    pltArr[1].plot(SineFullRangeSignal_MidTread, color='red')
    pltArr[1].set_title("Sine Quantized Signal")
    pltArr[2].plot(SineFullRangeSignal_MidTread_reconstructed, color='red')
    pltArr[2].set_title("Sine reconstructed Signal")
    pltArr[3].plot(abs(SineFullRangeSignal - SineFullRangeSignal_MidTread_reconstructed), color='red')
    pltArr[3].set_title("Error Signal")

    #
    # Plot Triangular
    #
    style.use("dark_background")
    fig, pltArr = plt.subplots(4, sharex=True) 
    fig.suptitle("Full-Range Mid-Rise Quantization")
    pltArr[0].plot(TriangularSignalFullRange, color='red')
    pltArr[0].set_title("Triangular Signal")
    pltArr[1].plot(TriangularSignalFullRange_MidTread, color='red')
    pltArr[1].set_title("Triangular Quantized Signal")
    pltArr[2].plot(TriangularSignalFullRange_MidTread_reconstructed, color='red')
    pltArr[2].set_title("Triangular reconstructed Signal")
    pltArr[3].plot(abs(TriangularSignalFullRange - TriangularSignalFullRange_MidTread_reconstructed), color='red')
    pltArr[3].set_title("Error Signal")


    #
    # Plot Audio
    #
    style.use("dark_background")
    fig, pltArr = plt.subplots(4, sharex=True) 
    fig.suptitle("Full-Range Mid-Rise Quantization")
    pltArr[0].plot(AudioSignalFullRange, color='red')
    pltArr[0].set_title("Audio Signal")
    pltArr[1].plot(AudioSignalFullRange_MidTread, color='red')
    pltArr[1].set_title("Audio Quantized Signal")
    pltArr[2].plot(AudioSignalFullRange_MidTread_reconstructed, color='red')
    pltArr[2].set_title("Audio reconstructed Signal")
    pltArr[3].plot(abs(AudioSignalFullRange - AudioSignalFullRange_MidTread_reconstructed), color='red')
    pltArr[3].set_title("Error Signal")
    #
    plt.show()



    #
    # uLaw Quantization with 8-bit
    #

    #Step
    A = 1
    mu = 2**8 - 1

    # Sine
    SineFullRangeSignal_uLaw = np.sign(SineFullRangeSignal) * (np.log(1+mu*np.abs(SineFullRangeSignal/A)))/np.log(mu+1)
    SineFullRangeSignal_uLaw_reconstructed = np.sign(SineFullRangeSignal_uLaw) * ( ((mu+1)**np.abs(SineFullRangeSignal_uLaw) - 1) / (mu) ) * A
    
    # Triangular
    TriangularSignalFullRange_uLaw = np.sign(TriangularSignalFullRange) * (np.log(1+mu*np.abs(TriangularSignalFullRange/A)))/np.log(mu+1)
    TriangularFullRangeSignal_uLaw_reconstructed = np.sign(TriangularSignalFullRange_uLaw) * ( ((mu+1)**np.abs(TriangularSignalFullRange_uLaw) - 1) / (mu) ) * A

    # Audio
    AudioSignalFullRange_uLaw = np.sign(AudioSignalFullRange) * (np.log(1+mu*np.abs(AudioSignalFullRange/A)))/np.log(mu+1)
    AudioFullRangeSignal_uLaw_reconstructed = np.sign(AudioSignalFullRange_uLaw) * ( ((mu+1)**np.abs(AudioSignalFullRange_uLaw) - 1) / (mu) ) * A

    #
    # Plot Sine
    #
    style.use("dark_background")
    fig, pltArr = plt.subplots(4, sharex=True) 
    fig.suptitle("Full-Range u-Law Quantization")
    pltArr[0].plot(SineFullRangeSignal, color='red')
    pltArr[0].set_title("Sine Signal")
    pltArr[1].plot(SineFullRangeSignal_uLaw, color='red')
    pltArr[1].set_title("Sine Quantized Signal")
    pltArr[2].plot(SineFullRangeSignal_uLaw_reconstructed, color='red')
    pltArr[2].set_title("Sine reconstructed Signal")
    pltArr[3].plot(abs(SineFullRangeSignal - SineFullRangeSignal_uLaw_reconstructed), color='red')
    pltArr[3].set_title("Error Signal")

    #
    # Plot Triangular
    #
    style.use("dark_background")
    fig, pltArr = plt.subplots(4, sharex=True) 
    fig.suptitle("Full-Range Mid-Rise Quantization")
    pltArr[0].plot(TriangularSignalFullRange, color='red')
    pltArr[0].set_title("Triangular Signal")
    pltArr[1].plot(TriangularSignalFullRange_uLaw, color='red')
    pltArr[1].set_title("Triangular Quantized Signal")
    pltArr[2].plot(TriangularFullRangeSignal_uLaw_reconstructed, color='red')
    pltArr[2].set_title("Triangular reconstructed Signal")
    pltArr[3].plot(abs(TriangularSignalFullRange - TriangularFullRangeSignal_uLaw_reconstructed), color='red')
    pltArr[3].set_title("Error Signal")


    #
    # Plot Audio
    #
    style.use("dark_background")
    fig, pltArr = plt.subplots(4, sharex=True) 
    fig.suptitle("Full-Range Mid-Rise Quantization")
    pltArr[0].plot(AudioSignalFullRange, color='red')
    pltArr[0].set_title("Audio Signal")
    pltArr[1].plot(AudioSignalFullRange_uLaw, color='red')
    pltArr[1].set_title("Audio Quantized Signal")
    pltArr[2].plot(AudioFullRangeSignal_uLaw_reconstructed, color='red')
    pltArr[2].set_title("Audio reconstructed Signal")
    pltArr[3].plot(abs(AudioSignalFullRange - AudioFullRangeSignal_uLaw_reconstructed), color='red')
    pltArr[3].set_title("Error Signal")
    #
    plt.show()




    #
    # 20db Under Full-Range
    #

    # Signals

    # Sine
    SineFullRangeSignal = 0.1 * np.sin(2*np.pi*f_sine*t)
    # Triangular
    TriangularSignalFullRange = 0.1 * signal.sawtooth(2*np.pi*f_triangle*t)

    # Audio
    # open the file for reading.
    audioPath = "AdvancedDSP\Labs\Lab1\ImperialMarch_12.wav"
    a = AudioFile(audioPath)
    AudioSignalFullRange = a.extract() / 10
    
    #
    # Uniform Quantization with 16-bit - MidRise quantizer
    #

    #Step
    # step = (1-(-1))/(2**16)
    step = (max(t)-(min(t)))/(2**16)

    # Sine
    SineFullRangeSignal_MidRise = np.floor(SineFullRangeSignal/step)
    SineFullRangeSignal_MidRise_reconstructed = SineFullRangeSignal_MidRise * step

    # Triangular
    TriangularSignalFullRange_MidRise = np.floor(TriangularSignalFullRange/step)
    TriangularSignalFullRange_MidRise_reconstructed = TriangularSignalFullRange_MidRise * step

    # Audio
    AudioSignalFullRange_MidRise = np.floor(AudioSignalFullRange/step)
    AudioSignalFullRange_MidRise_reconstructed = AudioSignalFullRange_MidRise * step

    #
    # Plot Sine
    #
    style.use("dark_background")
    fig, pltArr = plt.subplots(4, sharex=True) 
    fig.suptitle("20db Under Full-Range Mid-Rise Quantization")
    pltArr[0].plot(SineFullRangeSignal, color='red')
    pltArr[0].set_title("Sine Signal")
    pltArr[1].plot(SineFullRangeSignal_MidRise, color='red')
    pltArr[1].set_title("Sine Quantized Signal")
    pltArr[2].plot(SineFullRangeSignal_MidRise_reconstructed, color='red')
    pltArr[2].set_title("Sine reconstructed Signal")
    pltArr[3].plot(abs(SineFullRangeSignal - SineFullRangeSignal_MidRise_reconstructed), color='red')
    pltArr[3].set_title("Error Signal")

    #
    # Plot Triangular
    #
    style.use("dark_background")
    fig, pltArr = plt.subplots(4, sharex=True) 
    fig.suptitle("20db Under Full-Range Mid-Rise Quantization")
    pltArr[0].plot(TriangularSignalFullRange, color='red')
    pltArr[0].set_title("Triangular Signal")
    pltArr[1].plot(TriangularSignalFullRange_MidRise, color='red')
    pltArr[1].set_title("Triangular Quantized Signal")
    pltArr[2].plot(TriangularSignalFullRange_MidRise_reconstructed, color='red')
    pltArr[2].set_title("Triangular reconstructed Signal")
    pltArr[3].plot(abs(TriangularSignalFullRange - TriangularSignalFullRange_MidRise_reconstructed), color='red')
    pltArr[3].set_title("Error Signal")


    #
    # Plot Audio
    #
    style.use("dark_background")
    fig, pltArr = plt.subplots(4, sharex=True) 
    fig.suptitle("20db Under Full-Range Mid-Rise Quantization")
    pltArr[0].plot(AudioSignalFullRange, color='red')
    pltArr[0].set_title("Audio Signal")
    pltArr[1].plot(AudioSignalFullRange_MidRise, color='red')
    pltArr[1].set_title("Audio Quantized Signal")
    pltArr[2].plot(AudioSignalFullRange_MidRise_reconstructed, color='red')
    pltArr[2].set_title("Audio reconstructed Signal")
    pltArr[3].plot(abs(AudioSignalFullRange - AudioSignalFullRange_MidRise_reconstructed), color='red')
    pltArr[3].set_title("Error Signal")
    #
    plt.show()


    #
    # Uniform Quantization with 16-bit - MidTread quantizer
    #

    #Step
    step = (max(t)-(min(t)))/(2**16)

    # Sine
    SineFullRangeSignal_MidTread = np.round(SineFullRangeSignal/step)
    SineFullRangeSignal_MidTread_reconstructed = SineFullRangeSignal_MidTread * step

    # Triangular
    TriangularSignalFullRange_MidTread = np.round(TriangularSignalFullRange/step)
    TriangularSignalFullRange_MidTread_reconstructed = TriangularSignalFullRange_MidTread * step

    # Audio
    AudioSignalFullRange_MidTread = np.round(AudioSignalFullRange/step)
    AudioSignalFullRange_MidTread_reconstructed = AudioSignalFullRange_MidTread * step

    #
    # Plot Sine
    #
    style.use("dark_background")
    fig, pltArr = plt.subplots(4, sharex=True) 
    fig.suptitle("20db Under Full-Range Mid-Rise Quantization")
    pltArr[0].plot(SineFullRangeSignal, color='red')
    pltArr[0].set_title("Sine Signal")
    pltArr[1].plot(SineFullRangeSignal_MidTread, color='red')
    pltArr[1].set_title("Sine Quantized Signal")
    pltArr[2].plot(SineFullRangeSignal_MidTread_reconstructed, color='red')
    pltArr[2].set_title("Sine reconstructed Signal")
    pltArr[3].plot(abs(SineFullRangeSignal - SineFullRangeSignal_MidTread_reconstructed), color='red')
    pltArr[3].set_title("Error Signal")

    #
    # Plot Triangular
    #
    style.use("dark_background")
    fig, pltArr = plt.subplots(4, sharex=True) 
    fig.suptitle("20db Under Full-Range Mid-Rise Quantization")
    pltArr[0].plot(TriangularSignalFullRange, color='red')
    pltArr[0].set_title("Triangular Signal")
    pltArr[1].plot(TriangularSignalFullRange_MidTread, color='red')
    pltArr[1].set_title("Triangular Quantized Signal")
    pltArr[2].plot(TriangularSignalFullRange_MidTread_reconstructed, color='red')
    pltArr[2].set_title("Triangular reconstructed Signal")
    pltArr[3].plot(abs(TriangularSignalFullRange - TriangularSignalFullRange_MidTread_reconstructed), color='red')
    pltArr[3].set_title("Error Signal")


    #
    # Plot Audio
    #
    style.use("dark_background")
    fig, pltArr = plt.subplots(4, sharex=True) 
    fig.suptitle("20db Under Full-Range Mid-Rise Quantization")
    pltArr[0].plot(AudioSignalFullRange, color='red')
    pltArr[0].set_title("Audio Signal")
    pltArr[1].plot(AudioSignalFullRange_MidTread, color='red')
    pltArr[1].set_title("Audio Quantized Signal")
    pltArr[2].plot(AudioSignalFullRange_MidTread_reconstructed, color='red')
    pltArr[2].set_title("Audio reconstructed Signal")
    pltArr[3].plot(abs(AudioSignalFullRange - AudioSignalFullRange_MidTread_reconstructed), color='red')
    pltArr[3].set_title("Error Signal")
    #
    plt.show()



    #
    # uLaw Quantization with 8-bit
    #

    #Step
    A = 1
    mu = 2**8 - 1

    # Sine
    SineFullRangeSignal_uLaw = np.sign(SineFullRangeSignal) * (np.log(1+mu*np.abs(SineFullRangeSignal/A)))/np.log(mu+1)
    SineFullRangeSignal_uLaw_reconstructed = np.sign(SineFullRangeSignal_uLaw) * ( ((mu+1)**np.abs(SineFullRangeSignal_uLaw) - 1) / (mu) ) * A
    
    # Triangular
    TriangularSignalFullRange_uLaw = np.sign(TriangularSignalFullRange) * (np.log(1+mu*np.abs(TriangularSignalFullRange/A)))/np.log(mu+1)
    TriangularFullRangeSignal_uLaw_reconstructed = np.sign(TriangularSignalFullRange_uLaw) * ( ((mu+1)**np.abs(TriangularSignalFullRange_uLaw) - 1) / (mu) ) * A

    # Audio
    AudioSignalFullRange_uLaw = np.sign(AudioSignalFullRange) * (np.log(1+mu*np.abs(AudioSignalFullRange/A)))/np.log(mu+1)
    AudioFullRangeSignal_uLaw_reconstructed = np.sign(AudioSignalFullRange_uLaw) * ( ((mu+1)**np.abs(AudioSignalFullRange_uLaw) - 1) / (mu) ) * A

    #
    # Plot Sine
    #
    style.use("dark_background")
    fig, pltArr = plt.subplots(4, sharex=True) 
    fig.suptitle("20db Under Full-Range u-Law Quantization")
    pltArr[0].plot(SineFullRangeSignal, color='red')
    pltArr[0].set_title("Sine Signal")
    pltArr[1].plot(SineFullRangeSignal_uLaw, color='red')
    pltArr[1].set_title("Sine Quantized Signal")
    pltArr[2].plot(SineFullRangeSignal_uLaw_reconstructed, color='red')
    pltArr[2].set_title("Sine reconstructed Signal")
    pltArr[3].plot(abs(SineFullRangeSignal - SineFullRangeSignal_uLaw_reconstructed), color='red')
    pltArr[3].set_title("Error Signal")

    #
    # Plot Triangular
    #
    style.use("dark_background")
    fig, pltArr = plt.subplots(4, sharex=True) 
    fig.suptitle("20db Under Full-Range Mid-Rise Quantization")
    pltArr[0].plot(TriangularSignalFullRange, color='red')
    pltArr[0].set_title("Triangular Signal")
    pltArr[1].plot(TriangularSignalFullRange_uLaw, color='red')
    pltArr[1].set_title("Triangular Quantized Signal")
    pltArr[2].plot(TriangularFullRangeSignal_uLaw_reconstructed, color='red')
    pltArr[2].set_title("Triangular reconstructed Signal")
    pltArr[3].plot(abs(TriangularSignalFullRange - TriangularFullRangeSignal_uLaw_reconstructed), color='red')
    pltArr[3].set_title("Error Signal")


    #
    # Plot Audio
    #
    style.use("dark_background")
    fig, pltArr = plt.subplots(4, sharex=True) 
    fig.suptitle("20db Under Full-Range Mid-Rise Quantization")
    pltArr[0].plot(AudioSignalFullRange, color='red')
    pltArr[0].set_title("Audio Signal")
    pltArr[1].plot(AudioSignalFullRange_uLaw, color='red')
    pltArr[1].set_title("Audio Quantized Signal")
    pltArr[2].plot(AudioFullRangeSignal_uLaw_reconstructed, color='red')
    pltArr[2].set_title("Audio reconstructed Signal")
    pltArr[3].plot(abs(AudioSignalFullRange - AudioFullRangeSignal_uLaw_reconstructed), color='red')
    pltArr[3].set_title("Error Signal")
    #
    plt.show()

# Task3
def Task3():
    """
    Lab1 Task 3.-
    """
    print("Lab 1 Task 3:")

    #
    #
    # Full-Range
    #
    #

    # Signals

    # Sine
    SineFullRangeSignal = np.sin(2*np.pi*f_sine*t)
    # Triangular
    TriangularSignalFullRange = signal.sawtooth(2*np.pi*f_triangle*t)
    # Audio
    # open the file for reading.
    audioPath = "AdvancedDSP\Labs\Lab1\ImperialMarch_12.wav"
    a = AudioFile(audioPath)
    AudioSignalFullRange = a.extract()
    
    #
    # Uniform Quantization with 16-bit - MidRise quantizer
    #

    #Step
    # step = (1-(-1))/(2**16)
    step = (max(t)-(min(t)))/(2**16)
    # Sine
    SineFullRangeSignal_MidRise = np.floor(SineFullRangeSignal/step)
    SineFullRangeSignal_MidRise_reconstructed = SineFullRangeSignal_MidRise * step
    # Triangular
    TriangularSignalFullRange_MidRise = np.floor(TriangularSignalFullRange/step)
    TriangularSignalFullRange_MidRise_reconstructed = TriangularSignalFullRange_MidRise * step
    # Audio
    AudioSignalFullRange_MidRise = np.floor(AudioSignalFullRange/step)
    AudioSignalFullRange_MidRise_reconstructed = AudioSignalFullRange_MidRise * step


    #
    # Uniform Quantization with 16-bit - MidTread quantizer
    #

    #Step
    step = (max(t)-(min(t)))/(2**16)
    # Sine
    SineFullRangeSignal_MidTread = np.round(SineFullRangeSignal/step)
    SineFullRangeSignal_MidTread_reconstructed = SineFullRangeSignal_MidTread * step
    # Triangular
    TriangularSignalFullRange_MidTread = np.round(TriangularSignalFullRange/step)
    TriangularSignalFullRange_MidTread_reconstructed = TriangularSignalFullRange_MidTread * step
    # Audio
    AudioSignalFullRange_MidTread = np.round(AudioSignalFullRange/step)
    AudioSignalFullRange_MidTread_reconstructed = AudioSignalFullRange_MidTread * step



    #
    # uLaw Quantization with 8-bit
    #

    #Step
    A = 1
    mu = 2**8 - 1
    # Sine
    SineFullRangeSignal_uLaw = np.sign(SineFullRangeSignal) * (np.log(1+mu*np.abs(SineFullRangeSignal/A)))/np.log(mu+1)
    SineFullRangeSignal_uLaw_reconstructed = np.sign(SineFullRangeSignal_uLaw) * ( ((mu+1)**np.abs(SineFullRangeSignal_uLaw) - 1) / (mu) ) * A
    # Triangular
    TriangularSignalFullRange_uLaw = np.sign(TriangularSignalFullRange) * (np.log(1+mu*np.abs(TriangularSignalFullRange/A)))/np.log(mu+1)
    TriangularFullRangeSignal_uLaw_reconstructed = np.sign(TriangularSignalFullRange_uLaw) * ( ((mu+1)**np.abs(TriangularSignalFullRange_uLaw) - 1) / (mu) ) * A
    # Audio
    AudioSignalFullRange_uLaw = np.sign(AudioSignalFullRange) * (np.log(1+mu*np.abs(AudioSignalFullRange/A)))/np.log(mu+1)
    AudioFullRangeSignal_uLaw_reconstructed = np.sign(AudioSignalFullRange_uLaw) * ( ((mu+1)**np.abs(AudioSignalFullRange_uLaw) - 1) / (mu) ) * A


    #
    #
    # 20db Under Full-Range
    #
    #

    # Signals
    # Sine
    SineFullRangeSignal = 0.1 * np.sin(2*np.pi*f_sine*t)
    # Triangular
    TriangularSignalFullRange = 0.1 * signal.sawtooth(2*np.pi*f_triangle*t)
    # Audio
    # open the file for reading.
    audioPath = "AdvancedDSP\Labs\Lab1\ImperialMarch_12.wav"
    a = AudioFile(audioPath)
    AudioSignalFullRange = a.extract() / 10
    
    #
    # Uniform Quantization with 16-bit - MidRise quantizer
    #

    #Step
    # step = (1-(-1))/(2**16)
    step = (max(t)-(min(t)))/(2**16)
    # Sine
    SineFullRangeSignal_MidRise = np.floor(SineFullRangeSignal/step)
    SineFullRangeSignal_MidRise_reconstructed = SineFullRangeSignal_MidRise * step
    # Triangular
    TriangularSignalFullRange_MidRise = np.floor(TriangularSignalFullRange/step)
    TriangularSignalFullRange_MidRise_reconstructed = TriangularSignalFullRange_MidRise * step
    # Audio
    AudioSignalFullRange_MidRise = np.floor(AudioSignalFullRange/step)
    AudioSignalFullRange_MidRise_reconstructed = AudioSignalFullRange_MidRise * step


    #
    # Uniform Quantization with 16-bit - MidTread quantizer
    #

    #Step
    step = (max(t)-(min(t)))/(2**16)
    # Sine
    SineFullRangeSignal_MidTread = np.round(SineFullRangeSignal/step)
    SineFullRangeSignal_MidTread_reconstructed = SineFullRangeSignal_MidTread * step
    # Triangular
    TriangularSignalFullRange_MidTread = np.round(TriangularSignalFullRange/step)
    TriangularSignalFullRange_MidTread_reconstructed = TriangularSignalFullRange_MidTread * step
    # Audio
    AudioSignalFullRange_MidTread = np.round(AudioSignalFullRange/step)
    AudioSignalFullRange_MidTread_reconstructed = AudioSignalFullRange_MidTread * step


    #
    # uLaw Quantization with 8-bit
    #

    #Step
    A = 1
    mu = 2**8 - 1
    # Sine
    SineFullRangeSignal_uLaw = np.sign(SineFullRangeSignal) * (np.log(1+mu*np.abs(SineFullRangeSignal/A)))/np.log(mu+1)
    SineFullRangeSignal_uLaw_reconstructed = np.sign(SineFullRangeSignal_uLaw) * ( ((mu+1)**np.abs(SineFullRangeSignal_uLaw) - 1) / (mu) ) * A
    # Triangular
    TriangularSignalFullRange_uLaw = np.sign(TriangularSignalFullRange) * (np.log(1+mu*np.abs(TriangularSignalFullRange/A)))/np.log(mu+1)
    TriangularFullRangeSignal_uLaw_reconstructed = np.sign(TriangularSignalFullRange_uLaw) * ( ((mu+1)**np.abs(TriangularSignalFullRange_uLaw) - 1) / (mu) ) * A
    # Audio
    AudioSignalFullRange_uLaw = np.sign(AudioSignalFullRange) * (np.log(1+mu*np.abs(AudioSignalFullRange/A)))/np.log(mu+1)
    AudioFullRangeSignal_uLaw_reconstructed = np.sign(AudioSignalFullRange_uLaw) * ( ((mu+1)**np.abs(AudioSignalFullRange_uLaw) - 1) / (mu) ) * A

 

    #
    #
    # SNR
    #
    #

    # MidRise
    SineFullRangeSignal_MidRise_Error = SineFullRangeSignal_MidRise_reconstructed - SineFullRangeSignal
    SineFullRangeSignal_MidRise_SNR = SNR(SineFullRangeSignal_MidRise_reconstructed, SineFullRangeSignal_MidRise_Error)
    print("Sine Full Range MidRise Quantization Reconstructed Signal SNR: " , SineFullRangeSignal_MidRise_SNR, "[dB]")
    TriangularSignalFullRange_MidRise_Error = TriangularSignalFullRange_MidRise_reconstructed - TriangularSignalFullRange
    TriangularFullRangeSignal_MidRise_SNR = SNR(TriangularSignalFullRange_MidRise_reconstructed, TriangularSignalFullRange_MidRise_Error)
    print("Triangular Full Range MidRise Quantization Reconstructed Signal SNR: " , TriangularFullRangeSignal_MidRise_SNR, "[dB]")
    AudioSignalFullRange_MidRise_Error = AudioSignalFullRange_MidRise_reconstructed - AudioSignalFullRange_MidRise
    AudioFullRangeSignal_MidRise_SNR = SNR(AudioSignalFullRange_MidRise_reconstructed, AudioSignalFullRange_MidRise_Error)
    print("Audio Full Range MidRise Quantization Reconstructed Signal SNR: " , AudioFullRangeSignal_MidRise_SNR, "[dB]")
    print("\n")

    
    # MidTread
    SineFullRangeSignal_MidTread_Error = SineFullRangeSignal_MidTread_reconstructed - SineFullRangeSignal
    SineFullRangeSignal_MidTread_SNR = SNR(SineFullRangeSignal_MidTread_reconstructed, SineFullRangeSignal_MidTread_Error)
    print("Sine Full Range MidTread Quantization Reconstructed Signal SNR: " , SineFullRangeSignal_MidTread_SNR, "[dB]")
    TriangularSignalFullRange_MidTread_Error = TriangularSignalFullRange_MidTread_reconstructed - TriangularSignalFullRange
    TriangularFullRangeSignal_MidTread_SNR = SNR(TriangularSignalFullRange_MidTread_reconstructed, TriangularSignalFullRange_MidTread_Error)
    print("Triangular Full Range MidTread Quantization Reconstructed Signal SNR: " , TriangularFullRangeSignal_MidTread_SNR, "[dB]")
    AudioSignalFullRange_MidTread_Error = AudioSignalFullRange_MidTread_reconstructed - AudioSignalFullRange_MidTread
    AudioFullRangeSignal_MidTread_SNR = SNR(AudioSignalFullRange_MidTread_reconstructed, AudioSignalFullRange_MidTread_Error)
    print("Audio Full Range MidTread Quantization Reconstructed Signal SNR: " , AudioFullRangeSignal_MidTread_SNR, "[dB]")
    print("\n")

    # uLaw
    SineFullRangeSignal_uLaw_Error = SineFullRangeSignal_uLaw_reconstructed - SineFullRangeSignal
    SineFullRangeSignal_uLaw_SNR = SNR(SineFullRangeSignal_uLaw_reconstructed, SineFullRangeSignal_uLaw_Error)
    print("Sine Full Range uLaw Quantization Reconstructed Signal SNR: " , SineFullRangeSignal_uLaw_SNR, "[dB]")
    TriangularSignalFullRange_uLaw_Error = TriangularFullRangeSignal_uLaw_reconstructed - TriangularSignalFullRange
    TriangularFullRangeSignal_uLaw_SNR = SNR(TriangularFullRangeSignal_uLaw_reconstructed, TriangularSignalFullRange_uLaw_Error)
    print("Triangular Full Range uLaw Quantization Reconstructed Signal SNR: " , TriangularFullRangeSignal_uLaw_SNR, "[dB]")
    AudioSignalFullRange_uLaw_Error = AudioFullRangeSignal_uLaw_reconstructed - AudioSignalFullRange_uLaw
    AudioFullRangeSignal_uLaw_SNR = SNR(AudioFullRangeSignal_uLaw_reconstructed, AudioSignalFullRange_uLaw_Error)
    print("Audio Full Range uLaw Quantization Reconstructed Signal SNR: " , AudioFullRangeSignal_uLaw_SNR, "[dB]")




#
# main
#
if __name__ == "__main__":
    Task1()
    Task2()
    Task3()
