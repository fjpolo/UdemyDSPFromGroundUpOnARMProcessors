from scipy import signal
import matplotlib.pyplot as plt
import numpy as np

s1 = signal.lti([],[1,1,1],[5])

w,H=signal.freqresp(s1)

#Complex plot

plt.plot(H.real,H.imag,"b")
plt.plot(H.real,-H.imag,"r")

plt.show()

  
