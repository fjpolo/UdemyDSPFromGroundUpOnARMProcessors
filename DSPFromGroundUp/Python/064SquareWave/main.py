from scipy import signal
import matplotlib.pyplot as plt
import numpy as np

t = np.linspace(0, 1, 500, endpoint=False)
f = 5
square = signal.square(2*np.pi*f*t)
sine = np.sin(2*np.pi*t)
pwm = signal.square(2*np.pi*30*t, duty=((sine+1)/2))
plt.subplot(2,1,1)
plt.plot(t, sine)
plt.subplot(2,1,2)
plt.plot(t, pwm)
plt.show()