'''
Created on 18 Feb 2016

@author: s1144899
'''
import numpy as np, math
def gammaDist(x,average,theta,):
    beta = 1.0/theta
    alpha = average*beta
    return  np.power(beta,alpha)*np.power(x,alpha-1)*np.exp(-x*beta)/math.gamma(alpha)

import matplotlib.pyplot as plt

def addToPlot(Vaverage,Vtheta):
    t = np.arange(0,0.2,0.001)
    s = gammaDist(t,Vaverage,Vtheta)
    plt.plot(t, s)

#addToPlot(0.005,0.0049)
addToPlot(0.01,0.004)
addToPlot(0.05,0.02)
addToPlot(0.05,0.005)
'''
for i in range(5,10,1):
    addToPlot(0.01*i,0.1)
'''
plt.show()
