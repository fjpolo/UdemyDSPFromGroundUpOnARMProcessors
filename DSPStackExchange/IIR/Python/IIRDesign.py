# https://dsp.stackexchange.com/questions/59688/how-to-design-a-digital-filter-in-python-that-will-run-over-an-uc

from scipy.signal import butter, freqz
import matplotlib.pyplot as plt
from math import pi
import numpy as np

f_s = 48000    # Sample frequency in Hz
# f_c = 10000     # Cut-off frequency in Hz
f_c = 5000     # Cut-off frequency in Hz
# f_c = 2000     # Cut-off frequency in Hz
order = 4    # Order of the butterworth filter

omega_c = 2 * pi * f_c       # Cut-off angular frequency
omega_c_d = omega_c / f_s    # Normalized cut-off frequency (digital)

# Design the digital Butterworth filter
b, a = butter(order, omega_c_d / pi)    
print('Coefficients')
print("b =", b)                           # Print the coefficients
print("a =", a)

# fc 10kHz
# b = [0.05298685 0.21194742 0.31792113 0.21194742 0.05298685]
# a = [ 1.         -0.65147165  0.62047212 -0.14737946  0.02616866]

# fc 5kHz
# b = [0.00554177 0.02216707 0.03325061 0.02216707 0.00554177]
# a = [ 1.         -2.30244827  2.20908011 -0.99219366  0.1742301 ]

# fc 2kHz
# b = [0.00021314 0.00085255 0.00127883 0.00085255 0.00021314]
# a = [ 1.         -3.31680791  4.17424555 -2.35740278  0.50337536]


#
w, H = freqz(b, a, 4096)                  # Calculate the frequency response
w *= f_s / (2 * pi)                       # Convert from rad/sample to Hz

# Plot the amplitude response
plt.subplot(2, 1, 1)            
plt.suptitle('Bode Plot')
H_dB = 20 * np.log10(abs(H))              # Convert modulus of H to dB
plt.plot(w, H_dB)
plt.ylabel('Magnitude [dB]')
plt.xlim(0, f_s / 2)
plt.ylim(-80, 6)
plt.axvline(f_c, color='red')
plt.axhline(-3, linewidth=0.8, color='black', linestyle=':')

# Plot the phase response
plt.subplot(2, 1, 2)
phi = np.angle(H)                         # Argument of H
phi = np.unwrap(phi)                      # Remove discontinuities 
phi *= 180 / pi                           # and convert to degrees
plt.plot(w, phi)
plt.xlabel('Frequency [Hz]')
plt.ylabel('Phase [°]')
plt.xlim(0, f_s / 2)
plt.ylim(-360, 0)
plt.yticks([-360, -270, -180, -90, 0])
plt.axvline(f_c, color='red')
# Show plot
plt.show()