from scipy import signal
import numpy as np


# System H(s) = 5(s-1)(s-2)/(s-3)(s-4)

simple_lti = signal.ZerosPolesGain([1,2],[3,4],5)

simple_dlti = signal.ZerosPolesGain([1,2],[3,4],5,dt=0.1)

print("Simple LTI :")
print(simple_lti)

print("Simple dLTI : ")
print(simple_dlti)
