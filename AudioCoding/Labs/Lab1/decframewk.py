from scipy.io import wavfile
import soundfile
import pickle
import numpy as np

#
def decframewk_Read32PCM(LoadPath, wavPath, samplerate):
    """
    """
    # Load from pickle
    with open(LoadPath,'rb') as f: array = pickle.load(f)
    # Save to wav file
    wavfile.write(wavPath, samplerate, array)

#
def decframewk_Read16PCM(LoadPath, wavPath, samplerate):
    """
    """
    # Load from pickle
    with open(LoadPath,'rb') as f: array = pickle.load(f)
    # Save to wav file
    wavfile.write(wavPath, samplerate, array)

#
def decframewk_Read8PCM(LoadPath, wavPath, samplerate):
    """
    """
    # Load from pickle
    with open(LoadPath,'rb') as f: array = pickle.load(f)
    # Save to wav file
    wavfile.write(wavPath, samplerate, array)