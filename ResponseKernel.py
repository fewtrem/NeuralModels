'''
Created on 19 Jan 2016

@author: s1144899
'''
import numpy as np, math
# The response kernel function for inputs (representing the synaptic time constants)
class ResponseKernel():
    # REF to a model class
    networkC = None
    # local response kernel properties (Dictionary)
    params = None
    '''
    responseLimit a calculated response limit! (Double)
    type (String)
    Gamma Type:
    theta Gamma distribution theta variable (Double)
    average Gamma distribution mean variable (Double)
    '''

    def __init__(self,networkC,params):
        self.networkC = networkC
        self.params = params
        print "WARNING: No specific initiation method implemted for the response Kernel!"
    def getVal(self):
        print "WARNING: Returning zero as not implemented"
        return 0
    def getValVec(self):
        print "WARNING: Returning zero as not implemented"
        return np.zeros(0)
    def setResponseLimit(self,sym,limit=1.0):
        x = 0.0
        cdf = 0.0
        lim = self.networkC.params['responseLimitCDF']*limit
        if sym == True:
            lim = lim/2
        while cdf<lim:
            cdf += self.getVal(x)*self.networkC.params['dt']
            x+=self.networkC.params['dt']
        return x
    def setNormFactor(self):
        # Get the normalisation:
        sumV = 1E-20
        xi = 0
        dx = self.networkC.params['normFactorDX']
        percdiff = 1.0
        prevVal = -1E20
        while(percdiff>1E-8 or percdiff<0):
            newV = self.getVal(xi)
            percdiff = (prevVal-newV)/sumV
            sumV+=newV*dx
            xi+=dx
            prevVal = newV
        print sumV," at ",xi
        self.params['normFactor'] = self.params['normFactor']/sumV
        print "Set a normalising factor as: ",self.params['normFactor']
def setResponseKernel(networkC,params):
    checkType = True
    try:
        params['type']
    except:
        checkType = False
    if checkType == True:    
        if params['type'] == "gamma":
            return ResponseKernel_Gamma(networkC,params)
        if params['type'] == "STDP":
            return ResponseKernel_STDP(networkC,params)
        if params['type'] == "PSD":
            return ResponseKernel_PSD(networkC,params)
        if params['type'] == "exDecay":
            return ResponseKernel_ExDecay(networkC,params)
        else:
            print "WARNING: Response Kernel not set"
            return None
    else:
        print "WARNING: Response Kernel not set"
        return None

class ResponseKernel_Gamma(ResponseKernel) :
    def __init__(self,networkC,params):
        self.networkC = networkC
        self.params = params
        self.responseLimit = self.setResponseLimit(False)
        self.getVectorFunc = np.vectorize(self.gammaDist,excluded=['self'])
    def gammaDist(self,x):
        beta = 1.0/self.params['theta']
        alpha = self.params['average']*beta
        return  np.power(beta,alpha)*np.power(x,alpha-1)*np.exp(-x*beta)/math.gamma(alpha)
    def getVal(self,x):
        return self.gammaDist(x)
    
    
class ResponseKernel_STDP(ResponseKernel) :
    def __init__(self,networkC,params):
        self.networkC = networkC
        self.params = params
        self.responseLimit = self.setResponseLimit(True)
        self.getVectorFunc = np.vectorize(self.STDPDist,excluded=['self'])
    def STDPDist(self,x):
        beta = self.params['beta']
        # Is NOT already normalised - need to multiply by 2*beta
        #return  2*beta*x*np.power(np.e,-beta*x*x)
        # Normalise for initial integration!
        return 1/12.0*np.power(beta,4.0)*x*np.power(np.e,-beta*np.power(np.abs(x),0.5))

    def getVal(self,x):
        return self.STDPDist(x)

  
class ResponseKernel_PSD(ResponseKernel):   
    def __init__(self,networkC,params):
        self.networkC = networkC
        self.params = params
        self.params['normFactor'] = 1.0
        self.setNormFactor()
        self.responseLimit = self.setResponseLimit(False)
        self.getVectorFunc = np.vectorize(self.psdDist,excluded=['self'])
    def psdDist(self,x):
        average = self.params['average']
        theta = self.params['theta']
        beta = theta/average
        norm = self.params['normFactor']
        return  beta*beta*norm*np.power(x,theta)*np.power(np.e,-x*beta)
    def getVal(self,x):
        return self.psdDist(x)
    
# http://icwww.epfl.ch/~gerstner/SPNM/node27.html, 4.31 where Theta() is the heaviside step function.
class ResponseKernel_ExDecay(ResponseKernel):   
    def __init__(self,networkC,params):
        self.params = params
        try:
            self.params['timeConst']
        except:
            self.params['timeConst'] = 1.0
            print "No time constant [timeConst] of decay for ",self.params['name']," so setting to 1.0"
        try:
            self.params['mult']
        except:
            self.params['mult'] = 1.0
            print "No decay scaler [mult] for ",self.params['name']," so setting to 1.0"
        self.networkC = networkC

        self.params['timeConstDiv'] = 1.0/self.params['timeConst']
        self.responseLimit = self.setResponseLimit(False,self.params['mult']*self.params['timeConst'])
        self.getVectorFunc = np.vectorize(self.exDist,excluded=['self'])

    def exDist(self,x):
        tauDiv = self.params['timeConstDiv']
        mult = self.params['mult']
        return  mult*np.power(np.e,-x*tauDiv)
    def getVal(self,x):
        return self.exDist(x)
    
# http://icwww.epfl.ch/~gerstner/SPNM/node27.html, 4.32 where Theta() is the heaviside step function.
# REquires only input spikes SINCE LAST SPIKE to be input....
class ResponseKernel_LinearPSDResponse(ResponseKernel):   
    def __init__(self,networkC,params):
        self.undefined = 0
    def psdDist(self,x):
        return 0
    def getVal(self,x):
        return 0
'''
class testMod:
    params={'dt':0.001,'responseLimitCDF':0.99,'normFactorDX':0.001}
#TEST
import matplotlib.pyplot as plt
t = np.arange(0.0, 2.0, 0.001)
r = ResponseKernel_PSD(testMod,{"average":0.1,"theta":1.0})
s = map(r.psdDist,t)
plt.plot(t, s)
g = ResponseKernel_PSD(testMod,{"average":0.1,"theta":2.0})
s = map(g.psdDist,t)
plt.plot(t, s)
plt.show()
'''
    
'''    
#TEST the response limit:
globalsM = {'dt':0.01,'responseLimitCDF':0.99}
r = ResponseKernel_Gamma(globalsM,{"average":9.0,"theta":1.0})
print r.responseLimit
'''
'''
class testMod:
    params={'dt':0.0001,'responseLimitCDF':0.99,'normFactorDX':0.001}
#TEST
import matplotlib.pyplot as plt
t = np.arange(0.0, 2.0, 0.001)
r = ResponseKernel_ExDecay(testMod,{"timeConst":0.1,"mult":1.0})
s = map(r.exDist,t)
plt.plot(t, s)
g = ResponseKernel_ExDecay(testMod,{"timeConst":0.1,"mult":2.0})
s = map(g.exDist,t)
plt.plot(t, s)
plt.show()
'''