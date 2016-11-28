'''
Created on 3 Jul 2016

@author: fewtrem
'''
import numpy as np, math
def psdDist(x,average,thetaIn,norm):
    beta = thetaIn/average
    theta = thetaIn
    return  beta*beta/norm*np.power(x,theta)*np.power(np.e,-x*beta)

import matplotlib.pyplot as plt

def addToPlot(Vaverage,Vtheta):
    # Get the normalisation:
    sumV = 0.00000001
    xi = 0
    dx = 0.001
    percdiff = 1.0
    prevVal = -1E100
    while(percdiff>0.001 or percdiff<0):
        newV = psdDist(xi,Vaverage,Vtheta,1)
        percdiff = (prevVal-newV)/sumV
        sumV+=newV*dx
        xi+=dx
        prevVal = newV
    print "normalising factor is: ",sumV
    t = np.arange(0,0.1,0.001)
    s = psdDist(t,Vaverage,Vtheta,sumV)
    plt.plot(t, s)

#addToPlot(0.005,0.0049)
#addToPlot(0.01,0.009)
addToPlot(0.002,5)
#addToPlot(0.05,5)
'''
for i in range(5,10,1):
    addToPlot(0.01*i,0.1)
'''
plt.show()