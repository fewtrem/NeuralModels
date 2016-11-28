'''
Created on 18 Jan 2016

@author: s1144899

In this simulation we aim to select the direction from a noisy background.

'''

# create neurons:
from Connection import Connection
import numpy as np,copy
import ResponseKernel
class Neuron:
    # The link to this network class
    networkC = None

    # This neuron's params VARIABLE VALUES THAT CAN BE PICKLED/JSONED etc. (not copied!)
    params = None
    '''
    'name' (String)
    'id' (int)
    'spikeOuts' (List of Doubles)
    'inateProb' (double)
    '''
    def __init__(self,networkC,params):
        # Store links to connection classes!
        self.connectionsOut = []
        self.connectionsIn = []
        self.params = params
        self.networkC = networkC
        try:
            self.params['name']
        except:
            self.params['name'] = "Untitled Neuron "+str(self.params['id'])+" (Undefined Type)"
        print "Warning: Neuron not setting parameters"
    def update(self,curT):
        print "Warning: Neuron does not implement method for updating!"
    # Input must be Connection class!
    def addOutput(self,ConnIn):
        if isinstance(ConnIn,Connection):
            self.connectionsOut.append(ConnIn)
        else:
            print "Warning: Connection not added as not connection!"
    # Input must be Connection class!
    def addInput(self,ConnIn):
        if isinstance(ConnIn,Connection):
            self.connectionsIn.append(ConnIn)
        else:
            print "Warning: Connection not added as not connection!"
    def getParams(self):
        return self.params
    
# Poisson neuron...
class PoissonNeuron(Neuron):
    def __init__(self,networkC,params):
        self.params = params
        self.networkC = networkC
        self.connectionsOut = []
        self.connectionsIn = []
        try:
            self.params['name']
        except:
            self.params['name'] = "Untitled Neuron id:"+str(self.params['id'])+" (Poisson)"
        try:
            self.params['spikeOuts']
        except:
            self.params['spikeOuts'] = []
        try:
            self.params['actVals']
        except:
            self.params['actVals'] = []
        try:
            self.params['recordAct']
        except:
            self.params['recordAct'] = False
        try:
            self.params['exScale']
        except:
            self.params['exScale'] = 1
            print "No scale direction defined for ",self.params['name']," so setting as excitatory"
            
            
    def update(self,curT):
        # calculate inputs from input's outputs... (i.e. calculate the presynaptic activity)
        # Go through all incoming connections:
        curAct = copy.deepcopy(self.params['inateProb'])
        for inputC in self.connectionsIn:
            curAct += inputC.getCurExVec(curT,False,0.0)
        if self.params['recordAct'] == True:
            self.params['actVals'].append([curT,curAct]) 
        # Now add to probability and determine what we are doing...
        # probability is that it will spike per unit of time,
        curProb = curAct*self.networkC.params['dt']
        if curProb > 1:
            print "Warning: Prob of spiking very high, higher than resolution dt allows!"
        if np.random.random()<curProb:
            self.params['spikeOuts'].append(curT)
            #print "spike from ",self.params['name']," at ",curT
            #Update the weights now we have a spike:
            # go through the list of connections and update them based on previous spikes
            # Initially we will assume that the updates happen instantaneously!
            for conn in self.connectionsOut:
                conn.updateWeights(curT,True)
            for conn in self.connectionsIn:
                conn.updateWeights(curT,False)

# LIF neuron...
class LIFNeuron(Neuron):
    def __init__(self,networkC,params):
        self.params = params
        self.networkC = networkC
        self.connectionsOut = []
        self.connectionsIn = []
        try:
            self.params['name']
        except:
            self.params['name'] = "Untitled Neuron id:"+str(self.params['id'])+" (LIF)"
        try:
            self.params['spikeOuts']
        except:
            self.params['spikeOuts'] = []
        try:
            self.params['actVals']
        except:
            self.params['actVals'] = []
        try:
            self.params['recordAct']
        except:
            self.params['recordAct'] = False
        try:
            self.params['thresh']
        except:
            self.params['thresh'] = 1.0
            print "No threshold for ",self.params['name']," so setting to 1.0"
        try:
            self.params['exScale']
        except:
            self.params['exScale'] = 1
            print "No scale direction defined for ",self.params['name']," so setting as excitatory"
            
    def update(self,curT):
        # calculate inputs from input's outputs... (i.e. calculate the presynaptic activity)
        # Go through all incoming connections:
        theLen = len(self.params['spikeOuts'])
        if theLen>0:
            lastSpikeT = self.params['spikeOuts'][theLen-1]
        else:
            lastSpikeT = 0.0
        curAct = 0.0
        for inputC in self.connectionsIn:
            curAct += inputC.getCurExVec(curT,True,lastSpikeT)
        if self.params['recordAct'] == True:
            self.params['actVals'].append([curT,curAct])
            
        if curAct>self.params['thresh']:
            self.params['spikeOuts'].append(curT)
            #print "spike from ",self.params['name']," at ",curT
            #Update the weights now we have a spike:
            # go through the list of connections and update them based on previous spikes
            # Initially we will assume that the updates happen instantaneously!
            for conn in self.connectionsOut:
                conn.updateWeights(curT,True)
            for conn in self.connectionsIn:
                conn.updateWeights(curT,False)

# Spike Response Model neuron...
class SRMNeuron(Neuron):
    def __init__(self,networkC,params):
        self.params = params
        self.networkC = networkC
        self.connectionsOut = []
        self.connectionsIn = []
        try:
            self.params['name']
        except:
            self.params['name'] = "Untitled Neuron id:"+str(self.params['id'])+" (SRM)"
        try:
            self.params['spikeOuts']
        except:
            self.params['spikeOuts'] = []
        try:
            self.params['actVals']
        except:
            self.params['actVals'] = []
        try:
            self.params['recordAct']
        except:
            self.params['recordAct'] = False
        try:
            self.params['thresh']
        except:
            self.params['thresh'] = 1.0
            print "No minimum threshold [thresh] for ",self.params['name']," so setting to 1.0"
        try:
            self.params['exScale']
        except:
            self.params['exScale'] = 1
            print "No scale direction defined for ",self.params['name']," so setting as excitatory"
        self.exResponseKernel = ResponseKernel.setResponseKernel(networkC,params['responseKernel'])
            
    def update(self,curT):
        # calculate inputs from input's outputs... (i.e. calculate the presynaptic activity)
        # Go through all incoming connections:
        theLen = len(self.params['spikeOuts'])
        if theLen>0:
            lastSpikeT = self.params['spikeOuts'][theLen-1]
        else:
            lastSpikeT = 0.0
        curAct = 0.0
        for inputC in self.connectionsIn:
            curAct += inputC.getCurExVec(curT,True,lastSpikeT)
        if self.params['recordAct'] == True:
            self.params['actVals'].append([curT,curAct])
        # Calculate the current threshold: using the kernel:
        curThresh = self.exResponseKernel.exDist(curT-lastSpikeT)
        if curAct>curThresh:
            self.params['spikeOuts'].append(curT)
            #print "spike from ",self.params['name']," at ",curT
            #Update the weights now we have a spike:
            # go through the list of connections and update them based on previous spikes
            # Initially we will assume that the updates happen instantaneously!
            for conn in self.connectionsOut:
                conn.updateWeights(curT,True)
            for conn in self.connectionsIn:
                conn.updateWeights(curT,False)
        # Update the potential
        

# Poisson neuron...
class ConstantRateNeuron(Neuron):
    def __init__(self,networkC,params):
        self.params = params
        self.networkC = networkC
        self.connectionsOut = []
        self.connectionsIn = []
        try:
            self.params['name']
        except:
            self.params['name'] = "Untitled Constant Rate Neuron id:"+str(self.params['id'])+" (Poisson)"
        try:
            self.params['spikeOuts']
        except:
            self.params['spikeOuts'] = []
        try:
            self.params['actVals']
        except:
            self.params['actVals'] = []
        try:
            self.params['recordAct']
        except:
            self.params['recordAct'] = False
        try:
            self.params['thresh']
        except:
            self.params['thresh'] = 1.0
            print "No threshold for ",self.params['name']," so setting to 1.0"
        try:
            self.params['exScale']
        except:
            self.params['exScale'] = 1
            print "No scale direction defined for ",self.params['name']," so setting as excitatory"
            
    def update(self,curT):
        # calculate inputs from input's outputs... (i.e. calculate the presynaptic activity)
        # Go through all incoming connections:
        theLen = len(self.params['spikeOuts'])
        if theLen>0:
            lastSpikeT = self.params['spikeOuts'][theLen-1]
        else:
            lastSpikeT = 0.0
        curAct = 0
        if self.params['recordAct'] == True:
            self.params['actVals'].append([curT,curAct])
            
        if (curT-lastSpikeT)>self.params['spikeSep']:
            self.params['spikeOuts'].append(curT)
            #print "spike from ",self.params['name']," at ",curT
            #Update the weights now we have a spike:
            # go through the list of connections and update them based on previous spikes
            # Initially we will assume that the updates happen instantaneously!
            for conn in self.connectionsOut:
                conn.updateWeights(curT,True)
            for conn in self.connectionsIn:
                conn.updateWeights(curT,False)

#Page 89 of the green book, model neuron. 
'''
C - capacitance scalar for V changes
E_L - resting Potential
g_l = scalar for leaking
E_NA - Equilibrium pot for Na.
Na_actP - activation midpoint for Na channels.
Na_actW - activation width for Na channels.
g_Na - scalar for Na
E_K - Equilibrium pot for K
g_K - scalar for K
K_actP - activation midpoint for K channels.
K_actW - activation width for K channels.
K_t - delay for K
I - current in
'''
class P89Neuron(Neuron):
    def __init__(self,networkC,params):
        self.params = params
        self.networkC = networkC
        self.connectionsOut = []
        self.connectionsIn = []
        self.params['spikeRecorded'] = False
        self.params['n_K'] = 0
        self.params['V'] = self.params['E_L']
        try:
            self.params['name']
        except:
            self.params['name'] = "Untitled P98 Neuron id:"+str(self.params['id'])+" (Poisson)"
        try:
            self.params['spikeOuts']
        except:
            self.params['spikeOuts'] = []
        try:
            self.params['actVals']
        except:
            self.params['actVals'] = []
        try:
            self.params['vVals']
        except:
            self.params['vVals'] = []
        try:
            self.params['recordAct']
        except:
            self.params['recordAct'] = False
        try:
            self.params['recordV']
        except:
            self.params['recordV'] = False
        try:
            self.params['exScale']
        except:
            self.params['exScale'] = 1
            print "No scale direction defined for ",self.params['name']," so setting as excitatory"
        # move to equilibium:
    def pHStyleCurve(self,V,V_half,k):
        return 1.0/(1.0+np.power(np.e,((V_half-V)/k)))
    def update(self,curT):
        # calculate inputs from input's outputs... (i.e. calculate the presynaptic activity)
        # Go through all incoming connections:
        curAct = 0.0
        for inputC in self.connectionsIn:
            curAct += inputC.getCurExVec(curT,False,0.0)
        self.params['n_K']+= self.networkC.params['dt']*(self.pHStyleCurve(self.params['V'],self.params['K_actP'],self.params['K_actW'])-self.params['n_K'])/self.params['K_t']
        #print "n_K: ",self.params['n_K']
        self.params['V']+= self.networkC.params['dt']*(1/self.params['C'])*(self.params['I']\
                            -self.params['g_L']*(self.params['V']-self.params['E_L'])
                            -self.params['g_Na']*self.pHStyleCurve(self.params['V'],self.params['Na_actP'],self.params['Na_actW'])*(self.params['V']-self.params['E_Na'])\
                            -self.params['g_K']*self.params['n_K']*(self.params['V']-self.params['E_K']))
        #print "V: ",self.params['V']
        if self.params['recordAct'] == True:
            #self.params['actVals'].append([curT,-self.params['g_K']*self.params['n_K']*(self.params['V']-self.params['E_K'])])
            self.params['actVals'].append([curT,curAct])
        if self.params['recordV'] == True:
            #self.params['vVals'].append([curT,-self.params['g_Na']*self.pHStyleCurve(self.params['V'],self.params['Na_actP'],self.params['Na_actW'])*(self.params['V']-self.params['E_Na'])])
            self.params['vVals'].append([curT,self.params['V']])
        if self.params['V']>=self.params['threshold'] and self.params['spikeRecorded']==False:
            self.params['spikeOuts'].append(curT)
            self.params['spikeRecorded'] = True
        if self.params['V']<self.params['threshold'] and self.params['spikeRecorded']==True:
            self.params['spikeRecorded'] = False

#Page 328 of the green book, model neuron. 
'''
C - capacitance scalar for V changes
E_L - resting Potential
g_l = scalar for leaking
E_NA - Equilibrium pot for Na.
Na_actP - activation midpoint for Na channels.
Na_actW - activation width for Na channels.
g_Na - scalar for Na
E_K - Equilibrium pot for K
g_K - scalar for K
K_actP - activation midpoint for K channels.
K_actW - activation width for K channels.
K_t - delay for K
E_KS - Equilibrium pot for K (slow)
g_KS - scalar for K (slow)
KS_actP - activation midpoint for K (slow) channels.
KS_actW - activation width for K (slow) channels.
KS_t - delay for K (slow)
I - current in
'''
class P328Neuron(Neuron):
    def __init__(self,networkC,params):
        self.params = params
        self.networkC = networkC
        self.connectionsOut = []
        self.connectionsIn = []
        self.params['spikeRecorded'] = False
        self.params['n_K'] = 0
        self.params['n_KS'] = 0
        self.params['V'] = self.params['E_L']
        try:
            self.params['name']
        except:
            self.params['name'] = "Untitled P328 Neuron id:"+str(self.params['id'])+" (Poisson)"
        try:
            self.params['spikeOuts']
        except:
            self.params['spikeOuts'] = []
        try:
            self.params['actVals']
        except:
            self.params['actVals'] = []
        try:
            self.params['vVals']
        except:
            self.params['vVals'] = []
        try:
            self.params['recordAct']
        except:
            self.params['recordAct'] = False
        try:
            self.params['recordV']
        except:
            self.params['recordV'] = False
        try:
            self.params['exScale']
        except:
            self.params['exScale'] = 1
            print "No scale direction defined for ",self.params['name']," so setting as excitatory"
        try:
            self.params['syn_K']
        except:
            self.params['syn_K'] = 0.0
            print "No synaptic Input Eq V specified, setting as ZERO! (Ok if no input)"
        # move to equilibium:
    def pHStyleCurve(self,V,V_half,k):
        return 1.0/(1.0+np.power(np.e,((V_half-V)/k)))
    def update(self,curT):
        # calculate inputs from input's outputs... (i.e. calculate the presynaptic activity)
        # Go through all incoming connections:
        curAct = 0.0
        for inputC in self.connectionsIn:
            curAct += inputC.getCurExVec(curT,False,0.0)
        self.params['n_K']+= self.networkC.params['dt']*(self.pHStyleCurve(self.params['V'],self.params['K_actP'],self.params['K_actW'])-self.params['n_K'])/self.params['K_t']
        self.params['n_KS']+= self.networkC.params['dt']*(self.pHStyleCurve(self.params['V'],self.params['KS_actP'],self.params['KS_actW'])-self.params['n_KS'])/self.params['KS_t']
        #print "n_K: ",self.params['n_K']
        self.params['V']+= self.networkC.params['dt']*(1/self.params['C'])*(self.params['I']\
                            -curAct*(self.params['V']-self.params['syn_K'])\
                            -self.params['g_L']*(self.params['V']-self.params['E_L'])\
                            -self.params['g_Na']*self.pHStyleCurve(self.params['V'],self.params['Na_actP'],self.params['Na_actW'])*(self.params['V']-self.params['E_Na'])\
                            -self.params['g_K']*self.params['n_K']*(self.params['V']-self.params['E_K'])
                            -self.params['g_KS']*self.params['n_KS']*(self.params['V']-self.params['E_K']))
        #print "V: ",self.params['V']
        if self.params['recordAct'] == True:
            #self.params['actVals'].append([curT,-self.params['g_K']*self.params['n_K']*(self.params['V']-self.params['E_K'])])
            self.params['actVals'].append([curT,-curAct*(self.params['V']-self.params['syn_K'])])
        if self.params['recordV'] == True:
            #self.params['vVals'].append([curT,-self.params['g_Na']*self.pHStyleCurve(self.params['V'],self.params['Na_actP'],self.params['Na_actW'])*(self.params['V']-self.params['E_Na'])])
            self.params['vVals'].append([curT,self.params['V']])
        if self.params['V']>=self.params['threshold'] and self.params['spikeRecorded']==False:
            self.params['spikeOuts'].append(curT)
            self.params['spikeRecorded'] = True
        if self.params['V']<self.params['threshold'] and self.params['spikeRecorded']==True:
            self.params['spikeRecorded'] = False


def addNeuron(networkC,params):
    checkType = True
    try:
        params['type']
    except:
        checkType = False
    if checkType == True:    
        if params['type'] == "poisson":
            return PoissonNeuron(networkC,params)
        if params['type'] == "lif":
            return LIFNeuron(networkC,params)
        if params['type'] == "constantrate":
            return ConstantRateNeuron(networkC,params)
        if params['type'] == "srm":
            return SRMNeuron(networkC,params)
        if params['type'] == "p89":
            return P89Neuron(networkC,params)
        if params['type'] == "p328":
            return P328Neuron(networkC,params)        
        else:
            print "WARNING: Neuron not set"
            return None           
    else:
        print "WARNING: Neuron not set"
        return None

'''
# TEST:
globalsM = {'dt':0.01,'responseLimitCDF':0.99}
params = {'responseKernel':{'type':'gamma','average':9.0,'theta':1.0},
          'lambdaZero':0.0}
pN = PoissonNeuron(globalsM,params)
print pN.responseKernel.getVal(3)    
'''    