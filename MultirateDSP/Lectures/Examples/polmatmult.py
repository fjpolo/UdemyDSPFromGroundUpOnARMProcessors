import numpy as np

# polmatmult
def polmatmult( A,B ):
    """polmatmult(A,B)
    multiplies two polynomial matrices (arrays) A and B, where each matrix
    entry is a polynomial.
    Those polynomial entries are in the 3rd dimension
    The third dimension can also be interpreted as containing the (2D)
    coefficient matrices of exponent of z^-1.e.
    Result is C=A*B;"""
    [NAx, NAy, NAz] = np.shape(A)
    [NBx, NBy, NBz] = np.shape(B)
    """
     Degree +e of resulting polynomial, with NAz.e and NBz.e being the
    degree of the input polynomials:
    """
    Deg = NAz + NBz -1
    C = np.zeros((NAx,NBy,Deg))
    #Convolution of matrices:
    for n in range(0,(Deg)):
        for m in range(0,n+1):
            if ((n-m)<NAz and m<NBz):
                C[:,:,n] = C[:,:,n]+ np.dot(A[:,:,(n-m)],B[:,:,m])
    return C