from scipy.io import wavfile
import soundfile
import pickle
import numpy as np

#
def encframewk_Read32PCM(FilePath, SavePath):
    """
    Reads file audio file and stores the samples with 32 bit per sample in a binary file file.bin.-
    """
    # Read
    samplerate, data = wavfile.read(FilePath)
    # Compress
    compressed_data = np.int32(data/np.max(np.abs(data)) * (2**32)) 
    # Save
    with open(SavePath,'wb') as f: pickle.dump(compressed_data, f)
    #
    return samplerate

#
def encframewk_Read16PCM(FilePath, SavePath):
    """
    Reads file audio file and stores the samples with 16 bit per sample in a binary file file.bin.-
    """
    # Read
    samplerate, data = wavfile.read(FilePath)
    # Compress
    compressed_data = np.int16(data/np.max(np.abs(data)) * (2**16)) 

    # Save
    with open(SavePath,'wb') as f: pickle.dump(compressed_data, f)
    #
    return samplerate

#
def encframewk_Read8PCM(FilePath, SavePath):
    """
    Reads file audio file and stores the samples with 8 bit per sample in a binary file file.bin.-
    """
    # Read
    samplerate, data = wavfile.read(FilePath)
    # Compress
    compressed_data = np.int8(data/np.max(np.abs(data)) * (2**8)) 
    # Save
    with open(SavePath,'wb') as f: pickle.dump(compressed_data, f)
    #
    return samplerate