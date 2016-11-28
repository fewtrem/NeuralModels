'''
Created on 18 Feb 2016

@author: s1144899
'''
import numpy as np, math
def STDPDist(x,beta):
    #return  x/(5*np.power(x,2)+1)
    # Old function (too symetrical peak)
    #return  x*np.power(np.e,-beta*x*x)
    return x*np.power(np.e,-beta*np.power(np.abs(x),0.5))


import matplotlib.pyplot as plt

def addToPlot(beta):
    t = np.arange(-0.5,0.5,0.001)
    s = STDPDist(t,beta)
    plt.plot(t, s)
    sums = 0.0
    for ns in np.arange(0,0.5,0.0001):
        sums+=STDPDist(ns,beta)*0.0001
    print sums
    print 12.0/np.power(beta,4)
        

addToPlot(20)



'''
for i in range(5,10,1):
    addToPlot(0.01*i,0.1)
'''
plt.show()
