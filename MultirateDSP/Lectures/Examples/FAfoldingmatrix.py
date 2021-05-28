import numpy as np

def Famatrix(h):
    """produces a diamond shaped folding matrix Fa from the coefcients h
    (h is a row matrix)
    """
    N = int(len(h)/2)
    print("Famatrix N=", N)
    #fiplr:
    h=h[::-1]
    Fa=np.zeros((N,N,1))
    # Fa[0:int(N/2),0:int(N/2),0]=-np.fiplr(np.diag(h[0:int(N/2)]))
    # Fa[int(N/2):N,0:int(N/2),0]=-np.diag(h[int(N/2):N])
    # Fa[0:int(N/2),int(N/2):N,0]=-np.diag(h[N:(N+int(N/2))])
    # Fa[int(N/2):N,int(N/2):N,0]=np.fiplr(np.diag(h[(N+int(N/2)):2*N]))
    return Fa