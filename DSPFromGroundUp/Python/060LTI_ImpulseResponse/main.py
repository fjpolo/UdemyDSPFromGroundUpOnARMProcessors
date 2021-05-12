from scipy import signal
import matplotlib.pyplot as plt
import numpy as np


#Transfer function H(s) = s^2/s^3+2s^2+s

system=([1],[1,2,1])
t,y=signal.impulse(system)
plt.plot(t,y)
plt.show()
