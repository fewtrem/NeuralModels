'''
Created on 30 June 2016

@author: s1144899
Test the neuron for burst-like behaviour on P89 of the green book...
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
demoNeuron = {'type':"p89",
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
          'g_K':8E3,
          'K_actP':-25E-3,
          'K_actW':5E-3,
          'K_t':1E-3,
          'I':0,
          'threshold':0,
          'exScale':1,
          'responseKernel':{'type':'exDecay',
                             'timeConst':0.42,
                             'mult':5}}
'''
Connections
'''
#None
'''
Network
'''
# This way we can add lots of the same neurons!
neuronsList = {1:demoNeuron}
# [From,To,Type]
connectionsList = []
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
runLength = 10E-3
model1.run(runLength)
model1.params['neurons'][1]['I']=5
a = datetime.datetime.now()
model1.run(100E-3)
b = datetime.datetime.now()
print b-a
model1.params['neurons'][1]['I']=0
model1.run(100E-3)
'''
Analysis
'''
from Analysis import pltV,pltSpikes
import matplotlib.pyplot as plt
pltV(model1,plt,1,'vVals')
pltSpikes(model1,plt,1,-0.03)
#plt.legend()
plt.show()