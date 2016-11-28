'''
Created on 3 Jul 2016

@author: fewtrem
'''
import numpy as np, math
import matplotlib.pyplot as plt
def hhDist(V,k,V_half,ENA):
    return  (V-ENA)/(1.0+np.power(np.e,((V_half-V)/k)))



def addToPlot(k,V_half,ENA):
    # Get the normalisation:
    sumV = 0.00000001
    '''
    xi = 0
    dx = 0.001
    percdiff = 1.0
    prevVal = -1E100
    while(percdiff>0.001 or percdiff<0):
        newV = hhDist(xi,Vaverage,Vtheta,1)
        percdiff = (prevVal-newV)/sumV
        sumV+=newV*dx
        xi+=dx
        prevVal = newV
    print "normalising factor is: ",sumV
    '''
    vfunc = np.vectorize(hhDist)
    t = np.arange(-100,100,0.01)
    s = vfunc(t,k,V_half,ENA)
    plt.plot(t, s)

#addToPlot(0.005,0.0049)
#addToPlot(0.01,0.009)
addToPlot(15,-20,60)
#addToPlot(0.05,5)
'''
for i in range(5,10,1):
    addToPlot(0.01*i,0.1)
'''
plt.show()