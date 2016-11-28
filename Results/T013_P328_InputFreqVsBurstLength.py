'''
Created on 30 June 2016

@author: s1144899
Test the neuron for to see how the burst length and the input freq. are related....
'''
import Model,datetime, numpy as np
# Set up some poisson Neurons:
'''
Neurons
'''
'''
C - capacitance scalar for V changes
E_L - resting Potential
g_L = scalar for leaking
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
constantRateNeuron = {'type':"constantrate",
          'name':"Very active input neuron with a target rate of up to 20Hz",
          'spikeSep':34E-3,#10Hz, seems reasonable.
          'recordAct':False,
          'thresh':15.0,
          'exScale':1}
singleSpikeBurster = {'type':"p328",
          'name':"Demo p328 type neuron",
          'inateProb':0,
          'recordAct':True,
          'recordV':True,
          'C':1.0,
          'E_L':-80E-3,
          'g_L':8*1E3,
          'E_Na':60E-3,
          'Na_actP':-20E-3,
          'Na_actW':15E-3,
          'g_Na':20E3,
          'E_K':-90E-3,
          'g_K':9E3,
          'K_actP':-24E-3,
          'K_actW':8E-3,
          'K_t':0.19E-3,
          'g_KS':20E3,
          'KS_actP':-37E-3,
          'KS_actW':5E-3,
          'KS_t':20E-3,
          'I':0,
          'threshold':-20E-3,
          'exScale':1,
          'responseKernel':{'type':'exDecay',
                             'timeConst':0.42,
                             'mult':5}}
segmentNeuron = {'type':"p328",
          'name':"Demo P89 type neuron",
          'inateProb':0,
          'recordAct':True,
          'recordV':True,
          'C':1.0,
          'E_L':-80E-3,
          'g_L':8*1E3,
          'E_Na':60E-3,
          'Na_actP':-20E-3,
          'Na_actW':15E-3,
          'g_Na':20E3,
          'E_K':-90E-3,
          'g_K':9E3,
          'K_actP':-25E-3,
          'K_actW':5E-3,
          'K_t':0.152E-3,
          'g_KS':5E3,
          'KS_actP':-20E-3,
          'KS_actW':6E-3,
          'KS_t':30E-3,
          'I':0,
          'threshold':-20E-3,
          'exScale':0.15}

delayNeuron = {'type':"p328",
          'name':"Demo P89 type neuron",
          'inateProb':0,
          'recordAct':True,
          'recordV':True,
          'C':1.0,
          'E_L':-80E-3,
          'g_L':8*1E3,
          'E_Na':60E-3,
          'Na_actP':-20E-3,
          'Na_actW':15E-3,
          'g_Na':20E3,
          'E_K':-90E-3,
          'g_K':9E3,
          'K_actP':-24E-3,
          'K_actW':8E-3,
          'K_t':0.152E-3,
          'g_KS':2E3,
          'KS_actP':-37E-3,
          'KS_actW':5E-3,
          'KS_t':20E-3,
          'I':0,
          'threshold':-20E-3,
          'exScale':-0.2,
          'responseKernel':{'type':'exDecay',
                             'timeConst':0.42,
                             'mult':5}}
'''
Connections
'''
stableConn = {'responseKernel':{'type':'PSD',
                             'average':0.002,
                             'theta':5},
            'postScale':0.1,
            'learn':False,
            'active':True}
#None
'''
Network
'''
# This way we can add lots of the same neurons!
neuronsList = {1:constantRateNeuron,
               2:singleSpikeBurster,
               3:segmentNeuron,
               4:delayNeuron,
               5:singleSpikeBurster,
               6:segmentNeuron}
# [From,To,Type]
connectionsList = [[1,2,stableConn],
                   [2,3,stableConn],
                   [2,4,stableConn],
                   [3,5,stableConn],
                   [4,5,stableConn],
                   [5,6,stableConn]]
# Save
params={'neurons':neuronsList,
        'connections':connectionsList,
        'dt':0.01E-3,
        'normFactorDX':0.001,
        'responseLimitCDF':0.99,
        'pickleOutFilePath':"/home/s1144899/Downloads/testPythonNeurons.pkl",
        'jsonOutFilePath':"/home/s1144899/Downloads/testPythonNeurons.jso"
        }
'''
Model Run
'''
print "Setting up..."
model1 = Model.Model(params)
print "Running model..."
'''
runLength = 10E-3
model1.run(runLength)
model1.params['neurons'][1]['I']=100
model1.run(2E-3)
model1.params['neurons'][1]['I']=0
model1.run(34E-3)
model1.params['neurons'][1]['I']=100
model1.run(2E-3)
model1.params['neurons'][1]['I']=0
model1.run(34E-3)
model1.params['neurons'][1]['I']=100
model1.run(2E-3)
model1.params['neurons'][1]['I']=0
model1.run(34E-3)
model1.params['neurons'][1]['I']=100
model1.run(2E-3)
model1.params['neurons'][1]['I']=0
model1.run(100E-3)
'''
model1.run(300E-3)
'''
Analysis
'''
from Analysis import pltV,pltSpikes
import matplotlib.pyplot as plt
pltV(model1,plt,2,'vVals')
pltV(model1,plt,3,'vVals')
#pltSpikes(model1,plt,6,-0.03)
#pltV(model1,plt,1,'actVals')
#plt.legend()
plt.show()

def getBursts(model1,plt,neuronID):
    neuron = model1.params['neurons'][neuronID]['vVals']