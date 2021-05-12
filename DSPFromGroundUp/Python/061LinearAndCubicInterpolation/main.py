import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from matplotlib import style


x = np.linspace(0,4,12)
y = np.cos(x**2/3+4)

f1 = interp1d(x,y,kind='linear')
f2 = interp1d(x,y,kind ='cubic')


xnew = np.linspace(0,4,30)
plt.plot(x,y,'o',xnew,f1(xnew),'-',xnew,f2(xnew),'--')
plt.legend(['data','linear','cubic'], loc ='best')

plt.show()
