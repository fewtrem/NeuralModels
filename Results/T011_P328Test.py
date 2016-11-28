'''
Created on 30 June 2016

@author: s1144899
Test the neuron for burst-like behaviour on P328 of the green book...
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
demoNeuron = {'type':"p328",
          'name':"Demo P328 type neuron",
          'inateProb':0,
          'recordAct':True,
          'recordV':True,
          'C':1.0,
          'E_L':-80E-3,
          'g_L':8E3,
          'E_Na':60E-3,
          'Na_actP':-20E-3,
          'Na_actW':15E-3,
          'g_Na':20E3,
          'E_K':-90E-3,
          'g_K':9E3,#10
          'K_actP':-25E-3,
          'K_actW':5E-3,
          'K_t':0.152E-3,#1
          'g_KS':5E3,
          'KS_actP':-20E-3,
          'KS_actW':5E-3,
          'KS_t':20E-3,
          'I':4,
          'threshold':-20E-3,
          'exScale':0.15}
'''
Connections
'''
stableConn = {'responseKernel':{'type':'PSD',
                             'average':0.042,
                             'theta':5},
            'postScale':5.0,
            'learn':False,
            'active':True}
#None
'''
Network
'''
# This way we can add lots of the same neurons!
neuronsList = {1:demoNeuron,
               2:demoNeuron}
# [From,To,Type]
connectionsList = []
#connectionsList = [[1,2,stableConn]]
# Save
params={'neurons':neuronsList,
        'connections':connectionsList,
        'dt':0.001E-3,
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
runLength = 200E-3
model1.run(runLength)
'''
model1.params['neurons'][1]['I']=5
model1.run(10E-3)
model1.params['neurons'][1]['I']=5
model1.run(300E-3)

model1.params['neurons'][1]['I']=0
model1.run(100E-3)
model1.params['neurons'][1]['I']=10
model1.run(100E-3)
model1.params['neurons'][1]['I']=0
model1.run(100E-3)
'''
'''
Analysis
'''
from Analysis import pltV,pltSpikes
import matplotlib.pyplot as plt
pltV(model1,plt,1,'actVals')
pltV(model1,plt,1,'vVals')
pltSpikes(model1,plt,1,0.20)
#pltV(model1,plt,1,'actVals')
#plt.legend()
plt.show()