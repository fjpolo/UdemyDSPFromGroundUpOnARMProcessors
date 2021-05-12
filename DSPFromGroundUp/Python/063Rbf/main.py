from scipy.interpolate import InterpolatedUnivariateSpline,Rbf
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import style



x = np.linspace(0,10,9)
y = np.sin(x)

xi = np.linspace(0,10,101)

spl =InterpolatedUnivariateSpline(x,y)
y_spl = spl(xi)

rbf = Rbf(x,y)
y_rbf = rbf(xi)


plt.subplot(2,1,1)
plt.plot(x,y,'bo')
plt.plot(xi,y_spl,'g')
plt.title('Interplotion using univriate spine')

plt.subplot(2,1,2)
plt.plot(x,y,'bo')
plt.plot(xi,y_rbf,'r')
plt.title('Interplotion usingRBF-multiquadrics')
plt.show()
