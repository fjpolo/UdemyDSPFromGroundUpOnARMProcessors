from scipy import signal
import numpy as np


#Transfer function H(s) s^2+3s+3 /s^2+2s+1


num =[1,3,3]
den =[1,2,1]

H1 = signal.TransferFunction(num,den)
print(H1)

#Tranfer function(discrete) with a samplying rate of 0.1 second
# H(s) = z^2 + 3z + 3 / z^2 +2z +1

H2 = signal.TransferFunction(num, den,dt=0.1)
print(H2)
