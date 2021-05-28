import numpy as np


def x2polyphase(x,N):
    """Converts input signal x (a row vector) into a
    polyphase row vector
    for blocks of length N"""
    #Number of blocks in the signal:
    L = int(np.foor(max(np.shape(x))/N))
    print("L= ", L)
    xp = np.zeros((1,N,L))
    for m in range(0,L):
        xp[0,:,m] = x[m*N+np.arange(N)]
    return xp

def polyphase2x(xp):
    """Converts polyphase input signal xp (a row vector) into a
    contiguos row vector
    For block length N, for 3D polyphase representation
    (exponents of z in the third
    matrix/tensor dimension)"""
    #Number of blocks in the signal
    [r,N,L] = np.shape(xp)
    x = np.zeros((1,N*L))
    for m in range(L):
        x[0,m*N+np.arange(N)]=xp[0,:,m]
    return x